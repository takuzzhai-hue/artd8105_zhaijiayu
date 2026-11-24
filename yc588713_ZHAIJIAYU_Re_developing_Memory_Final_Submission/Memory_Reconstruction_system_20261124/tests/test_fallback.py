import sys,tempfile,unittest,json
from pathlib import Path
from unittest.mock import patch
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import series
class FallbackTests(unittest.TestCase):
    def test_api_failures_and_extreme_photos(self):
        for color in (0,128,255):
            for error in (ValueError('API拒绝'),RuntimeError('格式无法解析')):
                with self.subTest(color=color,error=type(error)),tempfile.TemporaryDirectory() as tmp:
                    root=Path(tmp);source=root/'source.png';Image.new('RGB',(40,30),(color,)*3).save(source)
                    with patch.object(series,'PROJECT',root),patch.object(series,'run_stream',side_effect=error):
                        states=list(series.generate_series(source,'无法理解的回忆'))
                    final=states[-1]
                    self.assertEqual(len(final['images']),1)
                    self.assertTrue(Path(final['composite']).exists())
                    previous=np.array(Image.open(source))
                    for p in final['images']:
                        image=np.array(Image.open(p));self.assertFalse(np.array_equal(previous,image));previous=image
                    self.assertTrue(all(s['composite'] is None for s in states[:-1]))
    def test_keep_completed_stage_on_later_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);source=root/'source.png';Image.new('RGB',(40,30),'gray').save(source)
            def failed(photo,memory,output_dir):
                output_dir.mkdir();Image.new('RGB',(40,30),(100,100,100)).save(output_dir/'step_01.png')
                yield dict(kind='step',image=str(output_dir/'step_01.png'),source='变暗',operation='exposure')
                raise RuntimeError('后续操作异常')
            with patch.object(series,'PROJECT',root),patch.object(series,'run_stream',side_effect=failed):
                states=list(series.generate_series(source,'变暗'))
            self.assertEqual(len(states[-1]['images']),1)
            self.assertEqual(Image.open(states[-1]['images'][0]).getpixel((0,0)),(100,100,100))
