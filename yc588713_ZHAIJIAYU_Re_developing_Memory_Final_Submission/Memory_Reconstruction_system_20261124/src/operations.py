"""作品操作目录与参数校验；这是定义，不是第 3 步的图像引擎。"""
from __future__ import annotations
import json
import math
from copy import deepcopy


def number(low, high, default=0, unit='normalized'):
    return dict(type='number', minimum=low, maximum=high, default=default, unit=unit)


def choice(*values):
    return dict(type='string', enum=list(values), default=values[0])


OPERATIONS = {}


def define(name, scope, stage, params, description, example, implementation,
           note='', availability='planned'):
    OPERATIONS[name] = dict(name=name, type=scope, stage=stage, parameters=params,
        description=description, memory_examples=[example], implementation=implementation,
        note=note, availability=availability, requires_region=scope == 'local')


def strength():
    return {'amount': number(0, 1)}


def signed():
    return {'amount': number(-1, 1)}


define('exposure', 'global', 'raw', {'stops': number(-2, 3, unit='EV')},
       '整体提亮或压暗', '那天特别亮、刺眼',
       'exp_shift=2**stops；关闭自动亮度；固定其他显影设置', '不能恢复已丢失的细节')
define('white_balance', 'global', 'raw', signed(), '负值冷，正值暖', '灯光更暖',
       '基于相机白平衡，按 color_desc 将 R 乘 2**amount、B 乘 2**(-amount)，G 不变；写入 user_wb 并关闭自动及相机 WB 开关',
       '艺术性的相对冷暖控制，不是开尔文色温；基准白平衡无效时必须报告')
define('saturation', 'global', 'post', signed(), '调整色彩强度', '颜色褪掉了',
       '浮点 RGB 转 HSV，S 乘 1+amount，再限制到有效范围', '-1 去色，0 不变；不是传感器饱和值 user_sat')
define('contrast', 'global', 'post', signed(), '调整明暗反差', '画面很硬',
       '以 0.5 为中心，斜率 2**(2*amount)，裁剪到 [0,1]', '硬/柔含义不清时请求确认')
for name, scope in [('global_blur', 'global'), ('local_blur', 'local')]:
    define(name, scope, 'post', strength(), '弱化细节', '整个场景都模糊了' if scope == 'global' else '背景完全想不起来',
           'GaussianBlur；sigma=amount*0.02*图像短边；0 跳过；局部使用蒙版混合', '视觉转译，不是恢复记忆或重选焦平面')
define('local_brighten', 'local', 'post', {'stops': number(0, 2, unit='EV')},
       '提亮指定区域', '暗处的东西我记得很清楚', '在线性 RGB 乘 2**stops，再蒙版混合', '只增强已有信息')
define('local_sharpen', 'local', 'post', strength(), '增强局部边缘', '她的脸其实更清楚',
       '反差锐化：原图+2*amount*(原图-高斯模糊)，再蒙版混合', '不能恢复失焦丢失的真实细节')
define('lift_blacks', 'global', 'post', strength(), '抬升黑位', '雾蒙蒙的',
       '显示 RGB：y=x*(1-0.25*amount)+0.25*amount', '不是修改传感器黑电平校准')
define('vignette', 'global', 'post', strength(), '主动压暗四周', '视线只在中间',
       '按归一化椭圆半径平方施加最多 2*amount EV 衰减', '与保留镜头原有暗角分开')
define('pixelate', 'global', 'post', strength(), '块状轮廓', '只记得个大概',
       '块边长=1+round(amount*短边/32)，缩小后最近邻放大', '不是传感器采样结构')
define('color_shift', 'global', 'post', {'degrees': number(-180, 180, unit='degree')},
       '沿色相环旋转', '颜色怪怪的，不像真的', '浮点 HSV：H=(H+degrees)%360',
       '正值沿红→黄→绿方向，负值反向；叙述未指定方向时请求确认，不能任意选色')
