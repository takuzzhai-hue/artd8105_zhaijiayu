"""RAW 仅显影一次，之后按顺序在上一结果上继续处理。无 API、无随机数。"""
from __future__ import annotations
import argparse
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import hashlib
import json
import os
os.environ.setdefault('OMP_NUM_THREADS','1')
import cv2
import numpy as np
import rawpy
from operations import validate_operation, OPERATIONS
from photo_pipeline import apply_preview, SUPPORTED
from pipeline_effects import NAMES as PIPELINE_NAMES, apply as apply_pipeline
from poetic_effects import NAMES as POETIC_NAMES, apply as apply_poetic
from perceptual_effects import NAMES as PERCEPTUAL_NAMES, apply as apply_perceptual

PROJECT=Path(__file__).resolve().parents[1]


def sha256(path):
    digest=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''): digest.update(block)
    return digest.hexdigest()


def save_png(path,image):
    pixels=np.round(np.clip(image,0,1)*65535).astype(np.uint16)
    if not cv2.imwrite(str(path),cv2.cvtColor(pixels,cv2.COLOR_RGB2BGR)):
        raise OSError(f'无法保存 {path}')


def load_mask(path,shape):
    pixels=cv2.imread(str(path),cv2.IMREAD_UNCHANGED)
    if pixels is None or pixels.ndim!=2 or pixels.dtype not in (np.uint8,np.uint16):
        raise ValueError('蒙版必须是可读取的 8/16 位灰度图')
    h,w=shape[:2]
    mh,mw=pixels.shape
    if abs(mw/mh-w/h)>0.01:
        raise ValueError('蒙版比例与显影图不匹配；蒙版必须对应旋转后的完整画面')
    mask=pixels.astype(np.float32)/np.iinfo(pixels.dtype).max
    if (mh,mw)!=(h,w): mask=cv2.resize(mask,(w,h),interpolation=cv2.INTER_LINEAR)
    if not np.any(mask>0): raise ValueError('蒙版为空，无法确定作用区域')
    return mask


