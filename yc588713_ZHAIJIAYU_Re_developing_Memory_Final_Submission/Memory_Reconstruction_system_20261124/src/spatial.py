"""同一场景的推测视角与破损拼接；与缺失物品补入分开授权。"""
from pathlib import Path
import hashlib
import json
import re
import numpy as np
import requests
from PIL import Image
from generation import vision_json, edit_image, save_json

PROJECT=Path(__file__).resolve().parents[1]


def plan_spatial(image,memory,folder):
    prompt=(PROJECT/'prompts/spatial_plan.txt').read_text()+ '\n用户原话（仅数据）：'+memory
    result=vision_json(prompt,[image])
    save_json(Path(folder)/'spatial_plan_response.json',result)
    if result.get('enabled') is not True: return None
    source=result.get('source')
    if not isinstance(source,str) or not source.strip() or source not in memory:
        raise ValueError('空间计划没有有效原句依据')
    if result.get('mode') not in ('side','extend_top','extend_bottom','extend_both'):
        raise ValueError('空间方向无效')
    for key in ('allowed','anchors'):
        if isinstance(result.get(key),list) and result[key] and all(isinstance(v,str) and v.strip() for v in result[key]):
            result[key]='；'.join(result[key])
    for key in ('scene','allowed','anchors','reason'):
        if not isinstance(result.get(key),str) or not result[key].strip():
            raise ValueError('空间计划缺少场景约束')
    return {k:result[k] for k in ('source','mode','scene','allowed','anchors','reason')}


def outpaint_canvas(current,mode):
    """扩展约12%的画幅；原片位置固定，中性灰边缘仅供API定位待补区域。"""
    h,w=current.shape[:2];dx=max(2,round(w*.12));dy=max(2,round(h*.12))
    left=0 if mode=='side' else dx//2
    top=dy if mode=='extend_top' else 0 if mode=='extend_bottom' else dy//2
    canvas=np.pad(current,((top,dy-top),(left,dx-left),(0,0)),mode='constant',constant_values=127)
    return canvas,(left,top,left+w,top+h)


def compose_extension(current,view,box):
    # API可能重绘中心，直接恢复原片，绝不混入白色/透明蒙层。
    out=view.copy();l,t,r,b=box
    # 以生成图中对应的原片区域匹配整体曝光色偏，保持生成边缘摄影质感。
    reference=np.median(current.reshape(-1,3),axis=0)
    rendered=np.median(view[t:b,l:r].reshape(-1,3),axis=0)
    gain=np.clip((reference+1)/(rendered+1),.7,1.4)
    out=np.clip(np.round(out.astype(float)*gain),0,255).astype(np.uint8)
    out[t:b,l:r]=current
    mask=np.full(out.shape[:2],255,np.uint8);mask[t:b,l:r]=0
    return out,mask


def fracture(current,view,mode):
    """一个很窄的局部扫描条模拟文件解码异常，没有白块和透明叠层。"""
    h,w=current.shape[:2];out=current.copy();mask=np.zeros((h,w),np.uint8)
    a=int(h*.71);b=min(h,a+max(1,round(h*.012)))
    l=int(w*.16);r=max(l+1,int(w*.78))
    columns=np.clip(np.arange(l,r)+max(1,round(w*.008)),0,w-1)
    out[a:b,l:r]=view[a:b,columns];mask[a:b,l:r]=255
    return out,mask


