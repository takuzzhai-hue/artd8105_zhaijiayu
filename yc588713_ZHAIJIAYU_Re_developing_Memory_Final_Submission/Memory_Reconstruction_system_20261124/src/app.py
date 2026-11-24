"""本地双页摄影界面；异步任务适配器复用真实累计生成引擎。"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from threading import Lock
from uuid import uuid4
import secrets
import os
os.environ.setdefault('OMP_NUM_THREADS','1')
import time
import subprocess
from urllib.parse import urlsplit
from io import BytesIO
import qrcode
from fastapi import FastAPI, UploadFile, File, Request, HTTPException
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from pydantic import BaseModel, Field
from starlette.concurrency import run_in_threadpool
from vision import prepare_image
from develop_test import RAW_EXTENSIONS
from series import generate_series

PROJECT=Path(__file__).resolve().parents[1]
UPLOAD_ROOT=PROJECT/'outputs'/'web_uploads'
SUPPORTED=RAW_EXTENSIONS | {'.jpg','.jpeg','.png','.webp','.tif','.tiff','.heic','.heif'}
MAX_BYTES=512*1024*1024
UPLOADS={};JOBS={};LOCK=Lock()
WORKER=ThreadPoolExecutor(max_workers=1,thread_name_prefix='memory-reconstruction')
app=FastAPI(title='Memory / Reconstruction',docs_url=None,redoc_url=None)
def phone_host():
    for interface in ('en0','en1'):
        try:
            ip=subprocess.check_output(['ipconfig','getifaddr',interface],stderr=subprocess.DEVNULL,text=True).strip()
            if ip: return ip
        except (OSError,subprocess.CalledProcessError): pass
    return None
LAN_HOST=phone_host()
PUBLIC_BASE=os.getenv('PHONE_UPLOAD_BASE_URL','').rstrip('/')
allowed=['127.0.0.1','localhost','testserver']
if PUBLIC_BASE and urlsplit(PUBLIC_BASE).hostname: allowed.append(urlsplit(PUBLIC_BASE).hostname)
class NetworkHostMiddleware:
    """换 Wi-Fi/热点后接受当前网卡地址，不保留旧地址或放开任意 Host。"""
    def __init__(self,app): self.app=app
    async def __call__(self,scope,receive,send):
        hosts=list(allowed)
        host=dict(scope.get('headers',[])).get(b'host',b'').decode('latin1').split(':')[0]
        if host not in hosts:
            current=phone_host()
            if current: hosts.append(current)
        await TrustedHostMiddleware(self.app,allowed_hosts=hosts)(scope,receive,send)
app.add_middleware(NetworkHostMiddleware)
PAIRS={}

def phone_base():
    host=phone_host()
    return PUBLIC_BASE or (f'http://{host}:{os.getenv("PORT","7860")}' if host else '')

app.mount('/static',StaticFiles(directory=PROJECT/'web'),name='static')


@app.middleware('http')
async def session(request,call_next):
    owner=request.cookies.get('memory_session')
    if not owner or len(owner)!=64: owner=secrets.token_hex(32)
    request.state.owner=owner
    response=await call_next(request)
    if request.cookies.get('memory_session')!=owner:
        response.set_cookie('memory_session',owner,httponly=True,samesite='strict')
    response.headers['X-Content-Type-Options']='nosniff'
    response.headers['Referrer-Policy']='same-origin'
    if request.url.path.startswith(('/api/','/static/')) or request.url.path in ('/','/phone'):response.headers['Cache-Control']='no-store'
    return response


@app.get('/')
def index():return FileResponse(PROJECT/'web/index.html')


@app.get('/api/config')
def config():return {'formats':sorted(SUPPORTED),'max_bytes':MAX_BYTES,'mode':'live'}


def owned(items,key,request):
    value=items.get(key)
    if value is None or value['owner']!=request.state.owner:raise HTTPException(404,'此记录不存在或已过期，请重新上传照片。')
    return value


@app.post('/api/uploads')
async def upload(request:Request,photo:UploadFile=File(...)):
    suffix=Path(photo.filename or '').suffix.lower()
    if suffix not in SUPPORTED:raise HTTPException(415,'请选择 RAW、JPEG、PNG、WebP 或 TIFF 照片。')
    uid=uuid4().hex;folder=UPLOAD_ROOT/uid;folder.mkdir(parents=True)
    path=folder/('original'+suffix);total=0
    try:
        with path.open('wb') as out:
            while chunk:=await photo.read(1024*1024):
                total+=len(chunk)
                if total>MAX_BYTES:raise HTTPException(413,'照片超过 512 MB，请选择更小的文件。')
                out.write(chunk)
        preview=await run_in_threadpool(prepare_image,path)
        if min(preview.size)<4:raise ValueError('图片尺寸过小')
        await run_in_threadpool(preview.save,folder/'preview.png')
    except Exception as exc:
        path.unlink(missing_ok=True)
        if isinstance(exc,HTTPException):raise
        raise HTTPException(400,'无法读取这张照片，请检查文件是否完整或选择另一张。') from exc
    finally:await photo.close()
    UPLOADS[uid]={'owner':request.state.owner,'path':path,'preview':folder/'preview.png','width':preview.width,'height':preview.height}
    return {'id':uid,'width':preview.width,'height':preview.height,'preview':f'/api/uploads/{uid}/preview','name':photo.filename}


@app.get('/api/uploads/{uid}/preview')
def preview(uid:str,request:Request):return FileResponse(owned(UPLOADS,uid,request)['preview'])


class GenerationRequest(BaseModel):
    upload_id:str=Field(min_length=1,max_length=64)
    memory:str=Field(min_length=1,max_length=10000)


def execute_job(jid,photo,memory):
    try:
        with LOCK:JOBS[jid].update(phase='running',status='正在理解照片与回忆…')
        for state in generate_series(photo,memory):
            with LOCK:
                job=JOBS[jid]
                job.update(status=state['status'],total=state.get('total'),labels=list(state.get('labels',[])))
                # URL按阶段编号固定，最终复制到result文件时不会重复显示图片。
                job['paths']=list(state['images'])
                job['composite_path']=state.get('composite');job['archive_path']=state.get('archive')
                if state.get('archive'):
                    job.update(phase='complete',total=len(job['paths']),fallback_count=state.get('fallback_count',0),skipped_count=state.get('skipped_count',0))
        with LOCK:
            if JOBS[jid]['phase']!='complete':JOBS[jid]['phase']='error'
    except Exception:
        with LOCK:JOBS[jid].update(phase='error',status='本次处理未完成，已完成的照片仍可查看。请返回修改后重试。')


@app.post('/api/jobs')
def start(body:GenerationRequest,request:Request):
    uploaded=owned(UPLOADS,body.upload_id,request)
    if not body.memory.strip():raise HTTPException(422,'请写下关于照片的回忆。')
    with LOCK:
        active=next((jid for jid,j in JOBS.items() if j['owner']==request.state.owner and j['phase'] in ('queued','running')),None)
        if active:raise HTTPException(409,detail={'message':'上一段回忆仍在重构。','job_id':active})
        jid=uuid4().hex
        JOBS[jid]={'owner':request.state.owner,'phase':'queued','status':'等待开始重构…','paths':[],'labels':[],
                   'total':None,'composite_path':None,'archive_path':None,'width':uploaded['width'],'height':uploaded['height'],'memory':body.memory}
    WORKER.submit(execute_job,jid,uploaded['path'],body.memory)
    return {'id':jid}


@app.get('/api/jobs/{jid}')
def job_status(jid:str,request:Request):
    with LOCK:
        job=owned(JOBS,jid,request)
        return {'id':jid,'phase':job['phase'],'status':job['status'],'total':job['total'],
                'images':[f'/api/jobs/{jid}/images/{i}' for i in range(len(job['paths']))],
                'labels':list(job['labels']),'fallback_count':job.get('fallback_count',0),'skipped_count':job.get('skipped_count',0),'width':job['width'],'height':job['height'],'memory':job['memory'],
                'composite':f'/api/jobs/{jid}/composite' if job['composite_path'] else None,
                'archive':f'/api/jobs/{jid}/archive' if job['archive_path'] else None}


@app.get('/api/jobs/{jid}/images/{index}')
def job_image(jid:str,index:int,request:Request):
    with LOCK:
        job=owned(JOBS,jid,request)
        if index<0 or index>=len(job['paths']):raise HTTPException(404,'这张照片尚未完成。')
        path=job['paths'][index]
    return FileResponse(path)


@app.get('/api/jobs/{jid}/composite')
def composite(jid:str,request:Request):
    job=owned(JOBS,jid,request)
    if not job['composite_path']:raise HTTPException(404,'拼合图尚未完成。')
    return FileResponse(job['composite_path'])


@app.get('/api/jobs/{jid}/archive')
def archive(jid:str,request:Request):
    job=owned(JOBS,jid,request)
    if not job['archive_path']:raise HTTPException(404,'下载包尚未完成。')
    return FileResponse(job['archive_path'],filename='memory-reconstruction.zip',media_type='application/zip')


@app.get('/phone')
def phone_page():return FileResponse(PROJECT/'web/phone.html',headers={'Cache-Control':'no-store'})

@app.post('/api/phone-pairs')
def pair_create(request:Request):
    base=phone_base()
    if not base: raise HTTPException(503,'未找到局域网地址，请将电脑连接 Wi-Fi 或手机热点。')
    now=time.time()
    with LOCK:
        for key in list(PAIRS):
            if PAIRS[key]['expires']<now and PAIRS[key]['state']!='uploading': PAIRS.pop(key)
        # 同一浏览器多标签页/重复请求共用配对，不能互相删除已扫码的链接。
        for pid,pair in PAIRS.items():
            if (pair['owner']==request.state.owner and pair['expires']>now
                and pair['state'] in ('waiting','uploading')
                and pair['url'].split('/phone#')[0]==base):
                return dict(id=pid,qr=f'/api/phone-pairs/{pid}/qr',expires_in=int(pair['expires']-now))
        pid=secrets.token_urlsafe(24);token=secrets.token_urlsafe(32)
        PAIRS[pid]=dict(owner=request.state.owner,token=token,expires=now+900,state='waiting',result=None,url=base+'/phone#'+pid+':'+token)
    return dict(id=pid,qr=f'/api/phone-pairs/{pid}/qr',expires_in=900)

@app.get('/api/phone-pairs/{pid}')
def pair_status(pid:str,request:Request):
    with LOCK:
        pair=owned(PAIRS,pid,request)
        if pair['expires']<time.time():return dict(state='expired')
        base=phone_base()
        if pair['state']=='waiting' and base and pair['url'].split('/phone#')[0]!=base:
            return dict(state='expired')
        return dict(state=pair['state'],photo=pair['result'])

@app.get('/api/phone-pairs/{pid}/qr')
def pair_qr(pid:str,request:Request):
    pair=owned(PAIRS,pid,request)
    if pair['expires']<time.time():raise HTTPException(410,'二维码已过期')
    stream=BytesIO();qrcode.make(pair['url']).save(stream,format='PNG')
    return Response(stream.getvalue(),media_type='image/png',headers={'Cache-Control':'no-store'})

@app.post('/api/phone-pairs/{pid}/upload')
async def phone_upload(pid:str,request:Request,photo:UploadFile=File(...)):
    with LOCK:
        pair=PAIRS.get(pid)
        token=request.headers.get('X-Upload-Token','')
        if not pair or not secrets.compare_digest(token,pair['token']):raise HTTPException(404,'配对链接无效，请重新扫码。')
        if pair['expires']<time.time():raise HTTPException(410,'二维码已过期，请在电脑上刷新二维码。')
        if pair['state']!='waiting':raise HTTPException(409,'照片正在传送或已发送，请在电脑上重新配对。')
        pair['state']='uploading'
    try:
        # 只赋予这一张上传电脑会话的归属，不把电脑cookie交给手机。
        request.state.owner=pair['owner']
        result=await upload(request,photo)
        with LOCK:
            if PAIRS.get(pid) is not pair or pair['expires']<time.time():
                UPLOADS.pop(result['id'],None)
                raise HTTPException(410,'配对已刷新，请重新扫码。')
            pair.update(state='received',result=result)
        return {'ok':True}
    except Exception:
        with LOCK:
            if PAIRS.get(pid) is pair:pair['state']='waiting'
        raise


if __name__=='__main__':
    import uvicorn
    uvicorn.run(app,host=os.getenv('HOST','0.0.0.0'),port=int(os.getenv('PORT','7860')))