define('void', 'local', 'post', {}, '以空白和羽化边缘替代区域', '那里本来还有一个人',
       '蒙版内白色填充；边缘固定羽化半径为短边的 1%；位置未知时仅旁注', '无强度参数；不补出具体人物')
define('tone_mapping', 'global', 'post', {'shadows': number(0, 1), 'highlights': number(0, 1)},
       '暗部提升、亮部压暗', '亮处和暗处都看得清',
       '在线性亮度上用平滑暗部/亮部权重调节，保留色度；两参数为 0 时不变', '不增加采集信息；先采用色调映射，不默认多次融合')
define('local_glow', 'local', 'post', {'stops': number(0, 2, unit='EV'), 'halo': number(0, 1)},
       '局部提亮并向外形成柔光', '他的手好像在发光',
       '蒙版内线性提亮，提亮增量经高斯扩散形成光晕；halo=0 无光晕', '艺术诠释；好像需记录不确定性，不自动转为事实')
define('sensor_pattern', 'local', 'sensor', {'scale': number(1, 32, 8, 'display_pixels_per_site')},
       '真实采样格点可视化', '背景完全想不起来',
       '读取 raw_image_visible、raw_colors_visible、color_desc；按真实 CFA 着色，再处理方向与蒙版坐标映射',
       '不得假设 Bayer；检查实际传感器，非 CFA 数据不执行', 'experimental')
define('preserve_noise', 'global', 'raw', {}, '保留记录中现存噪声', '很粗糙、很嘈杂',
       'fbdd_noise_reduction=Off, noise_thr=None, median_filter_passes=0',
       '默认已经关闭时可能没有变化；不能恢复已删除的噪声；嘈杂是隐喻')
define('noise_emphasis', 'global', 'post', strength(), '增强现有高频纹理', '噪点更明显',
       '放大原图与低通结果的残差，不添加随机噪声', '残差包含纹理和边缘，不声称分离了真实传感器噪声')
define('preserve_aberration', 'global', 'raw', {}, '保留现有色差', '边缘有点花',
       'chromatic_aberration=(1,1)，不额外执行镜头色差校正', '不能撤销已烘焙的修正', 'experimental')
define('channel_shift', 'global', 'post', {'dx': number(-0.02, 0.02), 'dy': number(-0.02, 0.02)},
       '主动通道错位', '边缘在晃', 'R 按宽高比例位移，B 反向位移，G 不变；反射边界', '主动制造，非恢复色差')
define('preserve_distortion', 'global', 'raw', {}, '不添加镜头几何校正', '那里感觉更宽',
       '不调用后续镜头校正模块', '不能恢复真实视点；rawpy 本来未校正时无可见变化', 'experimental')
define('geometry_warp', 'global', 'post', {'width': number(-1, 1), 'zoom': number(-1, 1)},
       '改变空间比例与接近感', '那里感觉更宽、更近',
       '中心变换：横向缩放 2**(0.5*width)，整体缩放 2**(0.5*zoom)，保留画布；反射边界', '主动变形，不是恢复真实空间')
define('raw_color_experiment', 'global', 'raw', {'darken_stops': number(-2, 0, unit='EV')},
       '相机通道的实验色彩显示', '颜色怪怪的，整体更暗',
       'output_color=raw；按 color_desc 映射 R/G/B，多个 G 取均值；单位 WB；线性缩放后以固定 sRGB 编码显示',
       '明确为伪色显示，不是色度准确的转换；整体压暗优先用 exposure；与常规 WB 管线互斥', 'experimental')
define('preserve_hot_pixels', 'global', 'raw', {}, '保留现存异常点', '夜里那些小亮点还在',
       '不提供 bad_pixels_path，不调用额外坏点修补；需逐机型验证', '不能保证解码器保留所有坏点；噪点提升另用 noise_emphasis', 'experimental')
