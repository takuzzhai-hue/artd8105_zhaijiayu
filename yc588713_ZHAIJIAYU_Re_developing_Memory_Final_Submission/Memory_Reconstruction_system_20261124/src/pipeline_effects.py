"""源数据参与的摄影实验。R 是来源，累计合成如实记为 R+E。"""
from pathlib import Path
import cv2
import numpy as np
import rawpy
from develop_test import RAW_EXTENSIONS

RAW_NAMES={'sensor_sites','raw_wb_split','raw_demosaic_linear','raw_half_detail','raw_noise_gain','raw_camera_color','dual_development'}
POST_NAMES={'faded_fog','linear_negative','local_linear_negative','local_exposure_erase'}
NAMES=RAW_NAMES|POST_NAMES|{'multi_frame_median'}

def register(define,number,choice,operations):
    rows=[
      ('sensor_sites','global','sensor',{'amount':number(0,1,.7),'scale':number(1,16,4)},'真实CFA采样点着色，不插值','我想要最原始的图像','Müller-Pohle / Digital Scores（用户提供的视觉参照）'),
      ('faded_fog','global','post',{'amount':number(0,1,.3)},'抬显示黑位、压低白位并适度去色','颜色褪掉了，有雾','Orloff / Elusive Memory（用户提供）'),
      ('raw_wb_split','local','raw',{'warmth':number(-1,1,.35),'outside_warmth':number(-1,1,-.25)},'同一RAW两组白平衡显影后按蒙版合成','她那边是暖的，其余很冷','韩磊 / 虚构的记忆（用户提供）'),
      ('raw_demosaic_linear','global','raw',{'amount':number(0,1,.65)},'比较LINEAR与AHD去马赛克差异，不保证每张图有明显伪色','画面像碎的','Ruff / jpegs（视觉参照，非原作技术复现）'),
      ('raw_half_detail','global','raw',{'amount':number(0,1,.65)},'half_size显影后放大，与全尺寸显影比较','记不清细节','Orloff；黎朗 / 1974（用户提供）'),
      ('raw_noise_gain','global','raw',{'stops':number(0,2,.5)},'关闭可控降噪并提高显影曝光；噪声与信号一起增强','很吵，颗粒很粗','Provoke（视觉参照；嘈杂是隐喻）'),
      ('raw_camera_color','global','raw',{'amount':number(0,1,.5)},'相机RGB通道作伪色显示；不是准确sRGB转换','颜色很怪，说不上来','相机原生通道实验'),
      ('linear_negative','global','post',{'amount':number(0,1,.65)},'在线性化RGB上反相再编码显示','像噩梦，明暗反了','Cordova / Fictitious Family（用户提供）'),
      ('local_linear_negative','local','post',{'amount':number(0,1,.65)},'仅在蒙版内线性反相','那里像噩梦','Cordova / Fictitious Family（用户提供）'),
      ('local_exposure_erase','local','post',{'stops':number(0,8,4)},'蒙版内增加线性曝光直到输出高光裁剪','我不记得那里有什么','Parrish；Mays / Punched out stars（用户提供）'),
      ('dual_development','global','raw',{'stops':number(.25,2,.75),'warmth':number(0,1,.4),'mix':number(0,1,.5)},'同一RAW冷暗与暖亮两个版本叠合','既是那时，又是现在','Segal / Remembered（用户提供）'),
    ]
    for name,scope,stage,params,desc,example,reference in rows:
        define(name,scope,stage,params,desc,example,'pipeline_effects.apply',
               '保留上一阶段；记录源数据与实际处理。视觉参考由用户提供，非原作方法考据。')
        operations[name].update(category='R+E' if name in RAW_NAMES else 'E',reference=reference,requires_raw=name in RAW_NAMES)
    define('multi_frame_median','global','multi_frame',{'frames':{'type':'array','items':{'type':'string'},'minItems':2}},
           '至少三张同场景真实RAW对齐后中值合成','那时街上好像没人','pipeline_effects.median_frames',
           '网页当前只接收一张；多帧请用引擎JSON提供至少两张额外RAW。不保证去除一直站着的人。',availability='deferred')
    operations['multi_frame_median'].update(category='R+E',reference='Daguerre / Boulevard du Temple（效果参照；中值合成不是长曝光）')
    operations['vignette'].update(category='E',reference='Aspen Mays 暗房作品（用户提供）',note='主动径向衰减；rawpy没有自动镜头暗角补偿可关闭，不声称反转平场校准。')

def linear(x): return np.where(x<=.04045,x/12.92,((x+.055)/1.055)**2.4)
def display(x):
    x=np.clip(x,0,1)
    return np.where(x<=.0031308,x*12.92,1.055*x**(1/2.4)-.055)
def resize(x,shape,nearest=False):
    return cv2.resize(x,(shape[1],shape[0]),interpolation=cv2.INTER_NEAREST if nearest else cv2.INTER_AREA)
