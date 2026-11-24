"""诗意摄影的非生成转译；保留来源，不声称真实材料损伤或记忆恢复。"""
from pathlib import Path
import json
import cv2
import numpy as np
from PIL import Image, ImageDraw

NAMES={'retain_gesture','local_cutout','memory_fragments','paper_decay','image_codes'}

def register(define,number,choice,operations):
    specs=[
      ('retain_gesture','local',{'amount':number(0,1,.65),'tone':choice('gray','white','dark')},'只保留选中动作，其他部分褪去但保留痕迹','只记得我们牵着手，其他都淡了'),
      ('local_cutout','local',{'amount':number(0,1,1),'tone':choice('white','black')},'硬边挖空可见对象，保留其占据的位置；不补背景','把这个人剪掉，只留下空洞'),
      ('memory_fragments','global',{'amount':number(0,1,.55),'direction':choice('vertical','horizontal')},'少量宽条切割移位，只取当前照片内容','还记得这些片段，但它们的位置对不上了'),
      ('paper_decay','global',{'amount':number(0,1,.45)},'边缘受潮、纸面褪色和少量裂痕的数字模拟','照片像被水泡过，正在慢慢坏掉'),
      ('image_codes','global',{'amount':number(0,1,.7)},'将当前图像采样RGB数值转为十六进制字符，并保存数据','照片只剩下数字和编码')]
    for name,scope,params,desc,example in specs:
        define(name,scope,'post',params,desc,example,'poetic_effects.apply','E类数字转译，不新增场景内容，不复原艺术家的材料工艺')
        operations[name]['category']='E'

def apply(current,operation,masks,source=None,folder=None):
    name=operation['name'];p=operation['parameters'];a=p['amount']
    floating=np.issubdtype(current.dtype,np.floating)
    x=current.astype(np.float32)/(1 if floating else 255)
    h,w=x.shape[:2];short=min(h,w)
    meta=dict(category='E',generated=False,simulated=True,pipeline_stage=name)
    if a==0:return current.copy(),meta
    mask=None
    if name in {'retain_gesture','local_cutout'}:
        mask=np.asarray((masks or {}).get(operation['region']),dtype=np.float32)
        if mask.shape!=(h,w) or not np.isfinite(mask).all() or not np.any(mask>.5):
            raise ValueError('需要实际可见动作或对象的有效分割区域')
        mask=np.clip(mask,0,1)
        if float((mask>.5).mean())>.85:raise ValueError('目标覆盖几乎全图，不能将整张照片挖空或遮盖')
    if name=='retain_gesture':
        # 保留核心原像素；仅向外羽化，避免动作本身被遮盖。
        distance=cv2.distanceTransform((mask<.5).astype(np.uint8),cv2.DIST_L2,5)
        keep=np.maximum(mask,np.clip(1-distance/max(2,short*.018),0,1))
        tone={'gray':.55,'white':.95,'dark':.06}[p['tone']]
        alpha=(1-keep)*min(a,.82)
        out=x*(1-alpha[...,None])+tone*alpha[...,None]
        meta['display_note']='只保留可见动作；背景数字遮蔽仍留痕，不生成记不清的内容'
    elif name=='local_cutout':
        cut=(mask>.5).astype(np.float32);alpha=(cut*a)[...,None]
        out=x*(1-alpha)+({'white':1.,'black':0.}[p['tone']])*alpha
        meta['display_note']='对象轮廓硬边挖空的平色模拟；不是透明PNG，不生成被遮挡的背景'
        if folder:
            Path(folder).mkdir(parents=True,exist_ok=True)
            Image.fromarray((cut*255).astype(np.uint8)).save(Path(folder)/'cutout_mask.png')
    elif name=='memory_fragments':
        vertical=p['direction']=='vertical';size=w if vertical else h
        edges=[0,round(size*.24),round(size*.57),round(size*.81),size]
        out=x.copy();mapping=[]
        for i,(lo,hi) in enumerate(zip(edges[:-1],edges[1:])):
            shift=round((h if vertical else w)*a*[0,.16,-.12,.08][i])
            if vertical:out[:,lo:hi]=np.roll(x[:,lo:hi],shift,axis=0)
            else:out[lo:hi,:]=np.roll(x[lo:hi,:],shift,axis=1)
            mapping.append(dict(start=lo,end=hi,shift=shift))
        meta.update(strips=mapping,display_note='四条以内宽条重排；循环移位只使用当前照片，未扩图、未增加物体或色散')
    elif name=='paper_decay':
        yy,xx=np.indices((h,w),dtype=np.float32);nx=xx/max(1,w-1);ny=yy/max(1,h-1)
        edge=np.minimum.reduce([nx,1-nx,ny,1-ny])
        stain=np.exp(-edge*18)*(.55+.45*np.sin(nx*13+ny*9)**2)
        crack=np.exp(-((ny-(.82+.017*np.sin(nx*24)))/.0018)**2)*(nx>.55)
        alpha=np.clip(a*(.6*stain+.30*crack),0,.75)
        gray=x.mean(axis=2,keepdims=True)
        faded=x*.8+gray*.2
        out=x*(1-alpha[...,None])+(.7*faded+.3*.85)*alpha[...,None]
        meta['display_note']='确定性受潮边缘与纸面裂痕模拟，保留照片细节；非真实乳剂变化'
    elif name=='image_codes':
        # 每格字符来自当前照片对应采样点；不是随机或传感器代码。
        cw,ch=40,14
        canvas=Image.new('RGB',(w,h),(12,12,12));draw=ImageDraw.Draw(canvas);samples=[]
        for y in range(0,h,ch):
            for z in range(0,w,cw):
                sy=min(h-1,y+ch//2);sx=min(w-1,z+cw//2)
                rgb=np.round(np.clip(x[sy,sx],0,1)*255).astype(np.uint8)
                code=''.join(f'{v:02X}' for v in rgb)
                draw.text((z,y),code,fill=tuple(int(80+v*.68) for v in rgb))
                samples.append(dict(x=sx,y=sy,rgb=rgb.tolist(),hex=code))
        out=x*(1-a)+np.asarray(canvas,dtype=np.float32)/255*a
        meta.update(display_note='当前显示图像的真实RGB采样转码，不是RAW传感器数据，也不代表完整文件编码',sample_count=len(samples))
        if folder:
            Path(folder).mkdir(parents=True,exist_ok=True)
            (Path(folder)/'image_codes.json').write_text(json.dumps(dict(source='current_stage_display_RGB',samples=samples),ensure_ascii=False),encoding='utf-8')
    else:raise ValueError('未知诗意摄影效果')
    out=np.clip(out,0,1).astype(np.float32)
    return (out if floating else np.round(out*255).astype(np.uint8)),meta
