"""上传照片 → 回忆 → 逐步累积修改 → 条带拼合。"""
import os
os.environ.setdefault('GRADIO_ANALYTICS_ENABLED','False')
import gradio as gr
from vision import prepare_image
from series import generate_series


def preview(photo):
    if not photo: return None
    try: return prepare_image(photo)
    except Exception: raise gr.Error('无法读取这张照片，请检查 RAW/JPEG 文件是否完整。')


def create(photo,memory):
    try:
        for state in generate_series(photo,memory):
            yield (state['status'],[(p,state.get('labels',[f'第 {j+1} 步 · 累计修改' for j in range(len(state['images']))])[i]) for i,p in enumerate(state['images'])],state['composite'],state['archive'],state['masks'])
    except ValueError as exc: raise gr.Error(str(exc))
    except Exception: raise gr.Error('处理未完成，已写入的结果保留在 outputs 文件夹。')


with gr.Blocks(title='Latent Recall · 回忆显影') as app:
    gr.Markdown('# 回忆显影\n上传一张照片，写下你的回忆，让不同显影结果以条带交织。')
    with gr.Row():
        with gr.Column():
            photo=gr.File(label='1 · 上传 RAW 或 JPEG 照片',type='filepath')
            memory=gr.Textbox(label='2 · 写下关于这张照片的回忆',lines=5,placeholder='我想隐藏这张照片。／记忆好像破损了。／焦点应该在窗户上……')
            gr.Markdown('每一步在上一步的结果上继续修改。每完成一步立即显示一张，全部完成后再拼合。原图在最左侧，后面按步骤顺序等宽拼合。')
            gr.Markdown('点击后会将缩小的照片预览和回忆发送给百炼。先理解原话与照片，再按顺序累计处理；至少输出三张有变化的累计阶段图；无法直接理解或执行时，用基础明暗调整兜底并注明。')
            button=gr.Button('开始生成并拼合',variant='primary')
        original=gr.Image(label='上传照片预览',interactive=False)
    gr.Markdown('支持白化消失、粗颗粒、漏光、重影、失焦柔白和图像破损等媒介模拟。焦点迁移保留目标已有细节、虚化其他部分；不恢复失焦细节或画外信息。')
    gr.Markdown('只有你明确提到照片中缺失的对象，才会尝试局部AI补充，并标注生成内容；自查不通过会重试一次。新增人脸仅呈现模糊白色脸形，不生成五官。')
    status=gr.Markdown('等待上传照片与输入回忆。')
    gallery=gr.Gallery(label='按顺序累计修改的阶段照片',columns=3)
    composite=gr.Image(label='条带拼合成品',interactive=False)
    masks=gr.Gallery(label='局部范围（绿色：分割区域或生成允许范围）',columns=3)
    archive=gr.File(label='下载全部结果与创作记录',interactive=False)
    gr.Markdown('阶段效果图基于最长边 1600 像素预览；拼合画布与原图同尺寸，放大不增加细节。局部区域由分割模型识别；请在绿色标记图中检查范围，分割失败时不执行该局部修改。')
    photo.change(preview,photo,original)
    button.click(create,[photo,memory],[status,gallery,composite,archive,masks],concurrency_limit=1)

if __name__=='__main__':
    app.queue().launch(server_name='127.0.0.1',server_port=7860,share=False)
