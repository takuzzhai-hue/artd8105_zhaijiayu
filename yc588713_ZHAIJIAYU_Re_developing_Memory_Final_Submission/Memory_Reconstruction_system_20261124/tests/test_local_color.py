import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import numpy as np
from analyze_memory import validate_analysis
from photo_pipeline import apply_preview
from style import gentle_analysis
class LocalColorTests(unittest.TestCase):
    def test_repair_and_locality(self):
        image=np.full((20,20,3),[90,130,180],np.uint8)
        mask=np.zeros((20,20),np.float32);mask[5:15,5:15]=1
        for name,params,expected in [('saturation',{'amount':.1},'local_saturation'),('white_balance',{'amount':-.04},'local_white_balance'),('local_brighten',{'stops':-.2},'local_exposure')]:
            result={'sentences':[dict(source='树荫',intent='调整',status='proposed',reason='测试',operations=[dict(name=name,parameters=params,region='树荫')])]}
            result=gentle_analysis(validate_analysis(result,'树荫',['树荫']))
            op=result['sentences'][0]['operations'][0]
            self.assertEqual(op['name'],expected)
            output=apply_preview(image,op,{'树荫':mask})
            np.testing.assert_array_equal(output[mask==0],image[mask==0])
            self.assertFalse(np.array_equal(output[mask==1],image[mask==1]))
