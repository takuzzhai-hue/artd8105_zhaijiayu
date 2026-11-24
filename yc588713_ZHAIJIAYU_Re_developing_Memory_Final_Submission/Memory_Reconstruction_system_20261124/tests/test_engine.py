import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys
import numpy as np
import cv2
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from engine import execute
from photo_pipeline import apply_preview

class EngineTests(unittest.TestCase):
    def test_sequential_once_full_size_and_failures(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);source=root/'test.raw';source.write_bytes(b'fixture')
            mask=np.full((24,32),255,np.uint8);cv2.imwrite(str(root/'mask.png'),mask)
            ops=[dict(source='模糊',name='local_blur',parameters={'amount':0.2},region='目标'),
                 dict(source='对比',name='contrast',parameters={'amount':0.1},region=None),
                 dict(source='越界',name='exposure',parameters={'stops':10},region=None),
                 dict(source='空白',name='void',parameters={},region='目标'),
                 dict(source='锐化',name='local_sharpen',parameters={'amount':0.5},region='目标')]
            config=root/'ops.json';config.write_text(json.dumps({'operations':ops,'regions':{'目标':'mask.png'}}))
            raw=MagicMock();raw.__enter__.return_value=raw
            raw.postprocess.return_value=np.arange(24*32*3,dtype=np.uint16).reshape(24,32,3)*20
            with patch('engine.rawpy.imread',return_value=raw):
                folder,report=execute(source,config,True,root/'run')
            self.assertEqual(raw.postprocess.call_count,1)
            self.assertFalse(raw.postprocess.call_args.kwargs['half_size'])
            self.assertEqual([x['status'] for x in report['steps']],['成功','成功','无法执行','成功','与之前的操作冲突'])
            self.assertEqual(report['steps'][1]['sha256'],report['steps'][2]['sha256'])
            self.assertEqual(report['steps'][3]['sha256'],report['steps'][4]['sha256'])
            # 从上一步图像计算对比，允许一次 PNG 量化误差；不能再重放局部模糊。
            first=cv2.cvtColor(cv2.imread(str(folder/'step_01.png'),-1),cv2.COLOR_BGR2RGB).astype(np.float32)/65535
            second=cv2.cvtColor(cv2.imread(str(folder/'step_02.png'),-1),cv2.COLOR_BGR2RGB).astype(np.float32)/65535
            expected=apply_preview(first,{k:ops[1][k] for k in ('name','parameters','region')})
            self.assertLess(float(np.max(abs(expected-second))),3/65535)
            raw.reset_mock()
            with patch('engine.rawpy.imread',return_value=raw):
                _,again=execute(source,config,False,root/'again')
            self.assertTrue(raw.postprocess.call_args.kwargs['half_size'])
            self.assertEqual([s['sha256'] for s in report['steps']],[s['sha256'] for s in again['steps']])

if __name__=='__main__': unittest.main()
