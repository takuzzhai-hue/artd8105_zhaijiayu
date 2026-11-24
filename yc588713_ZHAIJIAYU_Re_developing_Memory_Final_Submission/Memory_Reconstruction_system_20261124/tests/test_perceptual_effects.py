import sys,unittest,tempfile
from pathlib import Path
from unittest.mock import patch
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from perceptual_effects import apply,depth_blur
from operations import OPERATIONS,validate_operation

class PerceptualTests(unittest.TestCase):
 def setUp(self):
  yy,xx=np.indices((80,100));self.x=np.stack([(xx*17+yy*9)%255]*3,axis=2).astype(np.uint8)
  self.mask=np.zeros((80,100),np.float32);self.mask[20:60,30:60]=1
 def op(self,name):
  return dict(name=name,region='target',parameters={k:r['default'] for k,r in OPERATIONS[name]['parameters'].items()})
 def test_silhouette_retains_outline_and_background(self):
  op=self.op('local_silhouette');validate_operation(op,['target'])
  out,meta=apply(self.x,op,{'target':self.mask})
  np.testing.assert_array_equal(out[self.mask==0],self.x[self.mask==0])
  self.assertEqual(float(out[self.mask==1].std()),0);self.assertFalse(meta['generated'])
  with self.assertRaises(ValueError):apply(self.x,op,{'target':np.ones_like(self.mask)})
 def test_touch_deterministic_local_and_no_hand(self):
  op=self.op('touch_trace')
  a,meta=apply(self.x,op,{'target':self.mask});b,_=apply(self.x,op,{'target':self.mask})
  np.testing.assert_array_equal(a,b);np.testing.assert_array_equal(a[self.mask==0],self.x[self.mask==0])
  self.assertFalse(np.array_equal(a,self.x));self.assertFalse(meta['generated']);self.assertEqual(meta['category'],'E')
 def test_depth_target_preserved_and_different_depths_blur(self):
  depth=np.full(self.mask.shape,.9,np.float32);depth[self.mask==1]=.2
  with patch('perceptual_effects.estimate_depth',return_value=depth):
   with tempfile.TemporaryDirectory() as folder:
    out,meta=apply(self.x,self.op('depth_focus'),{'target':self.mask},folder=folder)
    self.assertTrue((Path(folder)/'depth_relative.npy').exists())
  np.testing.assert_array_equal(out[self.mask==1],self.x[self.mask==1])
  self.assertFalse(np.array_equal(out[self.mask==0],self.x[self.mask==0]));self.assertNotIn('depth_fallback',meta)
 def test_depth_failure_is_explicit_mask_fallback(self):
  with patch('perceptual_effects.estimate_depth',side_effect=OSError('missing')):
   _,meta=apply(self.x,self.op('depth_focus'),{'target':self.mask})
  self.assertTrue(meta['depth_fallback']);self.assertNotIn('depth_model',meta)
 def test_zero_identity(self):
  for name in ('depth_focus','local_silhouette','touch_trace'):
   op=self.op(name);op['parameters']['amount']=0
   out,_=apply(self.x,op,{'target':self.mask});np.testing.assert_array_equal(out,self.x)
