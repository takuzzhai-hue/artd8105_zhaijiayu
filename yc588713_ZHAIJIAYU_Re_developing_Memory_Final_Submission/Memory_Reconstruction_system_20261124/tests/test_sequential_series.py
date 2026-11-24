import unittest,tempfile,sys,json
from pathlib import Path
from unittest.mock import patch
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import series
class SequentialTests(unittest.TestCase):
    def test_each_result_is_each_step_and_run_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);source=root/'input.png';Image.new('RGB',(20,10),'white').save(source)
            def fake(photo,memory,output_dir):
                output_dir.mkdir();records=[]
                for i in range(1,4):
                    Image.new('RGB',(20,10),(30*i,0,0)).save(output_dir/f'step_{i:02d}.png')
                    records.append(dict(status='success',image=f'step_{i:02d}.png',source='测试',operation={'name':'contrast'}))
                    yield dict(kind='step',image=str(output_dir/f'step_{i:02d}.png'),source='测试',operation='contrast')
                yield dict(kind='complete',folder=output_dir,report={'execution':records})
            with patch.object(series,'PROJECT',root),patch.object(series,'run_stream',side_effect=fake) as call:
                states=list(series.generate_series(source,'测试'));result=states[-1]
            self.assertEqual([len(s['images']) for s in states if '步已完成：' in s['status']],[1,2,3])
            self.assertTrue(all(s['composite'] is None for s in states[:-1]))
            self.assertEqual(call.call_count,1)
            self.assertEqual(len(result['images']),3)
            for i,p in enumerate(result['images'],1):
                p=Path(p)
                self.assertEqual(p.read_bytes(),(p.parent/'run_01'/f'step_{i:02d}.png').read_bytes())
            self.assertTrue(Path(result['composite']).exists())
