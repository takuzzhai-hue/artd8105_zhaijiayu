"""网页生成采用略微明显但克制的摄影调整；保留模型原提案供对照。"""
from copy import deepcopy
import re
LIMITS={'exposure':{'stops':(-.25,.25)},'white_balance':{'amount':(-.10,.10)},
'saturation':{'amount':(-.18,.18)},'contrast':{'amount':(-.25,.25)},
'color_shift':{'degrees':(-4,4)},'lift_blacks':{'amount':(0,.10)},
'vignette':{'amount':(0,.16)},'global_blur':{'amount':(0,.05)},
'local_blur':{'amount':(0,.08)},'motion_blur':{'amount':(0,.14)},
'local_brighten':{'stops':(0,.25)},'local_glow':{'stops':(0,.25),'halo':(0,.10)},
'local_sharpen':{'amount':(0,.16)},
'overexposure':{'amount':(0,.45)},'underexposure':{'amount':(0,.45)},
'defocus_bloom':{'amount':(0,.45)}}

for local,global_name in [('local_white_balance','white_balance'),('local_saturation','saturation'),('local_contrast','contrast'),('local_exposure','exposure')]:
    LIMITS[local]=deepcopy(LIMITS[global_name])

def gentle_analysis(analysis):
    result=deepcopy(analysis)
    used=set()
    text='，'.join(row.get('source','') for row in result['sentences'])
    mild_dark=bool(re.search(r'(?:暗|压暗)(?:一?点(?:点)?|一些)|(?:稍微|略微|轻微).{0,5}暗|\b(?:slightly|a little|a bit)\s+darker\b',text,re.I))
    for row in result['sentences']:
        selected=[]
        for op in row['operations']:
            if mild_dark:
                base=op['name'].removeprefix('local_')
                if base=='underexposure' or (base=='exposure' and op['parameters'].get('stops',0)<0):
                    op['name']='local_exposure' if op.get('region') else 'exposure'
                    op['parameters']={'stops':-.25}
                    row['reason']+='；轻微变暗只使用−0.25EV曝光，不使用暗部沉没。'
                if base=='vignette' and not any(word in text.lower() for word in ('暗角','四周暗','边缘暗')):
                    continue
                if base=='contrast':
                    if not any(word in text.lower() for word in ('对比','反差','contrast')): continue
                    op['parameters']['amount']=max(-.25,min(.25,op['parameters']['amount']))
            key=(op['name'],op['region'],op['parameters'].get('request_id'))
            if key in used: continue  # 不在同一次生成中重复叠加相同效果。
            used.add(key)
            for param,(lo,hi) in LIMITS.get(op['name'],{}).items():
                op['parameters'][param]=max(lo,min(hi,op['parameters'][param]))
            selected.append(op)
        row['operations']=selected
        if row['status']=='proposed' and not selected:
            row['status']='no_action';row['reason']+='；相同区域效果已提出，本轮不重复叠加。'
    return result


def expand_media_stages(analysis):
    """少于三项时，把媒介变化拆为渐进阶段，仍逐步处理上一张结果。"""
    from media_effects import MEDIA_NAMES
    result=deepcopy(analysis)
    count=sum(len(row['operations']) for row in result['sentences'])
    if count>=3: return result
    for row in result['sentences']:
        for index,op in enumerate(row['operations']):
            if op['name'] in ('overexposure','underexposure','defocus_bloom'): continue
            if op['name'] not in MEDIA_NAMES or op['parameters']['amount']<=0: continue
            steps=4-count
            expanded=[]
            for i in range(steps):
                stage=deepcopy(op)
                stage['parameters']['amount']=op['parameters']['amount']*(i+1)/steps
                expanded.append(stage)
            row['operations'][index:index+1]=expanded
            row['reason']+='；此媒介效果拆成渐进阶段，各阶段在上一结果上继续处理。'
            return result
    return result
