import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from analyze_memory import validate_analysis
class SourceTests(unittest.TestCase):
    def row(self,source,status='proposed',stops=-.2):
        return dict(source=source,intent='压暗',reason='按语境理解',status=status,operations=[dict(name='exposure',region=None,parameters={'stops':stops})])
    def test_corrected_typo_binds_real_input(self):
        memory='总觉得应该更按一点'
        result=validate_analysis({'sentences':[self.row('应该更暗一点')]},memory,[])
        self.assertEqual(result['sentences'][0]['source'],memory)
        self.assertIn('未逐字匹配',result['sentences'][0]['reason'])
    def test_invalid_parameters_still_rejected(self):
        with self.assertRaises(ValueError): validate_analysis({'sentences':[self.row('更暗一点',stops=-10)]},'更按一点',[])
    def test_unknown_status_not_silently_executed(self):
        with self.assertRaises(ValueError): validate_analysis({'sentences':[self.row('暗一点',status='unknown')]},'暗一点',[])
