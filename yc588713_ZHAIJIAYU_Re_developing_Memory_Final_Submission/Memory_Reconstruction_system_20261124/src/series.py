"""一次理解，逐步累积修改；原图和各阶段依次等宽拼合。"""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json
import shutil
import zipfile
from PIL import Image
import numpy as np
from fallback import fallback_step
from photo_pipeline import run_stream, PROJECT
from vision import prepare_image


def compose(original,paths,output):
    """按原图 W/(N+1) 在对应坐标取条；余数由整数边界均匀分配。"""
    w,h=original.size
    count=len(paths)+1
    if w<count: raise ValueError('照片宽度不足以拼合全部结果')
    result=Image.new('RGB',(w,h));mapping=[]
    for i,path in enumerate([None]+list(paths)):
        left=i*w//count;right=(i+1)*w//count
        if path is None:
            stripe=original.crop((left,0,right,h));name='original.png'
        else:
            with Image.open(path) as im:
                im=im.convert('RGB');iw,ih=im.size
                # 裁取相应画面位置并恢复至原图画布大小，避免把整张图压成窄条。
                stripe=im.resize((right-left,h),Image.Resampling.BICUBIC,
                    box=(left*iw/w,0,right*iw/w,ih))
            name=Path(path).name
        result.paste(stripe,(left,0));mapping.append(dict(start=left,end=right,source=name))
    result.save(output)
    return mapping


