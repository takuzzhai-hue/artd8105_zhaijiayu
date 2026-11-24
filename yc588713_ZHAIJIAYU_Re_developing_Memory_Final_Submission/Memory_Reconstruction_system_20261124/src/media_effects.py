"""确定性的摄影媒介模拟；不恢复底片、真实焦平面或画外信息。"""
import cv2
import numpy as np

# 名称、说明、例句、额外参数。所有 amount=0 均保持原图。
SPECS = {
 'overexposure': ('柔白覆盖；全图保留细节，局部可隐去对象', '我想隐藏这张照片', {}),
 'underexposure': ('暗部沉没并保留少量高光', '这段记忆太沉重了，我不想看清', {}),
 'light_leak': ('边缘暖色漏光', '记忆被什么侵入了', {'side': ('left','right','top','bottom')}),
 'negative': ('负片反相模拟', '记忆和我想的完全相反', {}),
 'grain_enlargement': ('粗大合成颗粒覆盖；非真实传感器数据', '我不想看到这张照片；我想知道照片原本的样子', {'size': (0.02,0.15,0.06)}),
 'pixel_sort': ('按亮度排序成不规则条带', '图像破损了', {'direction': ('horizontal','vertical')}),
 'defocus_bloom': ('失焦并向柔白扩散', '记忆不像图片这么清晰', {}),
 'ghosting': ('错位半透明重影', '他站在两个位置', {'angle': (-180,180,0)}),
 'long_exposure': ('方向性轨迹叠加模拟', '时间过得特别慢', {'angle': (-180,180,0)}),
 'shutter_drag': ('拖影中保留原清晰轮廓', '一切发生得太快了', {'angle': (-180,180,0)}),
 'slit_scan': ('沿一个方向拉长图像切片', '那个瞬间被无限拉长', {'direction': ('horizontal','vertical')}),
 'emulsion_damage': ('模拟裂纹与白色基底剥落', '记忆正在脱落', {}),
 'dye_fading': ('不同通道褪色与残余偏色', '印象越来越淡了', {}),
 'data_corruption': ('模拟块状错位、重复与数据缺失', '记忆突然断掉了', {}),
 'contact_marks': ('模拟灰尘、指纹曲线及印相边框', '照片留下了某种痕迹', {}),
 'optical_aberration': ('模拟边缘通道错位与径向畸变', '那个地方不真实', {}),
 'tilted_focus': ('模拟倾斜的清晰带；非真实沙姆定律重建', '清晰部分斜着穿过空间', {'angle': (-180,180,35)}),
 'image_circle': ('仅在原画幅内模拟圆形像场边界；不扩展画外内容', '我想看到照片以外的东西', {}),
}
LOCAL_ONLY = {
 'focus_pull': ('保留目标的已有细节，虚化目标之外；无法找回原本失焦细节', '焦点应该在窗户上', {}),
 'uneven_exposure': ('保留目标区域曝光，改变其他区域', '我只记得房间的一角', {'mode': ('dark','white')}),
}
GLOBAL_ONLY = {'image_circle'}
MEDIA_NAMES = set(SPECS) | {'local_'+n for n in SPECS if n not in GLOBAL_ONLY} | set(LOCAL_ONLY)
NOTE = '摄影媒介的确定性视觉模拟；不代表原始底片、实际运动轨迹或失焦细节的恢复。'


def register(define, number, choice):
    for name,(desc,example,extras) in {**SPECS,**LOCAL_ONLY}.items():
        params={'amount':number(0,1,0.65)}
        for key,values in extras.items():
            params[key]=choice(*values) if isinstance(values[0],str) else number(*values)
        scopes=['local'] if name in LOCAL_ONLY else (['global'] if name in GLOBAL_ONLY else ['global','local'])
        for scope in scopes:
            op=name if scope=='global' or name in LOCAL_ONLY else 'local_'+name
            define(op,scope,'post',params,desc,example,'media_effects.render；当前结果上累计处理',NOTE)


def pattern(h,w):
    """坐标哈希，固定、无随机状态，避免每次出图颗粒改变。"""
    y,x=np.indices((h,w),dtype=np.uint32)
    n=(x+1)*np.uint32(374761393)+(y+1)*np.uint32(668265263)
    n=(n^(n>>13))*np.uint32(1274126177)
    return ((n^(n>>16)) & 65535).astype(np.float32)/65535