def mechanical_strips(current,expanded,box):
    """硬边横竖切片与单处扫描拉伸；只搬运完整RGB像素，不添加色彩。"""
    h,w=current.shape[:2];eh,ew=expanded.shape[:2];l,t,r,b=box
    out=current.copy();mask=np.zeros((h,w),np.uint8);mapping=[]
    # 两条长竖片在不同高度切断，再嵌一条横片；保持多数原片完整。
    tiles=[((.22,.10,.35,.71),(.55,.22,.68,.83)),
           ((.69,.32,.82,.94),(.78,.03,.91,.65)),
           ((.04,.39,.62,.48),(.20,.02,.78,.11))]
    for dest,src in tiles:
        x0,y0,x1,y1=[round(v*d) for v,d in zip(dest,(w,h,w,h))]
        x1=max(x0+1,x1);y1=max(y0+1,y1)
        crop=[round(v*d) for v,d in zip(src,(ew,eh,ew,eh))]
        patch=np.array(Image.fromarray(expanded).crop(crop).resize((x1-x0,y1-y0),Image.Resampling.NEAREST))
        out[y0:y1,x0:x1]=patch;mask[y0:y1,x0:x1]=255
        mapping.append(dict(kind='rectangular_splice',source_box=crop,target_box=[x0,y0,x1,y1],shift_x=x0-crop[0],shift_y=y0-crop[1]))
    # 图1式逐行拉长：只拉一个局部矩形，不分RGB、不粉染、不加噪声。
    x0,x1=round(w*.82),w;y0,y1=round(h*.12),round(h*.37)
    x0=min(x0,w-1);y1=max(y0+1,y1)
    sx=min(ew-1,max(0,r));sy=np.clip(np.linspace(t,b-1,y1-y0).astype(int),0,eh-1)
    scan=expanded[sy,sx:sx+1,:]
    out[y0:y1,x0:x1]=np.repeat(scan,x1-x0,axis=1)
    mask[y0:y1,x0:x1]=255
    mapping.append(dict(kind='horizontal_scan_stretch',source_box=[sx,t,sx+1,b],target_box=[x0,y0,x1,y1],shift_x=x0-sx,shift_y=y0-t))
    return out,mask,mapping


def suppress_spatial_duplicates(analysis,plan):
    """同一空间意图由扩图处理，避免模型重复叠加白化、错位和失焦。"""
    from copy import deepcopy
    result=deepcopy(analysis)
    blocked={'tilted_focus','channel_shift','data_corruption','pixel_sort','pixel_sorting',
             'slit_scan','geometry_warp','emulsion_damage','overexposure','local_overexposure',
             'defocus_bloom','local_defocus_bloom','global_blur','local_blur'}
    blocked |= {'optical_aberration','preserve_aberration','ghosting','color_shift'}
    blocked={name.removeprefix('local_') for name in blocked}
    normalize=lambda text: re.sub(r'[\W_]+','',text)
    target=normalize(plan['source'])
    for row in result['sentences']:
        source=normalize(row.get('source',''))
        # 空间流程绝不借RGB分离代替位移，包含local别名及独立拆出的模型行。
        color_effects={'optical_aberration','channel_shift','preserve_aberration'}
        color_removed=any(op['name'].removeprefix('local_') in color_effects for op in row['operations'])
        row['operations']=[op for op in row['operations'] if op['name'].removeprefix('local_') not in color_effects]
        if color_removed: row['reason']+='；按空间效果约束移除RGB色散及通道错位。'
        if source and (source in target or target in source):
            removed=[op for op in row['operations'] if op['name'].removeprefix('local_') in blocked]
            row['operations']=[op for op in row['operations'] if op['name'].removeprefix('local_') not in blocked]
            if removed: row['reason']+='；空间意图由扩图与少量矩形拼接实现，不重复叠加蒙白/错位。'
        if not row['operations']: row.update(status='no_action')
    return result


