import sys,unittest,tempfile,json
from pathlib import Path
from unittest.mock import patch
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from poetic_effects import apply,NAMES
from operations import OPERATIONS,validate_operation
from series import split_narrators,generate_series
from analyze_memory import validate_analysis

class PoeticTests(unittest.TestCase):
 def setUp(self):
  yy,xx=np.indices((100,140));self.x=np.stack([(xx*7+yy*13)%255,(xx*11)%255,(yy*7)%255],axis=2).astype(np.uint8)
  self.m=np.zeros((100,140),np.float32);self.m[30:65,40:80]=1
 def op(self,name):
  spec=OPERATIONS[name]
  return dict(name=name,region='target' if spec['type']=='local' else None,parameters={k:v['default'] for k,v in spec['parameters'].items()})
 def test_all_registered_deterministic_and_zero_identity(self):
  for name in NAMES:
   op=self.op(name);validate_operation(op,['target'])
   validate_analysis({'sentences':[dict(source='test',intent='test',status='proposed',reason='test',operations=[op])]},'test',['target'])
   a,meta=apply(self.x,op,{'target':self.m});b,_=apply(self.x,op,{'target':self.m})
   np.testing.assert_array_equal(a,b);self.assertFalse(meta['generated']);self.assertFalse(np.array_equal(a,self.x))
   op['parameters']['amount']=0;out,_=apply(self.x,op,{});np.testing.assert_array_equal(out,self.x)
 def test_gesture_preserves_target_cutout_preserves_background(self):
  out,_=apply(self.x,self.op('retain_gesture'),{'target':self.m})
  np.testing.assert_array_equal(out[self.m==1],self.x[self.m==1])
  out,_=apply(self.x,self.op('local_cutout'),{'target':self.m})
  np.testing.assert_array_equal(out[self.m==0],self.x[self.m==0]);self.assertTrue(np.all(out[self.m==1]==255))
  with self.assertRaises(ValueError):apply(self.x,self.op('local_cutout'),{'target':np.ones_like(self.m)})
 def test_fragments_only_rearrange_pixels(self):
  out,_=apply(self.x,self.op('memory_fragments'),{})
  self.assertEqual(sorted(map(tuple,out.reshape(-1,3))),sorted(map(tuple,self.x.reshape(-1,3))))
 def test_codes_are_real_current_pixels(self):
  with tempfile.TemporaryDirectory() as d:
   apply(self.x,self.op('image_codes'),{},folder=d)
   data=json.loads((Path(d)/'image_codes.json').read_text())
   for item in data['samples']:
    self.assertEqual(item['rgb'],self.x[item['y'],item['x']].tolist())
    self.assertEqual(item['hex'],''.join(f'{v:02X}' for v in item['rgb']))
 def test_speaker_parse_and_independent_source(self):
  self.assertEqual(split_narrators('我记得她\n\n我也记得天空'),[])
  text='【叙述者：甲】\n只记得手\n【Narrator: B】\nOnly the sky'
  self.assertEqual(len(split_narrators(text)),2)
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);source=root/'photo.png';Image.fromarray(self.x).save(source);calls=[]
   def run(photo,memory):
    calls.append((photo,memory));yield dict(status='done',images=[str(source)],labels=['step'],archive=None)
   with patch('series.PROJECT',root),patch('series._generate_single_series',side_effect=run):
    states=list(generate_series(source,text))
   self.assertEqual([c[0] for c in calls],[source,source]);self.assertTrue(Path(states[-1]['composite']).is_file())
   self.assertEqual(len(states[-1]['images']),2)

if __name__=='__main__':unittest.main()