for name, desc, example in [('generate_add', '加入人物或物体', '那里本来还有一个人'),
                             ('generate_remove', '移除对象并补背景', '那个东西当时不在'),
                             ('generate_detail', '生成局部细节', '她的脸其实更清楚')]:
    define(name, 'local', 'generative', {'prompt': {'type': 'string', 'minLength': 1}},
           desc, example, '未来接入蒙版内重绘；保存模型、提示词、种子和生成区域',
           '推测性补充，必须带生成标记；当前不可执行', 'deferred')
define('motion_blur', 'local', 'post', {'amount': number(0, 1), 'angle': number(-180, 180, unit='degree')},
       '非生成方向拖影', '人来人往，一直在动', '方向卷积核长度=1+round(amount*短边*0.05)，蒙版混合', '单帧视觉转译，不是多帧记录')
define('multi_frame_blend', 'global', 'multi_frame', {'frames': {'type': 'array', 'items': {'type': 'string'}, 'minItems': 2}},
       '多帧叠加', '人来人往，一直在动', '检查多帧来源并对齐后等权融合', '只有一张 RAW 时不可执行；不能自动代换为生成', 'deferred')


for local, global_name in [('local_saturation','saturation'),('local_white_balance','white_balance'),('local_contrast','contrast'),('local_exposure','exposure')]:
    base=OPERATIONS[global_name]
    define(local,'local','post',deepcopy(base['parameters']), '局部'+base['description'],
           '只调整指定区域', '在当前 RGB 上处理并用蒙版混合', '局部曝光允许负值压暗；不重显影、不恢复丢失细节')


# 网页新增对象由独立视觉计划授权，不能直接编写自由生图提示词。
define('generate_add','global','generative',{'request_id':{'type':'string','minLength':1}},
       '在已批准的位置补入原话明确提及的缺失对象','那里本来还有一把伞',
       '百炼图像编辑、范围合成、视觉自查；失败重试一次','推测性生成；人脸仅白色模糊轮廓；必须引用 approved_additions 中的 id')

from media_effects import register
register(define, number, choice)
from pipeline_effects import register as register_pipeline
register_pipeline(define, number, choice, OPERATIONS)
from perceptual_effects import register as register_perceptual
register_perceptual(define, number, choice, OPERATIONS)

from poetic_effects import register as register_poetic
register_poetic(define, number, choice, OPERATIONS)


def catalog():
    return deepcopy(list(OPERATIONS.values()))


def validate_operation(item, regions=()):
    """拒绝越界、未知字段、缺失参数及无效区域；不静默裁剪。"""
    if not isinstance(item, dict) or set(item) != {'name', 'parameters', 'region'}:
        raise ValueError('操作必须包含且仅包含 name、parameters、region')
    name = item['name']
    if not isinstance(name, str) or name not in OPERATIONS:
        raise ValueError('未知操作')
    spec = OPERATIONS[name]
    params = item['parameters']
    if not isinstance(params, dict) or set(params) != set(spec['parameters']):
        raise ValueError(f'{name}: 参数名称不匹配')
    for key, rule in spec['parameters'].items():
        value = params[key]
        if rule['type'] == 'number':
            if type(value) not in (int, float) or not math.isfinite(value) or not rule['minimum'] <= value <= rule['maximum']:
                raise ValueError(f'{name}.{key}: 数值不合法或超出范围')
        elif rule['type'] == 'string':
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f'{name}.{key}: 需要非空文本')
            if 'enum' in rule and value not in rule['enum']:
                raise ValueError(f'{name}.{key}: 不支持此选项')
        elif rule['type'] == 'array':
            if not isinstance(value, list) or len(value) < rule['minItems'] or any(not isinstance(v, str) or not v.strip() for v in value):
                raise ValueError(f'{name}.{key}: 需要至少两张来源文件')
    if spec['requires_region']:
        if not isinstance(item['region'], str) or item['region'] not in regions:
            raise ValueError(f'{name}: 缺少已登记区域')
    elif item['region'] is not None:
        raise ValueError(f'{name}: 全局操作 region 必须为 null')
    return deepcopy(item)


if __name__ == '__main__':
    print(json.dumps(catalog(), ensure_ascii=False, indent=2))