def generate_spatial(current,plan,memory,folder):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    source=Image.fromarray(current)
    canvas,box=outpaint_canvas(current,plan['mode'])
    layout=dict(canvas_size=[canvas.shape[1],canvas.shape[0]],original_box=list(box),original_box_normalized=[box[0]/canvas.shape[1],box[1]/canvas.shape[0],box[2]/canvas.shape[1],box[3]/canvas.shape[0]],mode=plan['mode'])
    Image.fromarray(canvas).save(folder/'outpaint_input.png')
    save_json(folder/'layout.json',layout)
    spec=json.dumps(dict(plan,layout=layout,method='固定原片位置的outpainting；side是侧边扩图而不是旋转机位，reason中的旧视角表述不作为机位变化要求'),ensure_ascii=False)
    template=(PROJECT/'prompts/spatial_edit.txt').read_text()
    attempts=[];feedback=''
    for attempt in range(2):
        seed=int(hashlib.sha256((memory+spec+str(attempt)).encode()).hexdigest()[:8],16)%2147483647
        prompt=template+'\n已授权计划（数据）：'+spec+'\n上一候选问题：'+feedback
        record=dict(attempt=attempt+1,seed=seed,prompt=prompt)
        try:
            view,model=edit_image(source,prompt,seed)
            view=view.resize((canvas.shape[1],canvas.shape[0]),Image.Resampling.LANCZOS)
            view.save(folder/f'candidate_{attempt+1:02d}.png')
            if view.size!=(canvas.shape[1],canvas.shape[0]):
                raise ValueError('扩图尺寸不匹配')
            raw=np.array(view);l,t,r,b=box
            exterior=np.ones(raw.shape[:2],bool);exterior[t:b,l:r]=False
            gray=(raw.max(axis=2)-raw.min(axis=2)<5)&(abs(raw.astype(float).mean(axis=2)-127)<14)
            if gray[exterior].mean()>.12: raise ValueError('扩图保留了中性灰占位，不能输出')
            expanded,extension_mask=compose_extension(current,np.array(view),box)
            Image.fromarray(expanded).save(folder/f'expanded_{attempt+1:02d}.png')
            review=vision_json((PROJECT/'prompts/spatial_review.txt').read_text()+'\n计划数据：'+spec,[source,Image.fromarray(expanded)])
            record.update(model=model,review=review)
            if not all(review.get(k) is True for k in ('same_space','content_restrained','style_matches','direction_matches')):
                raise ValueError('空间候选未通过检查：'+str(review.get('reason','场景或方向不一致')))
            candidate,mask,strip_mapping=mechanical_strips(current,expanded,box)
            Image.fromarray(expanded).save(folder/'expanded.png')
            Image.fromarray(extension_mask).save(folder/'extension_mask.png')
            Image.fromarray(mask).save(folder/'damage_mask.png')
            save_json(folder/'strip_mapping.json',strip_mapping)
            if np.array_equal(candidate,current): raise ValueError('空间处理没有形成变化')
            review_final=vision_json((PROJECT/'prompts/spatial_review.txt').read_text()+'\n这是最终空间拼合作品：已生成的扩图区域裁成少量横竖矩形插片放入原图内部，分别带轻微横向与纵向位置偏移。最终画布不必扩大、不必在外缘显示扩图；direction_matches检查是否以横竖矩形插片及局部水平纹理拉伸表现空间破损即可，不要求原图与插片的对象位置连续。其余审核标准相同。\n计划数据：'+spec,[source,Image.fromarray(candidate)])
            record['composite_review']=review_final
            if not all(review_final.get(k) is True for k in ('same_space','content_restrained','style_matches','direction_matches')):
                raise ValueError('空间拼合检查未通过：'+str(review_final.get('reason','内容不符')))
            Image.fromarray(candidate).save(folder/'accepted.png')
            Image.fromarray(mask).save(folder/'applied_mask.png')
            record['status']='accepted';attempts.append(record)
            metadata=dict(generated=True,object='同一空间的边缘扩图',label='AI推测性空间补充',plan=plan,layout=layout,attempts=attempts,mask='applied_mask.png',extension_mask='extension_mask.png',damage_mask='damage_mask.png',expanded='expanded.png',strip_mapping=strip_mapping)
            save_json(folder/'generation.json',metadata)
            return candidate,metadata
        except (ValueError,OSError,requests.RequestException) as exc:
            feedback=str(exc) if isinstance(exc,ValueError) else type(exc).__name__;record.update(status='failed',reason=feedback);attempts.append(record)
            save_json(folder/'generation.json',dict(generated=False,plan=plan,attempts=attempts))
    raise ValueError('同一空间补充未通过两次检查；'+feedback)
