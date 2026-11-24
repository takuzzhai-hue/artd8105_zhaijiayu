import unittest
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from operations import OPERATIONS,validate_operation
from media_effects import MEDIA_NAMES,disappearance_mask
from photo_pipeline import apply_preview,run_stream
from style import gentle_analysis,expand_media_stages

class MediaTests(unittest.TestCase):
    def setUp(self):
        y,x=np.indices((80,120));self.image=np.stack([(x*13+y*7)%256,(x*3+y*19)%256,(x*11+y*5)%256],axis=2).astype(np.uint8)
        self.mask=np.zeros((80,120),np.float32);self.mask[20:60,40:80]=1
    def op(self,name):
        return dict(name=name,parameters={k:r['default'] for k,r in OPERATIONS[name]['parameters'].items()},region='主体' if OPERATIONS[name]['type']=='local' else None)
    def test_all_renderers_valid_deterministic_and_zero_identity(self):
        for name in sorted(MEDIA_NAMES):
            with self.subTest(name=name):
                op=self.op(name);validate_operation(op,['主体'])
                out=apply_preview(self.image,op,{'主体':self.mask})
                self.assertEqual(out.shape,self.image.shape)
                self.assertEqual(out.dtype,np.uint8)
                self.assertFalse(np.array_equal(out,self.image))
                np.testing.assert_array_equal(out,apply_preview(self.image,op,{'主体':self.mask}))
                op['parameters']['amount']=0
                np.testing.assert_array_equal(apply_preview(self.image,op,{'主体':self.mask}),self.image)
    def test_focus_preserves_new_target_blurs_outside(self):
        out=apply_preview(self.image,self.op('focus_pull'),{'主体':self.mask})
        np.testing.assert_array_equal(out[self.mask==1],self.image[self.mask==1])
        self.assertFalse(np.array_equal(out[self.mask==0],self.image[self.mask==0]))
    def test_local_white_expands_and_feathers(self):
        op=self.op('local_overexposure');op['parameters']['amount']=1
        out=apply_preview(self.image,op,{'主体':self.mask})
        self.assertTrue(np.all(out[self.mask==1]==255))
        halo=disappearance_mask(self.mask)
        self.assertTrue(np.any((halo>0)&(self.mask==0)))
        self.assertTrue(np.any((halo>0)&(halo<1)))
        np.testing.assert_array_equal(out[halo==0],self.image[halo==0])
        self.assertTrue(np.all(out[halo==1]==255))
        self.assertEqual(self.mask.sum(),1600)
        np.testing.assert_array_equal(disappearance_mask(np.zeros_like(self.mask)),np.zeros_like(self.mask))
    def test_extreme_global_effects_preserve_details(self):
        for name in ('overexposure','underexposure','defocus_bloom','local_overexposure'):
            op=self.op(name);op['parameters']['amount']=1
            out=apply_preview(self.image,op,{'主体':np.ones_like(self.mask)})
            self.assertGreater(float(out.std()),8)
            self.assertFalse(np.all(out==255))
            self.assertFalse(np.all(out==0))
    def test_enum_validation(self):
        op=self.op('pixel_sort');op['parameters']['direction']='diagonal'
        with self.assertRaises(ValueError): validate_operation(op)
    def test_white_progression_pipeline(self):
        op=self.op('overexposure');op['parameters']['amount']=1
        analysis={'sentences':[dict(source='隐藏这张照片',intent='隐藏',reason='白化模拟',status='proposed',operations=[op])]}
        expanded=expand_media_stages(gentle_analysis(analysis))
        self.assertEqual(len(expanded['sentences'][0]['operations']),1)
        self.assertEqual(analysis['sentences'][0]['operations'][0]['parameters']['amount'],1)
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);photo=root/'input.png';Image.fromarray(self.image).save(photo)
            with patch('photo_pipeline.plan_additions',return_value=[]),patch('photo_pipeline.segment_regions',return_value=({},[])),patch('photo_pipeline.analyze',return_value=analysis):
                events=list(run_stream(photo,'隐藏这张照片',root/'run',observation_override={'regions':[]}))
            paths=[event['image'] for event in events if event['kind']=='step']
            self.assertEqual(len(paths),1)
            images=[np.array(Image.open(path)) for path in paths]
            self.assertTrue(all(not np.array_equal(a,b) for a,b in zip([self.image]+images,images)))
            self.assertGreater(float(images[-1].std()),10)
            self.assertFalse(np.all(images[-1]==255))
            self.assertTrue(all(row['simulated'] for row in events[-1]['report']['execution']))

if __name__=='__main__': unittest.main()