def package_stages(folder,source,memory,run_dir,report):
    folder=Path(folder);run_dir=Path(run_dir);source=Path(source)
    paths=[];stages=[];generated_content=[]
    for record in report['execution']:
        if record['status']!='success' or not record.get('image'): continue
        target=folder/f'result_{len(paths)+1:02d}.png'
        shutil.copy2(run_dir/record['image'],target)
        if record.get('generated'): generated_content.append(record['generation']['object'])
        stages.append(dict(generated=record.get('generated',False),generated_content=list(generated_content),index=len(paths)+1,image=target.name,source_step=str((run_dir/record['image']).relative_to(folder)),
            source=record['source'],operation=record['operation'],previous='original_preview.png' if not paths else Path(paths[-1]).name,fallback=record.get('fallback',False),reason=record.get('reason',''),category=record.get('category','G' if record.get('generated') else 'E'),pipeline=record.get('pipeline')))
        paths.append(str(target))
    skipped=[r for r in report['execution'] if r['status'] not in ('success','no_action')]
    manifest=dict(mode='sequential',memory=memory,count=len(paths),source=source.name,stages=stages,skipped=skipped)
    manifest['addition_diagnostics']=report.get('addition_diagnostics',{})
    composite=None
    if paths:
        original=prepare_image(source,max_side=None);original.save(folder/'original.png')
        composite=str(folder/'composite.png')
        manifest['strips']=compose(original,paths,composite)
        manifest.update(status='completed',original_size=list(original.size),ideal_strip_width=original.width/(len(paths)+1))
    else: manifest['status']='no_executable_operations'
    (folder/'series.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (folder/'memory.txt').write_text(memory,encoding='utf-8')
    archive=folder/'results.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as z:
        z.write(source,'original_upload'+source.suffix.lower())
        for path in sorted(folder.rglob('*')):
            if path.is_file() and path not in (archive,source): z.write(path,path.relative_to(folder))
    status=f'已保存 {len(paths)} 张累计修改的阶段图，原图在左、后接实际完成的阶段。' if paths else '没有可执行操作，未生成阶段图。'
    fallback_count=sum(r.get('fallback',False) for r in stages)
    if fallback_count: status+=f'其中 {fallback_count} 张采用基础明暗调整兜底；不是精确的局部重建，原因已记录。'
    elif skipped: status+=f'另有 {len(skipped)} 项没有直接执行，详见记录。'
    if 'AllocationQuota.FreeTierOnly' in (report.get('pipeline_error') or ''):
        status+=' 百炼语义模型免费额度已用完，本次未完成AI语义分析；请检查百炼额度及计费设置。'
    addition_info=report.get('addition_diagnostics',{})
    if addition_info.get('status')=='error':
        status+=' 补物分析未完成：'+addition_info.get('error','详见补物记录')[:240]+'；没有生成新增物体。'
    elif addition_info.get('status')=='not_planned':
        summaries=[a.get('summary','') for a in addition_info.get('audit',[]) if a.get('summary')]
        status+=' 未安排AI补物：'+(str(summaries[-1])[:240] if summaries else '未确认明确补入意图和缺失对象，详见补物记录。')
    for failed in skipped:
        if failed.get('operation',{}).get('name')in ('generate_add','spatial_reconstruction'):
            status+='\n\n未完成这项补入：'+failed.get('source','')+'。原因：'+failed.get('reason','未通过检查')[:180]
    return dict(status=status,fallback_count=fallback_count,skipped_count=len(skipped),images=paths,labels=[f'第 {s["index"]} 步 · 累计修改'+(' · 含AI补充：'+ '、'.join(s['generated_content']) if s['generated_content'] else '') for s in stages],composite=composite,archive=str(archive),
        masks=[str(p) for p in sorted(run_dir.rglob('region_*_overlay.png'))])


def _generate_single_series(photo,memory):
    if not photo or not Path(photo).is_file(): raise ValueError('请上传照片')
    if not memory or not memory.strip(): raise ValueError('请输入关于照片的回忆')
    folder=PROJECT/'outputs'/('series_'+datetime.now(ZoneInfo('Asia/Shanghai')).strftime('%Y%m%d_%H%M%S_%f'))
    folder.mkdir(parents=True)
    source=folder/('source'+Path(photo).suffix.lower());shutil.copy2(photo,source)
    yield dict(status='正在理解照片与回忆，按顺序在上一结果上继续修改…',images=[],composite=None,archive=None,masks=[])
    paths=[];planned_total=None
    def state(status):
        generated=[];labels=[]
        for i in range(len(paths)):
            if i<len(completed) and completed[i].get('generated'): generated.append(completed[i]['generation']['object'])
            labels.append(f'第 {i+1} 步 · 累计修改'+(' · 含AI补充：'+'、'.join(generated) if generated else ''))
        return dict(status=status,images=list(paths),labels=labels,total=planned_total,composite=None,archive=None,
            masks=[str(p) for p in sorted((folder/'run_01').rglob('region_*_overlay.png'))])
    run_dir=folder/'run_01'
    report=None;completed=[];pipeline_error=None
    try:
        for event in run_stream(source,memory,output_dir=run_dir):
            if event['kind']=='plan':
                planned_total=event['total'];yield state('修改顺序已确定，正在制作影像…')
            elif event['kind']=='progress': yield state(event['status'])
            elif event['kind']=='step':
                paths.append(event['image'])
                completed.append(event.get('record',dict(status='success',image=Path(event['image']).name,
                    source=event['source'],operation=dict(name=event['operation'],parameters={},region=None))))
                yield state(f"第 {len(paths)} 步已完成：{event['source']}（{event['operation']}）")
            elif event['kind']=='complete': report=event['report']
    except Exception as exc:
        pipeline_error=str(exc) if isinstance(exc,ValueError) else type(exc).__name__
        yield state('智能分析暂未完成，正在检查并改用本地基础调整…')
    try:
        run_dir.mkdir(parents=True,exist_ok=True)
        if report is None:
            report=dict(memory=memory,execution=list(completed),pipeline_error=pipeline_error)
        failed=[r for r in report['execution'] if r['status'] not in ('success','no_action')]
        successful=[r for r in report['execution'] if r['status']=='success']
        # 不为凑张数重复明暗：已有有效阶段就保留；全部失败最多一次轻微兜底。
        needed=0 if successful else 1
        if needed>0:
            preview=run_dir/'original_preview.png'
            if not preview.exists(): prepare_image(source).save(preview)
            with Image.open(run_dir/successful[-1]['image'] if successful else preview) as im:
                current=np.array(im.convert('RGB'))
            direction=1 if current.mean()<128 else -1
            increment=direction*.06
            for index in range(needed):
                current,operation=fallback_step(current,increment)
                filename=f'fallback_{index+1:02d}.png'
                Image.fromarray(current).save(run_dir/filename)
                reason=failed[index].get('reason','无法直接执行') if index<len(failed) else pipeline_error or '没有有效阶段，提供一次轻微明暗兜底'
                record=dict(status='success',source=failed[index].get('source',memory) if index<len(failed) else memory,
                    image=filename,operation=operation,fallback=True,reason=reason)
                report['execution'].append(record)
                paths.append(str(run_dir/filename))
                completed.append(record)
                (run_dir/'analysis.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
                yield state(f'第 {len(paths)} 步已完成：基础明暗兜底（已确认画面发生变化）')
        yield state('全部阶段已保存，正在拼合与整理下载文件…')
        yield package_stages(folder,source,memory,run_dir,report)
    except Exception as exc:
        message=str(exc) if isinstance(exc,ValueError) else type(exc).__name__
        (folder/'series.json').write_text(json.dumps(dict(mode='sequential',memory=memory,source=source.name,status='failed',reason=message),ensure_ascii=False,indent=2))
        yield state('当前文件无法完成输出，请换一张可正常打开的照片或检查磁盘空间。已完成图片保留。')


def split_narrators(memory):
    """只有显式署名标题才拆分，不把普通多段回忆误当成多人。"""
    import re
    matches=list(re.finditer(r'^【(?:叙述者|Narrator)\s*[:：]\s*([^\n】]{1,60})】\s*$',memory,re.M|re.I))
    if not matches:return []
    if memory[:matches[0].start()].strip():raise ValueError('多人回忆请从【叙述者：名字】开始，前面不要放未署名内容')
    if len(matches)>6:raise ValueError('一次最多比较六位叙述者的回忆')
    entries=[]
    for i,m in enumerate(matches):
        text=memory[m.end():matches[i+1].start() if i+1<len(matches) else len(memory)].strip()
        if not text:raise ValueError('每位叙述者标题下需要填写回忆')
        entries.append(dict(narrator=m.group(1).strip(),memory=text))
    return entries




def generate_series(photo,memory):
    entries=split_narrators(memory or '')
    if not entries:
        yield from _generate_single_series(photo,memory)
        return
    folder=PROJECT/'outputs'/('perspectives_'+datetime.now(ZoneInfo('Asia/Shanghai')).strftime('%Y%m%d_%H%M%S_%f'))
    folder.mkdir(parents=True)
    original=prepare_image(photo,max_side=1600);original.save(folder/'original.png')
    completed=[];images=[];labels=[];skipped=0;fallbacks=0
    for i,entry in enumerate(entries,1):
        final=None
        try:
            for state in _generate_single_series(photo,entry['memory']):
                final=state
                yield dict(state,images=images+state.get('images',[]),labels=labels+[entry['narrator']+' · '+label for label in state.get('labels',[])],
                    composite=None,archive=None,total=None,status=f'回忆 {i}/{len(entries)} · {entry["narrator"]}：'+state['status'])
            if not final or not final.get('images'):raise ValueError('该回忆没有完成的阶段图')
            images.extend(final['images']);labels.extend(entry['narrator']+' · '+label for label in final.get('labels',[]))
            target=folder/f'perspective_{i:02d}.png';shutil.copy2(final['images'][-1],target)
            completed.append(dict(**entry,status='completed',image=target.name,archive=final.get('archive'),stages=list(final['images'])))
            skipped+=final.get('skipped_count',0)
            fallbacks+=final.get('fallback_count',0)
        except (ValueError,OSError) as exc:
            skipped+=1;completed.append(dict(**entry,status='failed',reason=str(exc)))
    successful=[folder/e['image'] for e in completed if e['status']=='completed']
    composite=None
    if successful:
        composite=str(folder/'composite.png');strips=compose(original,successful,composite)
    else:strips=[]
    manifest=dict(mode='parallel_memories',note='每位叙述者从同一原片独立开始；不是阶段间累计关系',entries=completed,strips=strips)
    (folder/'perspectives.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (folder/'memory.txt').write_text(memory,encoding='utf-8')
    archive=folder/'results.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        z.write(photo,'original_upload'+Path(photo).suffix.lower())
        for p in folder.iterdir():
            if p.is_file() and p!=archive:z.write(p,p.name)
        for i,e in enumerate(completed,1):
            if e.get('archive'):z.write(e['archive'],f'narrator_{i:02d}/all_stages.zip')
    yield dict(status=f'已完成 {len(successful)}/{len(entries)} 份独立回忆；各自从原图开始，最终按署名顺序并置。',images=images,labels=labels,
               composite=composite,archive=str(archive),total=len(images),masks=[],fallback_count=fallbacks,skipped_count=skipped)
