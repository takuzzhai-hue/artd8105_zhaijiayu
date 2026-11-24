"""百炼文本语义分析入口；不录音、不上传 RAW、不执行显影。"""
from __future__ import annotations
import argparse
import json
import os
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests
from dotenv import load_dotenv
from operations import OPERATIONS, catalog, validate_operation
from media_effects import SPECS, GLOBAL_ONLY

PROJECT = Path(__file__).resolve().parents[1]
STATUSES = {'proposed', 'missing', 'conflict', 'needs_confirmation', 'no_action', 'unavailable'}


def validate_analysis(result, memory, regions, additions=()):
    if not isinstance(result, dict) or set(result) != {'sentences'} or not isinstance(result['sentences'], list) or not result['sentences']:
        raise ValueError('需要非空 sentences 数组')
    for row in result['sentences']:
        if not isinstance(row, dict) or set(row) != {'source', 'intent', 'status', 'reason', 'operations'}:
            raise ValueError('句子字段不完整')
        if any(not isinstance(row[k], str) or not row[k].strip() for k in ('source', 'intent', 'status', 'reason')):
            raise ValueError('句子字段必须为非空文本')
        if row['source'] not in memory:
            # 模型可能纠正错字或改写标点；引用必须由程序绑定真实输入。
            model_quote=row['source']
            row['source']=memory
            row['reason']+=f'；模型引用为「{model_quote}」，未逐字匹配；此项关联整段原始输入，不将改写冒充原句。'
        aliases={'建议执行':'proposed','待执行':'proposed','需要确认':'needs_confirmation',
                 '缺失':'missing','冲突':'conflict','无需操作':'no_action','无法执行':'unavailable'}
        row['status']=aliases.get(row['status'].strip(),row['status'].strip())
        if row['status'] not in STATUSES:
            raise ValueError(f"未知状态：{row['status']}；请使用指定状态之一")
        if not isinstance(row['operations'], list):
            raise ValueError('operations 必须是数组')
        if row['status']=='proposed' and not row['operations']:
            row['status']='no_action'
            row['reason']+='；该条没有独立操作，保留原说明；其余有效步骤继续执行。'
        if bool(row['operations']) != (row['status'] == 'proposed'):
            raise ValueError('只有 proposed 可以包含操作，且至少一个')
        for op in row['operations']:
            # 规范等价表达，保留局部意图，绝不改成全图处理。
            original_name=op.get('name') if isinstance(op,dict) else None
            if isinstance(op,dict) and isinstance(op.get('region'),str) and op['region'] in regions:
                if original_name in ('saturation','white_balance','contrast','exposure') or original_name in set(SPECS)-GLOBAL_ONLY:
                    op['name']='local_'+original_name
                elif original_name=='local_brighten' and isinstance(op.get('parameters'),dict):
                    stops=op['parameters'].get('stops')
                    if type(stops) in (int,float) and stops<0: op['name']='local_exposure'
                if op['name']!=original_name:
                    row['reason']+=f"；接口规范化：{original_name} → {op['name']}，保留原区域和参数。"
            validate_operation(op, regions)
            if op['name']=='generate_add' and op['parameters']['request_id'] not in {p['id'] for p in additions}:
                raise ValueError('没有获准的缺失对象计划，禁止新增物品')
            if OPERATIONS[op['name']]['availability'] != 'planned':
                raise ValueError('实验或延后操作不能直接提出执行')
    return result


def analyze(memory, regions=(), observation=None, diagnostics_dir=None):
    load_dotenv(PROJECT / '.env')
    key = os.getenv('DASHSCOPE_API_KEY')
    if not key:
        raise ValueError('未配置 DASHSCOPE_API_KEY；请在项目 .env 中填写，不要粘贴到聊天。')
    if not memory.strip():
        raise ValueError('回忆文本不能为空')
    base = os.getenv('DASHSCOPE_BASE_URL', 'https://dashscope.aliyuncs.com/compatible-mode/v1').rstrip('/')
    if not base.startswith('https://'):
        raise ValueError('API 地址必须使用 HTTPS')
    messages = [dict(role='system', content=(PROJECT / 'prompts/translator.txt').read_text() + '\n' + (PROJECT / 'prompts/poetic_mapping.txt').read_text()),
                dict(role='user', content=json.dumps(dict(memory=memory, regions=list(regions), photo_observation=observation, operations=catalog()), ensure_ascii=False))]
    for attempt in range(2):
        response = requests.post(base + '/chat/completions',
            headers={'Authorization': 'Bearer ' + key}, timeout=(10, 90),
            json=dict(model=os.getenv('DASHSCOPE_MODEL', 'qwen-plus'), messages=messages,
                      temperature=0, response_format={'type': 'json_object'}))
        if response.status_code != 200:
            try:
                error=response.json().get('error',{})
                code=str(error.get('code','unknown')) if isinstance(error,dict) else 'unknown'
            except ValueError: code='unknown'
            code=re.sub(r'[^A-Za-z0-9_.-]','',code)[:80]
            if diagnostics_dir:
                Path(diagnostics_dir).mkdir(parents=True,exist_ok=True)
                (Path(diagnostics_dir)/'translation_http_error.json').write_text(json.dumps(dict(status=response.status_code,code=code)),encoding='utf-8')
            if code=='AllocationQuota.FreeTierOnly':
                raise ValueError('百炼语义模型免费额度已用完，免费额度用完即停限制了调用（AllocationQuota.FreeTierOnly）；请在百炼控制台检查额度和计费设置。')
            raise ValueError(f'百炼请求失败，HTTP {response.status_code}，错误代码 {code}；本次未完成语义分析。')
        content = ''
        try:
            content = response.json()['choices'][0]['message']['content']
            result = json.loads(content)
            if diagnostics_dir:
                Path(diagnostics_dir).mkdir(parents=True,exist_ok=True)
                (Path(diagnostics_dir)/f'translation_attempt_{attempt+1}.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
            return validate_analysis(result, memory, regions, (observation or {}).get('approved_additions',[]))
        except (ValueError, KeyError, IndexError, TypeError) as exc:
            if attempt:
                raise ValueError(f'模型输出连续两次未通过校验：{exc}') from exc
            messages.append(dict(role='user', content=f'上一轮输出校验失败：{exc}。可用区域名称仅为 {list(regions)}，为空则任何局部操作必须改为 missing 且 operations 为空。请重新生成完整 JSON，逐字复制 source 原文；操作参数名及范围必须和操作表一致。上轮输出：{content}'))
    raise RuntimeError('分析未完成')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--text-file', type=Path, required=True)
    parser.add_argument('--regions', nargs='*', default=[])
    args = parser.parse_args()
    try:
        memory = args.text_file.read_text(encoding='utf-8')
        result = analyze(memory, args.regions)
        folder = PROJECT / 'outputs' / datetime.now(ZoneInfo('Asia/Shanghai')).strftime('%Y%m%d_%H%M%S_%f')
        folder.mkdir(parents=True, exist_ok=False)
        (folder / 'analysis.json').write_text(json.dumps(dict(memory=memory, regions=args.regions,
            model=os.getenv('DASHSCOPE_MODEL', 'qwen-plus'), analysis=result), ensure_ascii=False, indent=2), encoding='utf-8')
        print(f'分析已保存：{folder / "analysis.json"}')
    except (ValueError, OSError, requests.RequestException) as exc:
        # 不打印请求对象或响应全文，避免日志包含凭据。
        parser.exit(1, f'分析失败：{exc if isinstance(exc, ValueError) else type(exc).__name__}\n')