def wb(raw,warmth):
    gains=np.array(raw.camera_whitebalance,dtype=float)
    if len(gains)!=4 or not np.isfinite(gains).all() or np.any(gains[:3]<=0):
        raise ValueError('此RAW没有可用相机白平衡，不能执行双白平衡实验')
    desc=raw.color_desc.decode('ascii').strip('\x00')
    for i,c in enumerate(desc[:4]):
        if c=='R': gains[i]*=2**warmth
        elif c=='B': gains[i]*=2**(-warmth)
    if gains[3]<=0: gains[3]=gains[1]
    return gains.tolist()
def develop(raw,output_shape=None,**overrides):
    settings=dict(half_size=True,use_camera_wb=True,use_auto_wb=False,no_auto_bright=True,
                  gamma=(1,1),output_color=rawpy.ColorSpace.sRGB,output_bps=16,
                  fbdd_noise_reduction=rawpy.FBDDNoiseReductionMode.Off,noise_thr=None,median_filter_passes=0)
    settings.update(overrides)
    pixels=raw.postprocess(**settings)
    if output_shape is not None:
        pixels=resize(pixels,output_shape,settings['half_size'])
    result=pixels.astype(np.float32)/65535
    if result.ndim!=3 or result.shape[2]!=3: raise ValueError('仅支持三通道RGB显影')
    return display(result)
