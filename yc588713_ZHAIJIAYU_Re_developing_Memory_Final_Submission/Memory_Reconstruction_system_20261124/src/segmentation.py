"""文字由视觉模型定位，SAM 2.1 在本地把位置框细化为物体轮廓。"""
from functools import lru_cache
from pathlib import Path
from threading import Lock
import json
import numpy as np
import cv2
from PIL import Image

PROJECT=Path(__file__).resolve().parents[1]
MODEL='facebook/sam2.1-hiera-tiny'
REVISION='de431c4043854a71d8101e17995dfe596bf101a5'
CACHE=PROJECT/'.models'
LOCK=Lock()


@lru_cache(maxsize=1)
def load_model():
    import torch
    from transformers import Sam2Model, Sam2Processor
    torch.set_num_threads(4)
    processor=Sam2Processor.from_pretrained(MODEL,revision=REVISION,cache_dir=str(CACHE),local_files_only=True)
    model=Sam2Model.from_pretrained(MODEL,revision=REVISION,cache_dir=str(CACHE),local_files_only=True,use_safetensors=True).eval().to('cpu')
    return processor,model


def download_model():
    from huggingface_hub import snapshot_download
    return snapshot_download(MODEL,revision=REVISION,cache_dir=str(CACHE),
        allow_patterns=['*.json','model.safetensors'])


def check_mask(mask,box,score):
    if not np.isfinite(score) or score<0.6: raise ValueError('分割质量评分偏低，需要重新定位或手动确认')
    if mask.ndim!=2 or not np.isfinite(mask).all(): raise ValueError('分割返回了无效蒙版')
    mask=mask.astype(bool)
    count=int(mask.sum())
    if count<8 or count>mask.size*0.95: raise ValueError('分割为空、过小或覆盖几乎全图，未执行局部修改')
    h,w=mask.shape
    l,t,r,b=box
    # 位置框只用于合理性检查，不裁掉 SAM 在框外识别出的真实轮廓。
    area=mask[max(0,int(t*h)):min(h,int(np.ceil(b*h))),max(0,int(l*w)):min(w,int(np.ceil(r*w)))].sum()
    if area/count<0.5: raise ValueError('分割与目标位置明显不符，需要确认')
    return mask


def segment_regions(image,regions,folder):
    """失败区域不回退为矩形；返回可用蒙版和全部区域的明确状态。"""
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    masks={};records=[]
    if not regions:
        (folder/'segmentation.json').write_text('[]',encoding='utf-8')
        return masks,records
    try:
        processor,model=load_model()
    except Exception as exc:
        records=[dict(name=r['name'],status='unavailable',reason=f'本地分割模型未就绪（{type(exc).__name__}），请运行 python src/segmentation.py --download') for r in regions]
    else:
        import torch
        w,h=image.size
        for index,region in enumerate(regions,1):
            record=dict(name=region['name'],box=region['box'],model=MODEL,revision=REVISION)
            try:
                l,t,r,b=region['box']
                if region.get('method','object')=='luminance':
                    if (r-l)*(b-t)>.8: raise ValueError('光影区域过于宽泛，需要更精确的定位')
                    binary=np.zeros((h,w),bool)
                    binary[int(t*h):max(int(t*h)+1,int(b*h)),int(l*w):max(int(l*w)+1,int(r*w))]=True
                    record['method']='luminance'
                    record['model']='luminance_selection'
                    score=None
                else:
                    inputs=processor(images=image,input_boxes=[[[l*w,t*h,r*w,b*h]]],return_tensors='pt')
                    with LOCK,torch.inference_mode():
                        outputs=model(**inputs,multimask_output=False)
                    mask=processor.post_process_masks(outputs.pred_masks.cpu(),inputs['original_sizes'])[0].reshape(-1,h,w)[0].numpy()
                    score=float(outputs.iou_scores.flatten()[0])
                    binary=check_mask(mask,region['box'],score)
                    record['method']='object'
                selection=region.get('selection','whole')
                if selection in ('highlights','shadows'):
                    rgb=np.array(image.convert('RGB'),dtype=np.float32)/255
                    light=rgb[:,:,0]*.2126+rgb[:,:,1]*.7152+rgb[:,:,2]*.0722
                    cutoff=float(np.quantile(light[binary],.65 if selection=='highlights' else .35))
                    binary=binary & ((light>=cutoff) if selection=='highlights' else (light<=cutoff))
                    if binary.sum()<8: raise ValueError('目标内没有足够明确的亮部或暗部')
                    record['selection']=selection
                    record['brightness_cutoff']=cutoff
                # 仅轻微羽化轮廓，不以位置框生成效果区域。
                soft=cv2.GaussianBlur(binary.astype(np.float32),(0,0),0.8)
                prefix=f'region_{index:02d}'
                Image.fromarray(binary.astype(np.uint8)*255).save(folder/f'{prefix}_binary.png')
                Image.fromarray(np.round(soft*255).astype(np.uint8)).save(folder/f'{prefix}_mask.png')
                overlay=np.array(image.convert('RGB')).astype(np.float32)
                overlay[binary]=overlay[binary]*0.55+np.array([35,225,130])*0.45
                Image.fromarray(np.round(overlay).astype(np.uint8)).save(folder/f'{prefix}_overlay.png')
                masks[region['name']]=soft
                record.update(status='success',score=score,area_pixels=int(binary.sum()),mask_file=f'{prefix}_mask.png',overlay_file=f'{prefix}_overlay.png')
            except Exception as exc:
                record.update(status='unavailable',reason=str(exc) if isinstance(exc,ValueError) else f'分割失败：{type(exc).__name__}')
            records.append(record)
    (folder/'segmentation.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
    return masks,records


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--download',action='store_true')
    args=parser.parse_args()
    if args.download: print(download_model())
