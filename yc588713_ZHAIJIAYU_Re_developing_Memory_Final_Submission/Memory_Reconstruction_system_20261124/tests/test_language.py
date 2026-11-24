import unittest,sys,tempfile
from pathlib import Path
from unittest.mock import patch
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from analyze_memory import validate_analysis
from photo_pipeline import run_stream
from style import gentle_analysis

class LanguageTests(unittest.TestCase):
 def plan(self):
  return {'sentences':[dict(source='slightly darker',intent='exposure',status='proposed',reason='darker',operations=[dict(name='exposure',region=None,parameters={'stops':-.25})]),dict(source='stronger contrast',intent='contrast',status='proposed',reason='contrast',operations=[dict(name='contrast',region=None,parameters={'amount':.25})]),dict(source='film grain',intent='grain',status='proposed',reason='grain',operations=[dict(name='grain_enlargement',region=None,parameters={'amount':.12,'size':.02})]),dict(source='slightly darker',intent='duplicate',status='proposed',reason='already covered',operations=[])]}
 def test_empty_proposal_keeps_valid_english_stages(self):
  memory='slightly darker, stronger contrast, film grain'
  a=gentle_analysis(validate_analysis(self.plan(),memory,[]))
  self.assertEqual(a['sentences'][-1]['status'],'no_action')
  self.assertEqual(sum(len(r['operations']) for r in a['sentences']),3)
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);photo=root/'input.png'
   x=np.tile(np.arange(30,210,dtype=np.uint8),(80,1));Image.fromarray(np.stack([x,x,x],axis=2)).save(photo)
   with patch('photo_pipeline.plan_additions',return_value=[]),patch('photo_pipeline.plan_spatial',return_value=None),patch('photo_pipeline.segment_regions',return_value=({},[])),patch('photo_pipeline.analyze',return_value=a):
    events=list(run_stream(photo,memory,root/'run',observation_override={'regions':[]}))
   steps=[e for e in events if e['kind']=='step']
   self.assertEqual(len(steps),3)
   previous=np.array(Image.open(photo))
   for step in steps:
    current=np.array(Image.open(step['image']));self.assertFalse(np.array_equal(previous,current));previous=current

 def test_noise_emphasis_executes_and_preserves_flat_image(self):
  from photo_pipeline import apply_preview
  op=dict(name='noise_emphasis',parameters={'amount':.25},region=None)
  flat=np.full((32,32,3),100,np.uint8)
  np.testing.assert_array_equal(apply_preview(flat,op),flat)
  textured=flat.copy();textured[::2,::2]=130
  result=apply_preview(textured,op)
  self.assertGreater(float(result.std()),float(textured.std()))
  np.testing.assert_array_equal(result,apply_preview(textured,op))