def execute(raw_path,operation_file,full_size=False,output_dir=None):
    raw_path=Path(raw_path).resolve();operation_file=Path(operation_file).resolve()
    def reject_constant(value): raise ValueError(f'JSON 包含非有限数值：{value}')
    document=json.loads(operation_file.read_text(encoding='utf-8'),parse_constant=reject_constant)
    if isinstance(document,list): operations=document;region_paths={}
    elif isinstance(document,dict) and set(document)<= {'operations','regions'}:
        operations=document.get('operations');region_paths=document.get('regions',{})
    else: raise ValueError('JSON 必须是操作数组，或包含 operations、regions 的对象')
    if not isinstance(operations,list) or not operations: raise ValueError('operations 必须是非空数组')
    if not isinstance(region_paths,dict) or any(not isinstance(k,str) or not isinstance(v,str) for k,v in region_paths.items()):
        raise ValueError('regions 必须将区域名映射到蒙版文件路径')
    folder=Path(output_dir) if output_dir else PROJECT/'outputs'/('engine_'+datetime.now(ZoneInfo('Asia/Shanghai')).strftime('%Y%m%d_%H%M%S_%f'))
    folder.mkdir(parents=True,exist_ok=False)
    cv2.setNumThreads(1);cv2.ocl.setUseOpenCL(False)
    print('正在初次显影 RAW…',flush=True)
    with rawpy.imread(str(raw_path)) as raw:
        # sRGB 原色、线性编码；自行应用准确的 sRGB 显示曲线。
        linear=raw.postprocess(half_size=not full_size,use_camera_wb=True,use_auto_wb=False,
            no_auto_bright=True,gamma=(1,1),output_color=rawpy.ColorSpace.sRGB,output_bps=16)
    current=linear.astype(np.float32)/65535
    del linear
    current=np.where(current<=0.0031308,current*12.92,1.055*current**(1/2.4)-0.055).astype(np.float32)
    save_png(folder/'step_00.png',current)
    report=dict(mode='sequential',raw=str(raw_path),raw_sha256=sha256(raw_path),
        half_size=not full_size,size=[current.shape[1],current.shape[0]],
        versions=dict(rawpy=rawpy.__version__,numpy=np.__version__,opencv=cv2.__version__),
        initial_development=dict(no_auto_bright=True,use_camera_wb=True,gamma=[1,1],output_bps=16),
        note='初始线性 sRGB 显影后转显示 sRGB；内存浮点累计处理，保存 16 位 PNG。曝光/冷暖是后处理，不重显影。',
        operations_input=document,regions={},steps=[])
    history=[];void_regions=set()
    def write_log():
        (folder/'log.json').write_text(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf-8')
    for index,entry in enumerate(operations,1):
        record=dict(step=index,source=entry.get('source') if isinstance(entry,dict) else None,
                    name=entry.get('name') if isinstance(entry,dict) else None,
                    parameters=entry.get('parameters') if isinstance(entry,dict) else None,
                    region=entry.get('region') if isinstance(entry,dict) else None)
        status='无法执行';reason=''
        try:
            if not isinstance(entry,dict) or set(entry)!= {'source','name','parameters','region'}:
                raise ValueError('每项必须包含且仅包含 source、name、parameters、region')
            if not isinstance(entry['source'],str) or not entry['source'].strip(): raise ValueError('缺少对应原句')
            op=validate_operation({k:entry[k] for k in ('name','parameters','region')},region_paths)
            name=op['name'];region=op['region']
            if region in void_regions and name!='void':
                status='与之前的操作冲突';reason='该区域已被 void 替为空白，不能再处理其原有内容；本步跳过'
            else:
                if name not in SUPPORTED | PIPELINE_NAMES | PERCEPTUAL_NAMES | POETIC_NAMES | {'void'}:
                    raise ValueError('该操作尚未接入叠加引擎，或需要原始传感器数据/生成服务，不能在上一结果上执行')
                masks={}
                if region is not None:
                    path=(operation_file.parent/region_paths[region]).resolve()
                    masks[region]=load_mask(path,current.shape)
                    report['regions'][region]=dict(path=str(path),sha256=sha256(path))
                if name=='void':
                    m=cv2.GaussianBlur(masks[region],(0,0),max(1,min(current.shape[:2])*0.01))[:,:,None]
                    candidate=current*(1-m)+m
                elif name in POETIC_NAMES:
                    candidate,metadata=apply_poetic(current,op,masks,raw_path,folder/('effect_'+str(index)))
                    record['pipeline']=metadata
                elif name in PERCEPTUAL_NAMES:
                    candidate,metadata=apply_perceptual(current,op,masks,raw_path,folder/('effect_'+str(index)))
                    record['pipeline']=metadata
                elif name in PIPELINE_NAMES:
                    if name=='multi_frame_median':
                        op['parameters']['frames']=[str((operation_file.parent/p).resolve()) for p in op['parameters']['frames']]
                    candidate,metadata=apply_pipeline(current,op,raw_path,masks,allow_frames=True)
                    record['pipeline']=metadata
                else: candidate=apply_preview(current,op,masks)
                if candidate.shape!=current.shape or not np.isfinite(candidate).all(): raise ValueError('处理产生了无效图像')
                current=candidate
                if name=='void': void_regions.add(region)
                history.append(op)
                status='成功';reason='在上一步内存结果上应用一次；此前局部操作不重复应用'
                if name=='white_balance': reason+='；冷暖使用 RGB 通道增益近似，不是相机 RAW 白平衡'
                if name=='exposure': reason+='；sRGB 线性化后乘曝光增益，不能恢复先前裁剪的细节'
        except (ValueError,TypeError,KeyError,NotImplementedError,cv2.error,OSError,rawpy.LibRawError) as exc:
            reason=str(exc)
        filename=f'step_{index:02d}.png'
        save_png(folder/filename,current)
        record.update(status=status,reason=reason,image=filename,sha256=sha256(folder/filename),applied_operations=list(history))
        report['steps'].append(record);write_log()
        print(f'{index}/{len(operations)} {record["name"]}: {status}',flush=True)
    print(f'完成：{folder}',flush=True)
    return folder,report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--raw',type=Path,required=True)
    parser.add_argument('--operations',type=Path,required=True)
    parser.add_argument('--full-size',action='store_true')
    parser.add_argument('--output',type=Path,help='新的输出目录；已存在时拒绝覆盖')
    args=parser.parse_args()
    try: execute(args.raw,args.operations,args.full_size,args.output)
    except (ValueError,OSError,rawpy.LibRawError) as exc: parser.exit(1,f'执行失败：{exc}\n')
