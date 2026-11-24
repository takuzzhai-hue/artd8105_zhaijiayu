"""深度辅助与触觉痕迹：不调用图像生成模型，不新增场景物体。"""
from pathlib import Path
from functools import lru_cache
from threading import Lock
import cv2
import numpy as np
from PIL import Image

PROJECT=Path(__file__).resolve().parents[1]
MODEL='depth-anything/Depth-Anything-V2-Small-hf'
REVISION='5426e4f0f36572d16453bbda7a8389317b1bef99'
LOCK=Lock()
NAMES={'depth_focus','local_silhouette','touch_trace'}

def register(define,number,choice,operations):
    entries=[('depth_focus',{'amount':number(0,1,.5)},'保留目标，按相对深度合成虚化','只记得她的脸'),
             ('local_silhouette',{'amount':number(0,1,1),'tone':choice('black','gray','white')},'分割人物后填平色，保留轮廓','记得有人在，但想不起样子'),
             ('touch_trace',{'amount':number(0,1,.45),'angle':number(-180,180,25),'mode':choice('smudge','exposure'),'stops':number(-1,1,.35)},'局部擦抹轨迹与抽象指纹脊线，不生成手','那里无法言说，只想留下一道抚摸过的痕迹')]
    for name,params,desc,example in entries:
        define(name,'local','post',params,desc,example,'perceptual_effects.apply',
               '确定性的非生成视觉转译；AI只辅助深度或分割。指纹为抽象合成纹理，不是任何人的真实指纹。')
        operations[name]['category']='E'
    operations['depth_focus']['reference']='黎朗（用户提供的虚焦方向，具体作品待核实）；Depth Anything仅为本项目实现工具'
    operations['local_silhouette']['reference']='Lebohang Kganye / Reconstruction of a Family'
    operations['touch_trace']['reference']='Aspen Mays 接触印相；Gerhard Richter / Overpainted Photographs（视觉参考，非复现材料工艺）'

@lru_cache(maxsize=1)
def load_model():
    import torch
    from transformers import AutoImageProcessor,AutoModelForDepthEstimation
    torch.set_num_threads(4)
    options=dict(revision=REVISION,cache_dir=str(PROJECT/'.models'),local_files_only=True)
    processor=AutoImageProcessor.from_pretrained(MODEL,**options)
    model=AutoModelForDepthEstimation.from_pretrained(MODEL,use_safetensors=True,**options).eval().to('cpu')
    return processor,model

def estimate_depth(x):
    import torch
    processor,model=load_model()
    rgb=Image.fromarray(np.round(np.clip(x,0,1)*255).astype(np.uint8))
    with LOCK,torch.inference_mode():
        inputs=processor(images=rgb,return_tensors='pt')
        output=model(**inputs).predicted_depth.unsqueeze(1)
        depth=torch.nn.functional.interpolate(output,size=x.shape[:2],mode='bicubic',align_corners=False)[0,0].cpu().numpy().copy()
    if not np.isfinite(depth).all(): raise ValueError('深度图含无效值')
    lo,hi=np.quantile(depth,[.02,.98])
    if hi-lo<1e-6: raise ValueError('深度图缺少可靠层次')
    return np.clip((depth-lo)/(hi-lo),0,1).astype(np.float32)

def depth_blur(x,mask,depth,amount):
    target=mask>.5
    if not target.any(): raise ValueError('没有可用的清晰目标')
    focal=float(np.median(depth[target]))
    distance=np.clip((np.abs(depth-focal)-.035)/.3,0,1)
    # 逐级虚化、背景归一化卷积，避免把人物颜色拖入背景。
    strength=distance*amount;out=x.copy();background=1-mask
    for lower,upper in zip(np.linspace(0,1,7)[:-1],np.linspace(0,1,7)[1:]):
        sigma=max(.3,min(x.shape[:2])*.028*upper)
        weight=cv2.GaussianBlur(background,(0,0),sigma)
        layer=cv2.GaussianBlur(x*background[...,None],(0,0),sigma)/np.maximum(weight[...,None],1e-5)
        layer=np.where((weight<1e-4)[...,None],x,layer)
        blend=np.clip((strength-lower)/(upper-lower),0,1)[...,None]
        out=out*(1-blend)+layer*blend
    return x*mask[...,None]+out*(1-mask[...,None]),focal

def trace_mask(mask,angle):
    yy,xx=np.indices(mask.shape,dtype=np.float32);ys,xs=np.where(mask>.5)
    if len(xs)<8: raise ValueError('触摸位置过小或不存在，不能随意在全图加痕迹')
    cx=float(np.mean(xs));cy=float(np.mean(ys));theta=np.deg2rad(angle)
    u=(xx-cx)*np.cos(theta)+(yy-cy)*np.sin(theta)
    v=-(xx-cx)*np.sin(theta)+(yy-cy)*np.cos(theta)
    short=min(mask.shape);length=max(8,min(short*.38,float(np.ptp(xs)+np.ptp(ys))*.5))
    width=max(4,length*.16)
    trail=np.exp(-((u/length)**4+(v/width)**2)*2)
    # 椭圆弧状脊线，不取用生物识别数据；仅作指腹接触的视觉隐喻。
    radial=np.sqrt(((u-length*.25)/(width*1.3))**2+(v/width)**2)
    ridges=(.5+.5*np.cos(radial*35))**6
    finger=np.exp(-radial**4)*ridges
    return np.clip((.65*trail+.35*finger)*mask,0,1).astype(np.float32)

