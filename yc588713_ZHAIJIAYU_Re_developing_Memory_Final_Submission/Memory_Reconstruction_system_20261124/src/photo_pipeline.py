"""照片→视觉观察→文字分析→受支持效果预览；不是最终 RAW 显影引擎。"""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import argparse
import json
import os
import numpy as np
import cv2
import requests
import rawpy
from PIL import Image
from vision import prepare_image, inspect_image
from analyze_memory import analyze
from segmentation import segment_regions
from generation import plan_additions, attach_additions, generate_addition
from style import gentle_analysis, expand_media_stages
from spatial import plan_spatial, generate_spatial, suppress_spatial_duplicates
from media_effects import MEDIA_NAMES, render, NOTE
from pipeline_effects import NAMES as PIPELINE_NAMES, RAW_NAMES, apply as apply_pipeline
from develop_test import RAW_EXTENSIONS
from poetic_effects import NAMES as POETIC_NAMES, apply as apply_poetic
from perceptual_effects import NAMES as PERCEPTUAL_NAMES, apply as apply_perceptual

PROJECT = Path(__file__).resolve().parents[1]
SUPPORTED = {'contrast', 'saturation', 'global_blur', 'lift_blacks', 'vignette', 'pixelate', 'color_shift', 'motion_blur', 'local_blur', 'local_brighten', 'local_sharpen', 'local_glow', 'exposure', 'white_balance', 'local_white_balance','local_saturation','local_contrast','local_exposure'}

SUPPORTED |= MEDIA_NAMES
SUPPORTED.add('noise_emphasis')


