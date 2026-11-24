import sys
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from segmentation import check_mask,segment_regions

class SegmentationTests(unittest.TestCase):
    def test_mask_checks(self):
        mask=np.zeros((100,100),bool);mask[30:50,30:50]=True
        self.assertEqual(check_mask(mask,[.25,.25,.55,.55],.9).sum(),400)
        for invalid,box,score in [(mask,[0,0,.1,.1],.9),(mask,[.25,.25,.55,.55],.2),(np.zeros_like(mask),[0,0,1,1],.9)]:
            with self.assertRaises(ValueError): check_mask(invalid,box,score)
    def test_no_rectangle_fallback(self):
        with tempfile.TemporaryDirectory() as tmp,patch('segmentation.load_model',side_effect=OSError('missing model')):
            masks,records=segment_regions(Image.new('RGB',(100,100)),[{'name':'钟摆','box':[.2,.2,.5,.5]}],tmp)
            self.assertEqual(masks,{})
            self.assertEqual(records[0]['status'],'unavailable')
            self.assertFalse(list(Path(tmp).glob('*mask.png')))

if __name__=='__main__': unittest.main()

class ShadowTests(unittest.TestCase):
    def test_shadow_selection_is_not_rectangle(self):
        image=np.full((100,100,3),210,np.uint8)
        image[30:60,30:60]=30
        with tempfile.TemporaryDirectory() as tmp,patch('segmentation.load_model',return_value=(None,None)):
            masks,records=segment_regions(Image.fromarray(image),[{'name':'树影','box':[.2,.2,.7,.7],'selection':'shadows','method':'luminance'}],tmp)
            self.assertEqual(records[0]['status'],'success')
            self.assertEqual(records[0]['method'],'luminance')
            self.assertGreater(masks['树影'][40,40],.9)
            self.assertEqual(masks['树影'][90,90],0)