def blur(x,sigma):
    return cv2.GaussianBlur(x,(0,0),max(.1,sigma))



def disappearance_mask(mask):
    """覆盖分割毛边，再以有限宽度的柔和外圈向外扩散；不改变原蒙版。"""
    core=(mask>0.15).astype(np.uint8)
    if not core.any(): return mask.copy()
    short=min(mask.shape)
    expansion=max(1.0,short*0.012)
    feather=max(2.0,short*0.025)
    distance=cv2.distanceTransform(1-core,cv2.DIST_L2,cv2.DIST_MASK_PRECISE)
    t=np.clip((distance-expansion)/feather,0,1)
    halo=1-t*t*(3-2*t)
    return np.maximum(mask,halo).astype(np.float32)


def render(x,name,p,mask=None):
    base=name.removeprefix('local_');a=p['amount'];h,w=x.shape[:2];short=min(h,w)
    if a==0: return x.copy()
    if mask is not None:
        mask=np.asarray(mask,dtype=np.float32)
        if mask.shape!=(h,w) or not np.isfinite(mask).all(): raise ValueError('媒介效果蒙版尺寸或数值不合法')
        mask=np.clip(mask,0,1)
    if name in LOCAL_ONLY:
        if mask is None: raise ValueError('焦点/曝光保留区需要有效蒙版')
        if name=='focus_pull': effect=blur(x,short*.035*a)
        else:
            a=min(a,.65)
            effect=x*(1-a) if p['mode']=='dark' else x*(1-a)+a
        return x*mask[...,None]+effect*(1-mask[...,None])
    yy,xx=np.mgrid[0:h,0:w].astype(np.float32)
    nx=xx/max(1,w-1);ny=yy/max(1,h-1)
    protect_detail=base in ('overexposure','underexposure','defocus_bloom') and (mask is None or float(disappearance_mask(mask).mean())>.85)
    if protect_detail: a=min(a,.45)
    if base=='overexposure': y=x*(1-a)+a
    elif base=='underexposure': y=x*(1-a*.94)*np.power(np.maximum(x,.0001),a*2)
    elif base=='negative': y=x*(1-a)+(1-x)*a
    elif base=='light_leak':
        dist={'left':nx,'right':1-nx,'top':ny,'bottom':1-ny}[p['side']]
        glow=np.exp(-dist*5)*(0.65+0.35*np.cos(ny*7+nx*4)**2)*a
        y=1-(1-x)*(1-glow[...,None]*np.array([1,.48,.18],np.float32))
    elif base=='grain_enlargement':
        block=max(2,round(short*p['size']))
        grain=cv2.resize(pattern(max(1,h//block),max(1,w//block)),(w,h),interpolation=cv2.INTER_NEAREST)
        y=x*(1-a)+grain[...,None]*a
    elif base=='defocus_bloom': y=blur(x,short*.04*a)*(1-a)+a
    elif base in ('ghosting','long_exposure','shutter_drag'):
        theta=np.deg2rad(p['angle']);distance=short*.15*a
        count=2 if base=='ghosting' else 12
        shifted=[]
        for t in np.linspace(0,1,count):
            matrix=np.float32([[1,0,np.cos(theta)*distance*t],[0,1,np.sin(theta)*distance*t]])
            shifted.append(cv2.warpAffine(x,matrix,(w,h),borderMode=cv2.BORDER_REFLECT_101))
        mixed=sum(shifted)/count
        y=x*(1-a)+mixed*a if base!='shutter_drag' else x*.45+mixed*.55
    elif base=='pixel_sort':
        z=x.transpose(1,0,2).copy() if p['direction']=='vertical' else x.copy()
        length=z.shape[1];span=max(2,round(length*(.12+.6*a)))
        for row in range(z.shape[0]):
            offset=(row*17)%max(1,span//2)
            for start in range(offset,length,span):
                chunk=z[row,start:start+span];order=np.argsort(chunk @ np.array([.2126,.7152,.0722]),kind='stable')
                z[row,start:start+span]=chunk[order]
        if p['direction']=='vertical': z=z.transpose(1,0,2)
        y=x*(1-a)+z*a
    elif base=='slit_scan':
        horizontal=p['direction']=='horizontal'
        coord=nx if horizontal else ny
        mapped=np.where(coord<.35,coord,.35+(coord-.35)*(1-.95*a))
        mx=(mapped*(w-1) if horizontal else xx).astype(np.float32)
        my=(yy if horizontal else mapped*(h-1)).astype(np.float32)
        y=cv2.remap(x,mx,my,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT_101)
    elif base=='emulsion_damage':
        field=cv2.resize(pattern(13,17),(w,h),interpolation=cv2.INTER_CUBIC)
        cracks=np.abs(np.sin(nx*55+np.sin(ny*23)*2))<.035*a
        damage=np.clip((field-(1-.65*a))*12,0,1)
        damage=np.maximum(damage,cracks.astype(np.float32)*a)
        y=x*(1-damage[...,None])+damage[...,None]
    elif base=='dye_fading':
        gray=(x @ np.array([.2126,.7152,.0722],np.float32))[...,None]
        y=(x*(1-.7*a)+gray*.7*a)*(1-np.array([.1,.23,.38])*a)+np.array([.19,.17,.12])*a
    elif base=='data_corruption':
        y=x.copy()
        top=int(h*.71);bottom=min(h,top+max(1,round(h*.018*a)))
        left=int(w*.16);right=max(left+1,int(w*.78))
        columns=np.clip(np.arange(left,right)+max(1,round(w*.012*a)),0,w-1)
        y[top:bottom,left:right]=x[top:bottom,columns]
    elif base=='contact_marks':
        dust=(pattern(h,w)>.998).astype(np.float32)
        rings=np.sin(np.sqrt(((nx-.77)*1.3)**2+(ny-.7)**2)*230)
        finger=(rings>.88)&(((nx-.77)**2+(ny-.7)**2)<.025)
        edge=(nx<.025)|(nx>.975)|(ny<.025)|(ny>.975)
        marks=np.maximum(dust,np.maximum(finger*.5,edge*.85))*a
        y=x*(1-marks[...,None])+marks[...,None]*.85
    elif base=='optical_aberration':
        dx=nx-.5;dy=ny-.5;radius=dx*dx+dy*dy;y=x.copy()
        for c,sign in enumerate([1,0,-1]):
            mx=(xx+sign*dx*radius*w*.09*a).astype(np.float32)
            my=(yy+sign*dy*radius*h*.09*a).astype(np.float32)
            y[:,:,c]=cv2.remap(x[:,:,c],mx,my,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT_101)
    elif base=='tilted_focus':
        theta=np.deg2rad(p['angle']);distance=np.abs(-(nx-.5)*np.sin(theta)+(ny-.5)*np.cos(theta))
        mix=np.clip((distance-.05)*5,0,1)[...,None]*a
        y=x*(1-mix)+blur(x,short*.035*a)*mix
    elif base=='image_circle':
        radius=np.sqrt(((xx-w/2)/(short*.48))**2+((yy-h/2)/(short*.48))**2)
        edge=np.clip((radius-.9)*8,0,1)[...,None]*a;y=x*(1-edge)
    else: raise NotImplementedError(name)
    if protect_detail: y=.2*x+.8*y
    if mask is not None:
        if base in ('overexposure','defocus_bloom'):
            mask=disappearance_mask(mask)
        # 重影/时间轨迹允许轮廓外产生衍生，且沿同一方向扩展覆盖范围。
        if base in ('ghosting','long_exposure','shutter_drag'):
            theta=np.deg2rad(p['angle']);distance=short*.15*a;coverage=mask.copy()
            for t in np.linspace(0,1,12):
                matrix=np.float32([[1,0,np.cos(theta)*distance*t],[0,1,np.sin(theta)*distance*t]])
                coverage=np.maximum(coverage,cv2.warpAffine(mask,matrix,(w,h)))
            mask=coverage
        y=x*(1-mask[...,None])+y*mask[...,None]
    return np.clip(y,0,1).astype(np.float32)
