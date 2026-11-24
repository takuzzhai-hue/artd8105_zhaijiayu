import unittest,sys,tempfile,json
from pathlib import Path
from unittest.mock import patch
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import generation as g
from analyze_memory import validate_analysis
from style import gentle_analysis,expand_media_stages
from photo_pipeline import run_stream,apply_preview

class GenerationTests(unittest.TestCase):
    def setUp(self):
        self.memory='颜色冷一点，那里本来还有一个杯子。'
        self.plan=dict(id='addition_01',source='那里本来还有一个杯子',object='杯子',kind='object',explicit_positive=True,absent=True,box=[.2,.2,.5,.6],reason='原话明确，当前缺失')
        self.image=np.full((100,120,3),70,np.uint8)
        self.gate=dict(explicit_positive=True,absent=True,kind='object',reason='原话明确')
        self.good=dict(object_matches=True,no_extra_objects=True,style_matches=True,placement_natural=True,face_rule_ok=True,passed=True,reason='通过')
    def test_foreground_finger_rejects_tiny_distant_box_and_repairs_plan(self):
        memory='我当时用食指触摸了建筑轮廓，我想把食指保留下来'
        tiny={**self.plan,'source':memory,'object':'食指','kind':'hand','box':[.32,.41,.35,.44]}
        large={**tiny,'box':[.35,.4,.6,1],'tip':[.475,.425],'entry_edge':'bottom'}
        approved,rejected=g.validate_plan({'additions':[tiny]},memory)
        self.assertFalse(approved);self.assertTrue(rejected)
        with tempfile.TemporaryDirectory() as tmp,patch.object(g,'vision_json',side_effect=[{'additions':[tiny]},{'additions':[large]}]) as call:
            result=g.plan_additions(Image.fromarray(self.image),memory,Path(tmp))
        self.assertEqual(call.call_count,2);np.testing.assert_allclose(result[0]['box'],large['box'])
        self.assertEqual(result[0]['entry_edge'],'bottom')
    def test_hand_can_enter_frame_without_fading_at_wrist(self):
        mask=g.edit_mask((100,120,3),[.3,.4,.6,1])
        self.assertEqual(mask[-1,54],1)
        self.assertEqual(mask[0,54],0)

    def test_local_illumination_matches_dark_background_without_changing_source(self):
        original=np.full((100,120,3),25,np.uint8)
        generated=np.full_like(original,100);generated[40:60,50:70]=240
        mask=np.zeros((100,120),np.float32);mask[40:60,50:70]=1
        result,gain=g.match_local_light(generated,original,mask)
        self.assertEqual(gain,.25);self.assertEqual(result[50,60,0],60)
        self.assertTrue(np.all(original==25))

    def test_foreground_hand_tip_is_not_cut_at_plan_box(self):
        plan={**self.plan,'source':'我用食指触摸建筑','object':'食指','kind':'hand','box':[.35,.4,.6,1],'tip':[.475,.425],'entry_edge':'bottom'}
        mask=np.zeros((100,120),np.float32);mask[37:,44:70]=1
        generated=np.full_like(self.image,70);generated[mask>0]=200
        with tempfile.TemporaryDirectory() as tmp,patch.object(g,'vision_json',return_value={**self.gate,'kind':'hand'}),patch.object(g,'edit_image',return_value=(Image.fromarray(generated),'fake')),patch.object(g,'isolate_object',return_value=mask),patch.object(g,'match_local_light',return_value=(generated,1)),patch.object(g,'review_candidate',return_value=self.good):
            out,meta=g.generate_addition(self.image,plan,plan['source'],Path(tmp)/'gen')
        self.assertGreater(out[38,55,0],70)
        self.assertEqual(out[0,0,0],70)

    def test_finger_segmentation_requests_connected_whole_hand(self):
        mask=np.zeros((100,120),np.float32);mask[40:,40:80]=1
        plan={**self.plan,'object':'食指','kind':'hand'}
        with tempfile.TemporaryDirectory() as tmp,patch.object(g,'vision_json',return_value={'found':True,'box_1000':[330,400,670,1000]}) as vision,patch('segmentation.segment_regions',return_value=({'食指':mask},[])):
            g.isolate_object(Image.fromarray(self.image),plan,Path(tmp))
        self.assertIn('不能只框食指',vision.call_args.args[0])
        self.assertIn('手掌',vision.call_args.args[0])

    def test_generated_object_coordinates_are_normalized_before_segmentation(self):
        mask=np.zeros((100,120),np.float32);mask[47:59,54:64]=1
        with tempfile.TemporaryDirectory() as tmp,patch.object(g,'vision_json',return_value={'found':True,'box_1000':[450,470,530,590]}),patch('segmentation.segment_regions',return_value=({'杯子':mask},[])) as segment:
            result=g.isolate_object(Image.fromarray(self.image),self.plan,Path(tmp))
        self.assertEqual(segment.call_args.args[1][0]['box'],[.45,.47,.53,.59])
        self.assertGreater(result.sum(),mask.sum())
        self.assertEqual(result[0,0],0)

    def test_request_uses_crop_reference_and_disables_prompt_extension(self):
        from unittest.mock import MagicMock
        from io import BytesIO
        crop=Image.new('RGB',(160,80),'gray')
        buf=BytesIO();Image.new('RGB',(1024,512),'gray').save(buf,format='PNG')
        response=MagicMock(status_code=200)
        response.json.return_value={'output':{'choices':[{'message':{'content':[{'text':'done'},{'image':'https://test.oss-cn-beijing.aliyuncs.com/test.png'}]}}]}}
        download=MagicMock(status_code=200);download.__enter__.return_value=download
        download.iter_content.return_value=[buf.getvalue()]
        with patch.object(g,'settings',return_value=('test-key','https://dashscope.aliyuncs.com/compatible-mode/v1')),patch.object(g.requests,'post',return_value=response) as post,patch.object(g.requests,'get',return_value=download):
            result,model=g.edit_image(crop,'只增加杯子',123,reference=Image.fromarray(self.image))
        self.assertEqual(result.size,crop.size)
        payload=post.call_args.kwargs['json']
        self.assertFalse(payload['parameters']['prompt_extend']);self.assertEqual(payload['parameters']['n'],1)
        self.assertEqual(payload['parameters']['seed'],123)
        self.assertEqual(len(payload['input']['messages'][0]['content']),3)
        import base64
        encoded=payload['input']['messages'][0]['content'][1]['image'].split(',',1)[1]
        with Image.open(BytesIO(base64.b64decode(encoded))) as upload:self.assertGreaterEqual(min(upload.size),384)

    def test_plan_does_not_authorize_invented_or_existing_objects(self):
        for patch_values in ({'object':'花瓶'},{'source':'我想要杯子'},{'absent':False},{'explicit_positive':False},{'box':[0,0,1,1]}):
            p={**self.plan,**patch_values};approved,rejected=g.validate_plan({'additions':[p]},self.memory)
            self.assertFalse(approved);self.assertTrue(rejected)
        self.assertEqual(g.validate_plan({'additions':[]},'冷一点')[0],[])
    def test_translation_cannot_bypass_authorized_plan(self):
        row=dict(source=self.memory,intent='添加',status='proposed',reason='新增',operations=[dict(name='generate_add',parameters={'request_id':'addition_01'},region=None)])
        with self.assertRaises(ValueError): validate_analysis({'sentences':[row]},self.memory,[])
        validate_analysis({'sentences':[row]},self.memory,[],[self.plan])
    def test_negative_gate_never_calls_image_generator(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(g,'vision_json',return_value={**self.gate,'explicit_positive':False}),patch.object(g,'edit_image') as edit:
            with self.assertRaises(ValueError):g.generate_addition(self.image,self.plan,self.memory,Path(tmp)/'gen')
            edit.assert_not_called()
    def test_failed_review_retries_from_same_input_and_limits_region(self):
        bad={**self.good,'passed':False,'object_matches':False,'reason':'对象不符'}
        with tempfile.TemporaryDirectory() as tmp,patch.object(g,'vision_json',return_value=self.gate),patch.object(g,'edit_image',side_effect=lambda image,*args,**kwargs:(Image.new('RGB',image.size,'white'),'fake')) as edit,patch.object(g,'review_candidate',side_effect=[bad,self.good]),patch.object(g,'isolate_object',side_effect=lambda im,*args:np.ones((im.height,im.width),np.float32)):
            result,meta=g.generate_addition(self.image,self.plan,self.memory,Path(tmp)/'gen')
            self.assertEqual(edit.call_count,2)
            for call in edit.call_args_list: np.testing.assert_array_equal(np.asarray(call.kwargs['reference']),self.image)
            self.assertEqual(edit.call_args_list[0].args[0].tobytes(),edit.call_args_list[1].args[0].tobytes())
            self.assertNotEqual(edit.call_args_list[0].args[2],edit.call_args_list[1].args[2])
            mask=g.edit_mask(self.image.shape,self.plan['box'])
            np.testing.assert_array_equal(result[mask==0],self.image[mask==0])
            self.assertEqual(len(meta['attempts']),2)
    def test_two_rejections_never_accept_candidate(self):
        bad={**self.good,'passed':False,'reason':'新增真实脸不允许'}
        with tempfile.TemporaryDirectory() as tmp,patch.object(g,'vision_json',return_value=self.gate),patch.object(g,'edit_image',side_effect=lambda image,*args,**kwargs:(Image.new('RGB',image.size,'white'),'fake')) as edit,patch.object(g,'review_candidate',return_value=bad),patch.object(g,'isolate_object',side_effect=lambda im,*args:np.ones((im.height,im.width),np.float32)):
            folder=Path(tmp)/'gen'
            with self.assertRaises(ValueError): g.generate_addition(self.image,self.plan,self.memory,folder)
            self.assertEqual(edit.call_count,2);self.assertFalse((folder/'accepted.png').exists())
    def test_face_never_calls_image_generator(self):
        plan={**self.plan,'source':'本来还有一张脸','object':'脸','kind':'face'}
        with tempfile.TemporaryDirectory() as tmp,patch.object(g,'vision_json',return_value={**self.gate,'kind':'face'}),patch.object(g,'edit_image') as edit,patch.object(g,'review_candidate',return_value=self.good):
            result,meta=g.generate_addition(self.image,plan,'本来还有一张脸',Path(tmp)/'gen')
            edit.assert_not_called();self.assertEqual(meta['kind'],'face');self.assertEqual(result.max(),255)
    def test_single_generation_between_cumulative_effects(self):
        rows=[dict(source=self.memory,intent='颜色',status='proposed',reason='调色',operations=[dict(name='white_balance',parameters={'amount':-.08},region=None),dict(name='generate_add',parameters={'request_id':'addition_01'},region=None),dict(name='contrast',parameters={'amount':.12},region=None)])]
        analysis={'sentences':rows};captured=[]
        def generate(current,*args):
            captured.append(current.copy());out=current.copy();out[30:40,40:50]=200
            return out,dict(object='杯子')
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);photo=root/'in.png';Image.fromarray(self.image).save(photo)
            with patch('photo_pipeline.plan_additions',return_value=[self.plan]),patch('photo_pipeline.segment_regions',return_value=({},[])),patch('photo_pipeline.analyze',return_value=analysis),patch('photo_pipeline.generate_addition',side_effect=generate) as mocked:
                events=list(run_stream(photo,self.memory,root/'run',observation_override={'regions':[]}))
            steps=[e for e in events if e['kind']=='step'];self.assertEqual(len(steps),3);self.assertEqual(mocked.call_count,1)
            np.testing.assert_array_equal(captured[0],np.asarray(Image.open(steps[0]['image'])))
            second=np.asarray(Image.open(steps[1]['image']));third=np.asarray(Image.open(steps[2]['image']))
            np.testing.assert_array_equal(third,apply_preview(second,rows[0]['operations'][2]))
    def test_no_proposal_no_generation(self):
        analysis={'sentences':[dict(source='冷一点',intent='调色',status='proposed',reason='按原话',operations=[dict(name='white_balance',parameters={'amount':-.08},region=None)])]}
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);photo=root/'in.png';Image.fromarray(self.image).save(photo)
            with patch('photo_pipeline.plan_additions',return_value=[]),patch('photo_pipeline.segment_regions',return_value=({},[])),patch('photo_pipeline.analyze',return_value=analysis),patch('photo_pipeline.generate_addition') as generate:
                list(run_stream(photo,'冷一点',root/'run',observation_override={'regions':[]}))
                generate.assert_not_called()



    def test_empty_plan_is_rechecked_for_missed_memory(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(g,'vision_json',side_effect=[{'additions':[],'summary':'没有'}, {'additions':[self.plan],'summary':'回忆中有杯子'}]) as call:
            plans=g.plan_additions(Image.fromarray(self.image),self.memory,Path(tmp))
            self.assertEqual(call.call_count,2);self.assertEqual(plans[0]['object'],'杯子')
            self.assertEqual(len(json.loads((Path(tmp)/'addition_plan.json').read_text())['audit']),2)

    def test_empty_after_review_stays_empty(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(g,'vision_json',return_value={'additions':[],'summary':'我想喝咖啡没有授权补入'}) as call:
            plans=g.plan_additions(Image.fromarray(self.image),'我想喝咖啡',Path(tmp))
            self.assertEqual(plans,[]);self.assertEqual(call.call_count,2)

    def test_retry_error_preserves_approved_plan(self):
        bad={**self.plan,'object':'未提及对象'}
        with tempfile.TemporaryDirectory() as tmp,patch.object(g,'vision_json',side_effect=[{'additions':[self.plan,bad]},ValueError('network')]):
            plans=g.plan_additions(Image.fromarray(self.image),self.memory,Path(tmp))
            self.assertEqual(len(plans),1)

    def test_text_analysis_failure_does_not_drop_approved_addition(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);photo=root/'source.png';Image.fromarray(self.image).save(photo)
            with patch('photo_pipeline.plan_additions',return_value=[self.plan]),patch('photo_pipeline.plan_spatial',return_value=None),patch('photo_pipeline.segment_regions',return_value=({},[])),patch('photo_pipeline.analyze',side_effect=ValueError('bad JSON')),patch('photo_pipeline.generate_addition',return_value=(self.image+10,{'object':'杯子','generated':True})) as generate:
                events=list(run_stream(photo,self.memory,root/'run',observation_override={'regions':[]}))
            self.assertEqual(generate.call_count,1)
            self.assertEqual(len([e for e in events if e['kind']=='step']),1)

if __name__=='__main__': unittest.main()
