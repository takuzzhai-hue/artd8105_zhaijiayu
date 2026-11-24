import unittest,tempfile,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from style import gentle_analysis
from series import compose
from PIL import Image
import numpy as np
class StyleTests(unittest.TestCase):
    def test_visible_but_restrained_global_and_local_adjustments(self):
        ops=[dict(name=name,region=region,parameters={param:value}) for name,region,param,value in [
            ('exposure',None,'stops',.25),('local_exposure','树','stops',-.25),
            ('contrast',None,'amount',.25),('local_contrast','树','amount',.25),
            ('local_brighten','天空','stops',.8)]]
        a={'sentences':[dict(source='亮一点，对比度强一点',status='proposed',reason='',operations=ops)]}
        result=gentle_analysis(a)['sentences'][0]['operations']
        self.assertEqual([next(iter(op['parameters'].values())) for op in result],[.25,-.25,.25,.25,.25])
    def test_gentle(self):
        a={'sentences':[{'status':'proposed','reason':'','operations':[{'name':'white_balance','region':None,'parameters':{'amount':.9}}]}]}
        b=gentle_analysis(a)
        self.assertEqual(b['sentences'][0]['operations'][0]['parameters']['amount'],.10)
        self.assertEqual(a['sentences'][0]['operations'][0]['parameters']['amount'],.9)
    def test_order_width(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);paths=[]
            for i in range(3):
                p=root/f'{i}.png';Image.new('RGB',(7,5),(50*(i+1),0,0)).save(p);paths.append(p)
            mapping=compose(Image.new('RGB',(19,11),(0,0,0)),paths,root/'out.png')
            a=np.array(Image.open(root/'out.png'))
            self.assertEqual(a.shape,(11,19,3))
            self.assertEqual([r['end']-r['start'] for r in mapping],[4,5,5,5])
            for i,r in enumerate(mapping): self.assertTrue(np.all(a[:,r['start']:r['end'],0]==i*50))