def sites(raw,shape,scale):
    samples=raw.raw_image_visible.copy().astype(np.float32)
    colors=raw.raw_colors_visible.copy()
    if samples.ndim!=2 or colors.shape!=samples.shape or raw.raw_pattern is None:
        raise ValueError('此文件不是可读取CFA排列的单层RAW；不伪造拜耳结构')
    desc=raw.color_desc.decode('ascii').strip('\x00')
    if any(c not in 'RGB' for c in desc): raise ValueError('仅支持RGB滤色阵列，不把其他滤色器伪装成RGB')
    black=np.array(raw.black_level_per_channel,dtype=np.float32)
    if int(colors.max())>=len(black) or int(colors.max())>=len(desc):
        raise ValueError('CFA颜色索引已改变；必须在显影前读取传感器数据')
    white=float(raw.white_level)
    values=np.clip((samples-black[colors])/np.maximum(1,white-black[colors]),0,1)
    # 缩小显示时按CFA周期选取完整块，避免直接缩图只抽到一种颜色。
    ph,pw=raw.raw_pattern.shape;flip=raw.sizes.flip
    hh,ww=shape[:2]
    if flip in (5,6): hh,ww=ww,hh
    gh=max(ph,(int(hh/scale)//ph)*ph);gw=max(pw,(int(ww/scale)//pw)*pw)
    iy=np.minimum((np.arange(gh)//ph*(samples.shape[0]//ph)/max(1,gh//ph)).astype(int)*ph+np.arange(gh)%ph,samples.shape[0]-1)
    ix=np.minimum((np.arange(gw)//pw*(samples.shape[1]//pw)/max(1,gw//pw)).astype(int)*pw+np.arange(gw)%pw,samples.shape[1]-1)
    v=values[np.ix_(iy,ix)];c=colors[np.ix_(iy,ix)];out=np.zeros((*v.shape,3),np.float32)
    for k,ch in enumerate(desc): out[:,:, 'RGB'.index(ch)]+=v*(c==k)
    out=display(out)
    if flip==3: out=np.rot90(out,2)
    elif flip==5: out=np.rot90(out,1)
    elif flip==6: out=np.rot90(out,-1)
    elif flip!=0: raise ValueError('不支持该RAW方向标记，避免采样图与蒙版错位')
    return resize(out,shape,True)

def median_frames(paths,shape):
    if len(paths)<3: raise ValueError('中值去运动至少需要三张真实RAW，不能由单帧推测背景')
    images=[];reference_size=None
    for path in paths:
        if Path(path).suffix.lower() not in RAW_EXTENSIONS: raise ValueError('多帧中值需要真实RAW来源')
        with rawpy.imread(str(path)) as raw: image=develop(raw)
        if reference_size is None: reference_size=image.shape
        if image.shape!=reference_size: raise ValueError('多帧画幅或方向不一致')
        images.append(resize(image,shape))
    ref=cv2.cvtColor(images[0],cv2.COLOR_RGB2GRAY);aligned=[images[0]]
    for im in images[1:]:
        warp=np.eye(2,3,dtype=np.float32)
        score,warp=cv2.findTransformECC(ref,cv2.cvtColor(im,cv2.COLOR_RGB2GRAY),warp,cv2.MOTION_EUCLIDEAN,(cv2.TERM_CRITERIA_COUNT|cv2.TERM_CRITERIA_EPS,80,1e-5))
        if score<.7: raise ValueError('多帧配准可靠性不足，未合成')
        aligned.append(cv2.warpAffine(im,warp,(shape[1],shape[0]),flags=cv2.INTER_LINEAR|cv2.WARP_INVERSE_MAP,borderMode=cv2.BORDER_REFLECT_101))
    return images[0],np.median(np.stack(aligned),axis=0)

def apply(current,operation,source,masks=None,allow_frames=False):
    name=operation['name'];p=operation['parameters'];region=operation['region']
    floating=np.issubdtype(current.dtype,np.floating)
    x=current.astype(np.float32)/(1 if floating else 255)
    mask=None
    if region is not None:
        if not masks or region not in masks: raise ValueError('此实验需要有效的分割区域')
        mask=np.asarray(masks[region],np.float32)
        if mask.shape!=x.shape[:2] or not np.isfinite(mask).all(): raise ValueError('蒙版与照片尺寸不匹配')
        mask=np.clip(mask,0,1)[...,None]
    metadata=dict(category='E',source_kind='RAW' if Path(source).suffix.lower() in RAW_EXTENSIONS else 'rendered_photo',pipeline_stage='linear RGB / display',generated=False)
    if name in RAW_NAMES or name=='multi_frame_median':
        if Path(source).suffix.lower() not in RAW_EXTENSIONS: raise ValueError('此效果需要原始RAW；JPEG/HEIC不能冒充传感器数据')
        metadata.update(category='R+E',pipeline_stage=name,composition='current + (RAW variant - RAW baseline); clipped to display range')
        if name=='multi_frame_median':
            if not allow_frames: raise ValueError('网页未提供多帧来源，不能执行中值消人')
            paths=[str(source)]+p['frames']
            if len(set(str(Path(q).resolve()) for q in paths))!=len(paths): raise ValueError('多帧来源不能重复')
            base,target=median_frames(paths,x.shape);metadata['source_frames']=paths
        else:
            with rawpy.imread(str(source)) as raw:
                # LibRaw处理后可能改变visible尺寸与CFA索引；先复制采样可视化。
                sensor=sites(raw,x.shape,p['scale']) if name=='sensor_sites' else None
                full=name in ('raw_half_detail','raw_demosaic_linear') or max(x.shape[:2])>max(raw.sizes.width,raw.sizes.height)//2
                base=develop(raw,output_shape=x.shape,half_size=not full);a=p.get('amount',1)
                def variant(**kw):
                    return develop(raw,output_shape=x.shape,**dict({'half_size':not full},**kw))
                if name=='sensor_sites': target=sensor
                elif name=='raw_wb_split':
                    warm=variant(use_camera_wb=False,user_wb=wb(raw,p['warmth']))
                    cool=variant(use_camera_wb=False,user_wb=wb(raw,p['outside_warmth']))
                    target=warm*mask+cool*(1-mask);mask=None
                elif name=='raw_demosaic_linear': target=variant(demosaic_algorithm=rawpy.DemosaicAlgorithm.LINEAR)
                elif name=='raw_half_detail': target=variant(half_size=True)
                elif name=='raw_noise_gain': target=variant(exp_shift=2**p['stops'])
                elif name=='raw_camera_color':
                    desc=raw.color_desc.decode('ascii').strip('\x00')
                    if desc[:3]!='RGB': raise ValueError('此相机原生通道排列尚未验证，不作错误色彩映射')
                    target=variant(output_color=rawpy.ColorSpace.raw,use_camera_wb=False,user_wb=[1,1,1,1])
                    metadata['display_note']='相机通道当作RGB编码的伪色显示，不是色度准确的sRGB转换；不保证发绿'
                elif name=='dual_development':
                    warm=variant(use_camera_wb=False,user_wb=wb(raw,p['warmth']),exp_shift=2**p['stops'])
                    cool=variant(use_camera_wb=False,user_wb=wb(raw,-p['warmth']),exp_shift=2**(-p['stops']))
                    target=warm*p['mix']+cool*(1-p['mix'])
                target=base+a*(target-base)
        y=x+(target-base)
        # 全图仍保留细节，不让源数据实验整体裁成白/黑。
        y=.15*x+.85*np.clip(y,0,1)
    elif name=='faded_fog':
        a=p['amount'];gray=np.sum(x*np.array([.2126,.7152,.0722]),axis=2,keepdims=True)
        faded=x*(1-.35*a)+gray*.35*a;y=faded*(1-.35*a)+.2*a
    elif name in ('linear_negative','local_linear_negative'): y=display(linear(x)*(1-p['amount'])+(1-linear(x))*p['amount'])
    elif name=='local_exposure_erase':
        if mask is None: raise ValueError('曝光消隐只用于局部区域')
        from media_effects import disappearance_mask
        mask=disappearance_mask(mask[:,:,0])[...,None]
        y=display(linear(x)*2**p['stops'])
        if mask.mean()>.85: y=.25*x+.75*y
        metadata['display_note']='后期线性曝光的输出裁剪；不改变原始传感器饱和状态，纯黑不凭空变白'
    else: raise ValueError('未知成像管线实验')
    if mask is not None: y=x*(1-mask)+y*mask
    y=np.clip(y,0,1).astype(np.float32)
    return (y if floating else np.round(y*255).astype(np.uint8)),metadata