def apply_preview(image, operation, masks=None):
    """只实现明确的显示 RGB 全局效果；其余操作明确报告未执行。"""
    name, params = operation['name'], operation['parameters']
    if name not in SUPPORTED:
        raise NotImplementedError('此操作尚未接入预览处理器，需要 RAW 引擎或局部蒙版支持')
    name = {'local_white_balance':'white_balance','local_saturation':'saturation','local_contrast':'contrast','local_exposure':'exposure'}.get(name,name)
    is_float = np.issubdtype(image.dtype, np.floating)
    x = image.astype(np.float32) / (1 if is_float else 255)
    amount = params.get('amount', 0)
    h, w = x.shape[:2]
    original = x.copy()
    if operation.get('region') is not None:
        if not masks or operation['region'] not in masks:
            raise NotImplementedError('没有可用的定位蒙版')
    if name in MEDIA_NAMES:
        mask = masks[operation['region']] if operation.get('region') is not None else None
        result = render(x, name, params, mask)
        return result if is_float else np.round(result*255).astype(np.uint8)
    if name in ('exposure', 'local_brighten', 'local_glow'):
        linear = np.where(x <= 0.04045, x/12.92, ((x+0.055)/1.055)**2.4)
        linear *= 2**params['stops']
        x = np.where(linear <= 0.0031308, linear*12.92, 1.055*np.maximum(linear,0)**(1/2.4)-0.055)
    elif name == 'white_balance':
        x *= np.array([2**amount,1,2**(-amount)],dtype=np.float32)
    elif name == 'motion_blur':
        size = 1 + round(amount*min(h,w)*0.05)
        size = max(1, size | 1)
        kernel = np.zeros((size,size), np.float32)
        center = size//2
        angle = np.deg2rad(params['angle'])
        dx,dy = int(round(center*np.cos(angle))),int(round(center*np.sin(angle)))
        cv2.line(kernel,(center-dx,center-dy),(center+dx,center+dy),1,1)
        kernel /= kernel.sum()
        x = cv2.filter2D(x,-1,kernel)
    elif name == 'local_blur' and amount>0:
        x = cv2.GaussianBlur(x,(0,0),amount*0.02*min(h,w))
    elif name == 'local_sharpen':
        x += 2*amount*(x-cv2.GaussianBlur(x,(0,0),max(0.5,min(h,w)*0.001)))
    elif name == 'noise_emphasis':
        # 增强照片现有的细颗粒/高频残差，不凭空声称恢复传感器噪声。
        x += amount*(x-cv2.GaussianBlur(x,(0,0),.7))
    elif name == 'contrast':
        x = (x - 0.5) * 2 ** (2 * amount) + 0.5
    elif name in ('saturation', 'color_shift'):
        hsv = cv2.cvtColor(x, cv2.COLOR_RGB2HSV)
        if name == 'saturation': hsv[:,:,1] = np.clip(hsv[:,:,1] * (1 + amount), 0, 1)
        else: hsv[:,:,0] = (hsv[:,:,0] + params['degrees']) % 360
        x = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
    elif name == 'global_blur' and amount > 0:
        x = cv2.GaussianBlur(x, (0,0), amount * 0.02 * min(h,w))
    elif name == 'lift_blacks':
        x = x * (1 - 0.25*amount) + 0.25*amount
    elif name == 'vignette':
        yy, xx = np.mgrid[-1:1:complex(h), -1:1:complex(w)]
        x *= (2 ** (-2*amount*(xx*xx+yy*yy)/2))[:,:,None]
    elif name == 'pixelate' and amount > 0:
        block = 1 + round(amount*min(h,w)/32)
        x = cv2.resize(cv2.resize(x, (max(1,w//block),max(1,h//block)), interpolation=cv2.INTER_AREA), (w,h), interpolation=cv2.INTER_NEAREST)
    if operation.get('region') is not None:
        mask = masks[operation['region']][:,:,None]
        if name == 'local_glow':
            delta = np.maximum(x-original,0)*mask
            x = original + delta + params['halo']*cv2.GaussianBlur(delta,(0,0),max(1,min(h,w)*0.02))
        else:
            x = original*(1-mask)+x*mask
    x = np.clip(x,0,1)
    return x.astype(np.float32) if is_float else np.round(x*255).astype(np.uint8)


def run_stream(photo, memory, output_dir=None, observation_override=None):
    if not memory.strip(): raise ValueError('请先输入文字')
    image = prepare_image(photo)
    folder = Path(output_dir) if output_dir is not None else PROJECT / 'outputs' / datetime.now(ZoneInfo('Asia/Shanghai')).strftime('%Y%m%d_%H%M%S_%f')
    folder.mkdir(parents=True, exist_ok=False)
    image.save(folder / 'original_preview.png')
    yield dict(kind='progress',status='正在看图并理解回忆…')
    observation = inspect_image(image, memory, diagnostics_path=folder/"vision_diagnostics.json") if observation_override is None else observation_override
    yield dict(kind='progress',status='正在检查原话是否明确提及画面中缺失的对象…')
    additions=[]
    addition_diagnostics={}
    try:
        additions=plan_additions(image,memory,folder)
        plan_file=folder/'addition_plan.json'
        if plan_file.exists(): addition_diagnostics=json.loads(plan_file.read_text())
        if additions:
            yield dict(kind='progress',status='已识别需要补入：'+'、'.join(p['object'] for p in additions)+'；将作为独立步骤制作。')
        else:
            summaries=[a.get('summary','') for a in addition_diagnostics.get('audit',[]) if a.get('summary')]
            if summaries: yield dict(kind='progress',status='补物判断：'+str(summaries[-1])[:240])
    except Exception as exc:
        addition_diagnostics=dict(status='error',error=str(exc) if isinstance(exc,ValueError) else type(exc).__name__)
        (folder/'addition_plan_error.json').write_text(json.dumps(addition_diagnostics,ensure_ascii=False),encoding='utf-8')
        yield dict(kind='progress',status='补物分析暂未完成：'+addition_diagnostics['error']+'；继续其他可执行效果。')
    observation['approved_additions']=additions
    spatial_plan=None
    try:
        spatial_plan=plan_spatial(image,memory,folder)
    except (ValueError,requests.RequestException,OSError) as exc:
        (folder/'spatial_plan_error.json').write_text(json.dumps(dict(error=str(exc) if isinstance(exc,ValueError) else type(exc).__name__),ensure_ascii=False))
    observation['spatial_plan']=spatial_plan
    (folder/'observation.json').write_text(json.dumps(observation,ensure_ascii=False,indent=2),encoding='utf-8')
    yield dict(kind='progress',status='正在识别需要修改的局部轮廓…')
    masks, segmentation = segment_regions(image, observation['regions'], folder)
    observation['segmentation'] = segmentation
    source_capabilities=dict(is_raw=Path(photo).suffix.lower() in RAW_EXTENSIONS,frame_count=1)
    observation['source_capabilities']=source_capabilities
    (folder/'observation.json').write_text(json.dumps(observation,ensure_ascii=False,indent=2),encoding='utf-8')
    yield dict(kind='progress',status='正在制定逐步修改计划…')
    try:
        proposed_analysis = analyze(memory, regions=list(masks), observation=observation, diagnostics_dir=folder)
    except (ValueError,requests.RequestException) as exc:
        if not additions: raise
        # 普通调色分析失败不能抹掉独立看图审核已通过的补物计划。
        proposed_analysis={'sentences':[dict(source=memory,intent='普通效果分析',status='unavailable',reason='普通效果分析失败，保留独立审核通过的补物步骤：'+(str(exc) if isinstance(exc,ValueError) else type(exc).__name__),operations=[])]}
    # 在出图前自查一次；修复失败区域/遗漏目标，不重复执行已经做过的图像效果。
    failed=[r for r in segmentation if r['status']!='success']
    missing=[r for r in proposed_analysis['sentences'] if r['status']=='missing']
    if failed or missing:
        yield dict(kind='progress',status='正在自查未定位区域，重新观察并尝试修复…')
        repair_dir=folder/'repair_01';repair_dir.mkdir()
        try:
            repaired=inspect_image(image,memory,diagnostics_path=repair_dir/'vision_diagnostics.json',
                repair_context=dict(failed_regions=failed,missing_intents=missing))
            repaired_masks,repaired_records=segment_regions(image,repaired['regions'],repair_dir)
            # 有效旧蒙版保留，新蒙版按名称更新；失败不抹去旧成果。
            masks.update(repaired_masks)
            for item in repaired_records:
                for key in ('mask_file','overlay_file'):
                    if key in item: item[key]='repair_01/'+item[key]
            good={r['name']:r for r in segmentation if r['status']=='success'}
            good.update({r['name']:r for r in repaired_records if r['status']=='success'})
            segmentation=list(good.values())+[r for r in repaired_records if r['status']!='success' and r['name'] not in good]
            observation=repaired;observation['segmentation']=segmentation
            observation['approved_additions']=additions
            observation['spatial_plan']=spatial_plan
            observation['source_capabilities']=source_capabilities
            proposed_analysis=analyze(memory,regions=list(masks),observation=observation,diagnostics_dir=repair_dir)
            (folder/'observation.json').write_text(json.dumps(observation,ensure_ascii=False,indent=2),encoding='utf-8')
        except Exception as exc:
            (repair_dir/'repair_error.json').write_text(json.dumps(dict(error=str(exc) if isinstance(exc,ValueError) else type(exc).__name__),ensure_ascii=False),encoding='utf-8')
    if spatial_plan:
        proposed_analysis=suppress_spatial_duplicates(proposed_analysis,spatial_plan)
    analysis = expand_media_stages(gentle_analysis(attach_additions(proposed_analysis, additions, memory)))
    # 空间变化放在已定位局部操作之后，避免沿用错位前的蒙版。
    if spatial_plan:
        analysis['sentences'].append(dict(source=spatial_plan['source'],intent='同一空间扩图与轻微文件破损',status='proposed',reason=spatial_plan['reason']+'；AI推测性空间补充',operations=[dict(name='spatial_reconstruction',parameters={'mode':spatial_plan['mode']},region=None)]))
    yield dict(kind='plan',total=max(1,sum(len(row['operations']) for row in analysis['sentences'])))
    # 普通效果可交给 RAW 引擎；generate_add 需网页流程的授权计划及审核。区域路径相对此 JSON。
    engine_input = dict(regions={r['name']:r['mask_file'] for r in segmentation if r['status']=='success'},
        operations=[dict(source=row['source'], **op) for row in analysis['sentences'] for op in row['operations']])
    (folder/'engine_operations.json').write_text(json.dumps(engine_input,ensure_ascii=False,indent=2),encoding='utf-8')
    current = np.array(image)
    log = []
    for row in analysis['sentences']:
        if row['status'] != 'proposed':
            log.append(dict(source=row['source'], status=row['status'], reason=row['reason']))
        for operation in row['operations']:
            record = dict(source=row['source'], operation=operation, interpretation=row['reason'],
                          simulated=operation['name'] in MEDIA_NAMES)
            try:
                if operation['name']=='spatial_reconstruction':
                    if spatial_plan is None: raise ValueError('没有已授权的空间计划')
                    yield dict(kind='progress',status='正在扩展同一空间，并检查边缘内容与轻微文件破损效果…')
                    candidate,metadata=generate_spatial(current,spatial_plan,memory,folder/'spatial_generation')
                    record.update(generated=True,generation=metadata)
                elif operation['name']=='generate_add':
                    plan=next(p for p in additions if p['id']==operation['parameters']['request_id'])
                    yield dict(kind='progress',status=f'正在补入「{plan["object"]}」并进行AI自查；不合格会重试一次…')
                    candidate,metadata=generate_addition(current,plan,memory,folder/('generation_'+plan['id']))
                    record.update(generated=True,generation=metadata)
                elif operation['name'] in POETIC_NAMES:
                    candidate,metadata=apply_poetic(current,operation,masks,photo,folder/('effect_'+str(len(log)+1)))
                    record['pipeline']=metadata
                    record['simulated']=True
                elif operation['name'] in PERCEPTUAL_NAMES:
                    candidate,metadata=apply_perceptual(current,operation,masks,photo,folder/('effect_'+str(len(log)+1)))
                    record['pipeline']=metadata
                    record['simulated']=True
                elif operation['name'] in PIPELINE_NAMES:
                    candidate,metadata=apply_pipeline(current,operation,photo,masks)
                    record['pipeline']=metadata
                else:
                    candidate = apply_preview(current, operation, masks)
                if np.array_equal(candidate,current): raise ValueError('此操作没有产生像素变化，将交给本地兜底补充')
                current=candidate
                filename = f'step_{len(log)+1:02d}.png'
                Image.fromarray(current).save(folder / filename)
                record.update(status='success', image=filename, reason='已应用于缩小的 8 位显示预览；不是全尺寸 RAW 成片' + ('；'+NOTE if operation['name'] in MEDIA_NAMES else ''))
                if 'pipeline' in record:
                    record['category']=record['pipeline']['category']
                    record['reason']+='；'+record['pipeline'].get('display_note','源数据参与方式见pipeline记录')
            except (NotImplementedError,ValueError,cv2.error,requests.RequestException,OSError,rawpy.LibRawError) as exc:
                record.update(status='unavailable', reason=str(exc) if isinstance(exc,(ValueError,NotImplementedError)) else type(exc).__name__)
            log.append(record)
            if record['status']=='success':
                yield dict(kind='step',image=str(folder/filename),source=row['source'],operation=operation['name'],record=dict(record))
    Image.fromarray(current).save(folder / 'result_preview.png')
    report = dict(photo=str(Path(photo).resolve()), memory=memory, preview_size=list(image.size),
        vision_model=os.getenv('DASHSCOPE_VISION_MODEL','qwen3-vl-plus'),
        text_model=os.getenv('DASHSCOPE_MODEL','qwen-plus'), observation=observation,
        analysis=analysis, proposed_analysis=proposed_analysis, execution=log,addition_diagnostics=addition_diagnostics)
    (folder/'analysis.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    yield dict(kind='complete',folder=folder,report=report)


def run(photo, memory, output_dir=None, observation_override=None):
    for event in run_stream(photo,memory,output_dir,observation_override):
        if event['kind']=='complete': return event['folder'],event['report']
    raise RuntimeError('处理未完成')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--photo', type=Path, required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--text')
    group.add_argument('--text-file',type=Path)
    args = parser.parse_args()
    try:
        folder, report = run(args.photo, args.text if args.text is not None else args.text_file.read_text(encoding='utf-8'))
        print(json.dumps(report,ensure_ascii=False,indent=2))
        print(f'结果目录：{folder}')
    except Exception as exc:
        parser.exit(1, f'处理失败：{str(exc) if isinstance(exc,ValueError) else type(exc).__name__}\n')
