import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from style import gentle_analysis,expand_media_stages
class MildDarkTests(unittest.TestCase):
    def test_underexposure_does_not_expand(self):
        a={'sentences':[dict(source='当时应该更暗一点，是很幽深的树林',status='proposed',reason='',operations=[dict(name=n,parameters=p,region=None) for n,p in [('underexposure',{'amount':.75}),('exposure',{'stops':-.4}),('vignette',{'amount':.1})]])]}
        result=expand_media_stages(gentle_analysis(a))
        ops=result['sentences'][0]['operations']
        self.assertEqual(ops,[dict(name='exposure',parameters={'stops':-.25},region=None)])
    def test_explicit_strong_effect_preserved(self):
        a={'sentences':[dict(source='主体沉入黑色，细节消失',status='proposed',reason='',operations=[dict(name='underexposure',parameters={'amount':.75},region=None)])]}
        self.assertEqual(gentle_analysis(a)['sentences'][0]['operations'][0]['name'],'underexposure')
