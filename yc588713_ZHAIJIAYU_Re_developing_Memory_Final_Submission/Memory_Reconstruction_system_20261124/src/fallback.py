"""不依赖 API 的可追踪基础调整；不生成物体，不把兜底称为语义理解。"""
import numpy as np
from photo_pipeline import apply_preview

def fallback_step(image, stops):
    op=dict(name='exposure',parameters={'stops':stops},region=None)
    result=apply_preview(image,op)
    if np.array_equal(result,image):
        # 纯黑/量化极限：曝光乘法无效时微调黑位；仍不捏造图像内容。
        delta=2 if float(image.mean())<128 else -2
        result=np.clip(image.astype(np.int16)+delta,0,255).astype(np.uint8)
        op=dict(name='fallback_tonal_offset',parameters={'levels':delta},region=None)
    if np.array_equal(result,image): raise ValueError('图像无法形成有效变化')
    return result,op
