import sys,unittest
from pathlib import Path
from unittest.mock import patch,MagicMock
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from pipeline_effects import apply,sites,RAW_NAMES
from operations import OPERATIONS,validate_operation

class PipelineEffectsTests(unittest.TestCase):
 def setUp(self):
  self.image=np.tile(np.arange(20,220,5,dtype=np.uint8)[None,:,None],(32,1,3))
  self.mask=np.zeros(self.image.shape[:2],np.float32);self.mask[8:24,10:25]=1
 def op(self,name):
  s=OPERATIONS[name];return dict(name=name,parameters={k:v['default'] for k,v in s['parameters'].items()},region='target' if s['type']=='local' else None)
 def test_rgb_effects_locality_and_not_blank(self):
  for name in ('faded_fog','linear_negative','local_linear_negative','local_exposure_erase'):
   op=self.op(name);validate_operation(op,['target'])
   out,meta=apply(self.image,op,'test.jpg',{'target':self.mask})
   self.assertEqual(meta['category'],'E');self.assertFalse(np.array_equal(out,self.image))
   self.assertGreater(out.std(),1)
   if name=='local_linear_negative': np.testing.assert_array_equal(out[self.mask==0],self.image[self.mask==0])
 def test_nonraw_cannot_fake_sensor(self):
  for name in RAW_NAMES:
   with self.assertRaisesRegex(ValueError,'原始RAW'): apply(self.image,self.op(name),'test.jpg',{'target':self.mask})
 def test_sensor_uses_actual_filter_and_orientation(self):
  raw=MagicMock();raw.raw_image_visible=np.full((8,12),1000);raw.raw_pattern=np.array([[0,1],[3,2]])
  raw.raw_colors_visible=np.tile(raw.raw_pattern,(4,6));raw.color_desc=b'RGBG';raw.black_level_per_channel=[0]*4;raw.white_level=1000;raw.sizes.flip=0
  result=sites(raw,(8,12,3),1)
  np.testing.assert_allclose(result[0,0],[1,0,0],atol=1e-6)
  np.testing.assert_allclose(result[1,1],[0,0,1],atol=1e-6)
  raw.sizes.flip=6
  np.testing.assert_allclose(sites(raw,(12,8,3),1),np.rot90(result,-1),atol=1e-6)
 def test_raw_variant_preserves_prior_change(self):
  raw=MagicMock();raw.__enter__.return_value=raw;raw.sizes.width=80;raw.sizes.height=64
  base=np.full(self.image.shape,.3,np.float32);variant=np.full(self.image.shape,.4,np.float32)
  op=self.op('raw_demosaic_linear');op['parameters']['amount']=1
  with patch('pipeline_effects.rawpy.imread',return_value=raw),patch('pipeline_effects.develop',side_effect=[base,variant]):
   out,meta=apply(np.full(self.image.shape,.5,np.float32),op,'test.dng')
  np.testing.assert_allclose(out,.585,atol=1e-6);self.assertEqual(meta['category'],'R+E')
 def test_single_frame_cannot_remove_people(self):
  op=dict(name='multi_frame_median',parameters={'frames':[]},region=None)
  with self.assertRaisesRegex(ValueError,'多帧来源'): apply(self.image,op,'test.dng')
  with self.assertRaisesRegex(ValueError,'至少'): apply(self.image,op,'test.dng',allow_frames=True)
 def test_full_mask_exposure_retains_texture(self):
  op=self.op('local_exposure_erase');op['parameters']['stops']=8
  out,_=apply(self.image,op,'test.jpg',{'target':np.ones_like(self.mask)})
  self.assertGreater(out.std(),2);self.assertFalse(np.all(out==255))
 def test_sampling_is_captured_before_raw_processing(self):
  raw=MagicMock();raw.__enter__.return_value=raw;raw.sizes.width=80;raw.sizes.height=64
  op=self.op('sensor_sites');order=[]
  def sampling(*args): order.append('sampling');return np.full(self.image.shape,.2,np.float32)
  def development(*args,**kwargs): order.append('development');return np.full(self.image.shape,.3,np.float32)
  with patch('pipeline_effects.rawpy.imread',return_value=raw),patch('pipeline_effects.sites',side_effect=sampling),patch('pipeline_effects.develop',side_effect=development):
   apply(self.image,op,'test.dng')
  self.assertEqual(order,['sampling','development'])
 def test_multiframe_median_removes_transient_patch(self):
  from pipeline_effects import median_frames
  a=np.full((20,30,3),.2,np.float32);b=a.copy();c=a.copy();b[3:6,4:9]=.9
  raw=MagicMock();raw.__enter__.return_value=raw
  with patch('pipeline_effects.rawpy.imread',return_value=raw),patch('pipeline_effects.develop',side_effect=[a,b,c]),patch('pipeline_effects.cv2.findTransformECC',return_value=(.99,np.eye(2,3,dtype=np.float32))):
   _,out=median_frames(['a.dng','b.dng','c.dng'],a.shape)
  np.testing.assert_allclose(out,a)
