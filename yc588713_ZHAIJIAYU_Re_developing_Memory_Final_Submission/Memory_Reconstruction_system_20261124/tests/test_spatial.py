import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import unittest
from unittest.mock import patch
from tempfile import TemporaryDirectory
import numpy as np
from PIL import Image
from spatial import plan_spatial, fracture, generate_spatial, outpaint_canvas, compose_extension, suppress_spatial_duplicates

PLAN=dict(source='空间错位',mode='side',scene='森林',allowed='树木',anchors='中心树干',reason='明确空间要求')
class SpatialTests(unittest.TestCase):
    def test_only_bands_change(self):
        base=np.full((100,120,3),30,np.uint8);view=np.full_like(base,160)
        for mode in ['side','extend_top','extend_bottom','extend_both']:
            out,mask=fracture(base,view,mode)
            self.assertTrue(np.array_equal(out[mask==0],base[mask==0]))
            self.assertGreater(np.count_nonzero(mask),0)
            self.assertLess(np.count_nonzero(mask),base.shape[0]*base.shape[1]*.4)
    def test_disabled_and_unbound(self):
        with TemporaryDirectory() as tmp,patch('spatial.vision_json',return_value={'enabled':False}):
            self.assertIsNone(plan_spatial(Image.new('RGB',(32,32)),'变暖',tmp))
        with TemporaryDirectory() as tmp,patch('spatial.vision_json',return_value=dict(PLAN,enabled=True)):
            with self.assertRaises(ValueError):plan_spatial(Image.new('RGB',(32,32)),'变暖',tmp)
    def test_rejected_candidates_do_not_commit(self):
        base=np.full((100,120,3),30,np.uint8)
        with TemporaryDirectory() as tmp,patch('spatial.edit_image',side_effect=lambda im,*args,**kwargs:(Image.fromarray(np.minimum(np.asarray(im).astype(int)+20,255).astype(np.uint8)),'test')),patch('spatial.vision_json',return_value={'same_space':False,'reason':'不同森林'}) as review:
            with self.assertRaises(ValueError):generate_spatial(base,PLAN,'空间错位',tmp)
            self.assertEqual(review.call_count,2)
            self.assertFalse((Path(tmp)/'accepted.png').exists())
    def test_success_records_generated_mask(self):
        base=np.full((100,120,3),30,np.uint8)
        good=dict(same_space=True,content_restrained=True,style_matches=True,direction_matches=True)
        with TemporaryDirectory() as tmp,patch('spatial.edit_image',side_effect=lambda im,*args,**kwargs:(Image.fromarray(np.minimum(np.asarray(im).astype(int)+20,255).astype(np.uint8)),'test')),patch('spatial.vision_json',return_value=good):
            out,meta=generate_spatial(base,PLAN,'空间错位',tmp)
            self.assertTrue(meta['generated']);self.assertFalse(np.array_equal(base,out))
            self.assertTrue((Path(tmp)/'applied_mask.png').exists())

    def test_extension_preserves_original_and_new_edges(self):
        base=np.arange(100*120*3,dtype=np.uint8).reshape(100,120,3)
        for mode in ['side','extend_top','extend_bottom','extend_both']:
            canvas,box=outpaint_canvas(base,mode)
            view=np.full_like(canvas,87)
            out,mask=compose_extension(base,view,box)
            l,t,r,b=box
            self.assertTrue(np.array_equal(out[t:b,l:r],base))
            self.assertTrue(np.all(out[mask>0]>0))
            self.assertTrue(np.all(out[mask>0]<255))
            self.assertGreater(out.shape[0],base.shape[0])
    def test_no_duplicate_white_or_damage(self):
        row=dict(source='空间错位',status='proposed',reason='',operations=[dict(name=n) for n in ['data_corruption','tilted_focus','local_overexposure','exposure']])
        clean=suppress_spatial_duplicates({'sentences':[row]},PLAN)
        self.assertEqual([o['name'] for o in clean['sentences'][0]['operations']],['exposure'])
    def test_file_damage_never_paints_white(self):
        from media_effects import render
        x=np.linspace(.1,.7,120,dtype=np.float32)[None,:,None]*np.ones((100,1,3),np.float32)
        out=render(x,'data_corruption',{'amount':.7})
        changed=np.any(out!=x,axis=2)
        self.assertLess(changed.mean(),.02)
        self.assertGreater(changed.sum(),0)
        self.assertLessEqual(float(out.max()),.71)
    def test_rgb_variants_cannot_leak_into_spatial_stages(self):
        from style import expand_media_stages
        rows=[dict(source='空间，错位。',status='proposed',reason='',operations=[dict(name='optical_aberration',parameters={'amount':.65},region=None),dict(name='local_optical_aberration',parameters={'amount':.65},region='树')]),dict(source='模型拆分的边缘失真',status='proposed',reason='',operations=[dict(name='channel_shift',parameters={'dx':.01,'dy':.01},region=None)])]
        cleaned=expand_media_stages(suppress_spatial_duplicates({'sentences':rows},PLAN))
        self.assertTrue(all(not row['operations'] for row in cleaned['sentences']))
        self.assertTrue(all(row['status']=='no_action' for row in cleaned['sentences']))

    def test_sparse_mechanical_strips_preserve_rest(self):
        from spatial import mechanical_strips,outpaint_canvas
        base=np.zeros((400,600,3),np.uint8)+45
        expanded,box=outpaint_canvas(base,'side');expanded[:]=170
        out,mask,mapping=mechanical_strips(base,expanded,box)
        self.assertTrue(np.array_equal(out[mask==0],base[mask==0]))
        self.assertLess((mask>0).mean(),.32)
        self.assertEqual(len(mapping),4)
        self.assertTrue(all(m['shift_x'] and m['shift_y'] for m in mapping))
        self.assertTrue(np.all(out[mask>0]==170))