def apply(current,operation,masks,source=None,folder=None):
    name=operation['name'];p=operation['parameters'];region=operation['region']
    if not masks or region not in masks: raise ValueError('需要实际分割区域；不生成虚构人物或猜测手指位置')
    floating=np.issubdtype(current.dtype,np.floating)
    x=current.astype(np.float32)/(1 if floating else 255)
    mask=np.asarray(masks[region],np.float32)
    if mask.shape!=x.shape[:2] or not np.isfinite(mask).all() or not np.any(mask>.5): raise ValueError('区域蒙版无效')
    mask=np.clip(mask,0,1);a=p['amount']
    metadata=dict(category='E',generated=False,pipeline_stage=name,region=region,simulated=True)
    if a==0: return current.copy(),metadata
    if name=='depth_focus':
        try:
            depth=estimate_depth(x)
            out,focal=depth_blur(x,mask,depth,a)
            metadata.update(depth_model=MODEL,depth_revision=REVISION,focal_relative_depth=focal,display_note='AI估计相对深度的合成虚化；不是物理距离或真实重新对焦，不恢复原本失焦细节')
            if folder:
                folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
                np.save(folder/'depth_relative.npy',depth)
                Image.fromarray(np.round(depth*65535).astype(np.uint16)).save(folder/'depth_relative.png')
                metadata['depth_file']='depth_relative.npy'
        except (OSError,ValueError,RuntimeError,ImportError) as exc:
            out=x*mask[...,None]+cv2.GaussianBlur(x,(0,0),max(.3,min(x.shape[:2])*.02*a))*(1-mask[...,None])
            metadata.update(depth_fallback=True,depth_error=type(exc).__name__,display_note='深度估计不可用，本步明确降级为蒙版合成虚化，不声称按深度处理')
    elif name=='local_silhouette':
        if float(mask.mean())>.85: raise ValueError('人物蒙版覆盖几乎全图，拒绝把整张照片填成剪影')
        tone={'black':.025,'gray':.45,'white':.97}[p['tone']]
        alpha=(mask*a)[...,None];out=x*(1-alpha)+tone*alpha
        metadata['display_note']='SAM区域内平色剪影，不新增人体、脸或背景'
    elif name=='touch_trace':
        trace=trace_mask(mask,p['angle'])*a
        if p['mode']=='exposure':
            from pipeline_effects import linear,display,develop
            from develop_test import RAW_EXTENSIONS
            if source and Path(source).suffix.lower() in RAW_EXTENSIONS:
                import rawpy
                with rawpy.imread(str(source)) as raw:
                    base=develop(raw,output_shape=x.shape)
                    variant=develop(raw,output_shape=x.shape,exp_shift=2**p['stops'])
                out=x+(variant-base)*trace[...,None];metadata['category']='R+E'
                metadata['display_note']='程序触摸轨迹驱动RAW曝光差异合成；不是实际手指接触底片'
            else:
                out=x+(display(linear(x)*2**p['stops'])-x)*trace[...,None]
                metadata['display_note']='渲染照片上的曝光痕迹模拟（E），不声称RAW处理'
        else:
            theta=np.deg2rad(p['angle']);distance=min(x.shape[:2])*.035*a
            layers=[]
            for t in np.linspace(-1,1,9):
                m=np.float32([[1,0,np.cos(theta)*distance*t],[0,1,np.sin(theta)*distance*t]])
                layers.append(cv2.warpAffine(x,m,(x.shape[1],x.shape[0]),borderMode=cv2.BORDER_REFLECT_101))
            smeared=cv2.GaussianBlur(sum(layers)/len(layers),(0,0),max(.3,min(x.shape[:2])*.003))
            alpha=trace[...,None];out=x*(1-alpha)+smeared*alpha
            # 原片色调上的轻微油印起伏，而非贴一只手。
            out+=alpha*.18*(1-x)
            metadata['display_note']='确定性擦抹轨迹和抽象指纹纹理；不是真实指纹，不新增手或物体'
        if folder:
            folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
            Image.fromarray(np.round(trace*255).astype(np.uint8)).save(folder/'touch_trace_mask.png')
            metadata['trace_file']='touch_trace_mask.png'
    else: raise ValueError('未知非生成效果')
    out=np.clip(out,0,1).astype(np.float32)
    return (out if floating else np.round(out*255).astype(np.uint8)),metadata

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--download',action='store_true',help='安装固定版本的Depth Anything权重')
    args=parser.parse_args()
    if args.download:
        from huggingface_hub import snapshot_download
        print(snapshot_download(MODEL,revision=REVISION,cache_dir=str(PROJECT/'.models'),allow_patterns=['*.json','model.safetensors']))
    else: parser.print_help()
