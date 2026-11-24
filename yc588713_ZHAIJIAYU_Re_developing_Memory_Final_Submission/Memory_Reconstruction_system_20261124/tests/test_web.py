import unittest,tempfile,sys,time,zipfile,json
from pathlib import Path
from io import BytesIO
from unittest.mock import patch
from PIL import Image
from fastapi.testclient import TestClient
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import app as web
import series

class WebTests(unittest.TestCase):
    def image(self):
        f=BytesIO();Image.new('RGB',(80,60),(110,130,150)).save(f,format='PNG');return f.getvalue()
    def test_upload_validation_preview_and_owner_isolation(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(web,'UPLOAD_ROOT',Path(tmp)),TestClient(web.app) as client,TestClient(web.app) as other:
            client.get('/');other.get('/')
            bad=client.post('/api/uploads',files={'photo':('secret.env',b'no')});self.assertEqual(bad.status_code,415)
            bad=client.post('/api/uploads',files={'photo':('bad.jpg',b'not image')});self.assertEqual(bad.status_code,400)
            result=client.post('/api/uploads',files={'photo':('photo.png',self.image())})
            self.assertEqual(result.status_code,200);data=result.json();self.assertEqual(data['width'],80)
            self.assertEqual(client.get(data['preview']).status_code,200)
            self.assertEqual(other.get(data['preview']).status_code,404)
            self.assertEqual(client.post('/api/jobs',json={'upload_id':data['id'],'memory':'   '}).status_code,422)
    def test_real_adapter_streams_stages_and_download_without_public_paths(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(web,'UPLOAD_ROOT',Path(tmp)/'uploads'),TestClient(web.app) as client,TestClient(web.app) as other:
            root=Path(tmp);client.get('/');other.get('/')
            upload=client.post('/api/uploads',files={'photo':('photo.png',self.image())}).json()
            def pipeline(photo,memory):
                first=root/'step.png';first.write_bytes(self.image())
                yield dict(status='第一步',images=[str(first)],labels=['第 1 步'],total=3,composite=None,archive=None)
                archive=root/'results.zip';archive.write_bytes(b'zip-test')
                yield dict(status='完成',images=[str(first)],labels=['第 1 步'],composite=str(first),archive=str(archive))
            with patch.object(web,'generate_series',side_effect=pipeline):
                jid=client.post('/api/jobs',json={'upload_id':upload['id'],'memory':'我记得更暖'}).json()['id']
                for _ in range(100):
                    state=client.get('/api/jobs/'+jid).json()
                    if state['phase']=='complete':break
                    time.sleep(.01)
            self.assertEqual(state['phase'],'complete');self.assertEqual(state['total'],1)
            self.assertNotIn(str(root),json.dumps(state))
            self.assertEqual(client.get(state['images'][0]).status_code,200)
            self.assertEqual(other.get(state['images'][0]).status_code,404)
            self.assertEqual(client.get(state['archive']).content,b'zip-test')
    def test_zip_includes_exact_original_and_memory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);run=root/'run_01';run.mkdir()
            original=root/'source.png';original.write_bytes(self.image())
            (run/'step.png').write_bytes(self.image())
            report={'execution':[dict(status='success',image='step.png',source='回忆',operation={'name':'exposure'})]}
            result=series.package_stages(root,original,'原始文字\n第二行',run,report)
            with zipfile.ZipFile(result['archive']) as z:
                self.assertEqual(z.read('original_upload.png'),original.read_bytes())
                self.assertEqual(z.read('memory.txt').decode(),'原始文字\n第二行')
                self.assertIn('result_01.png',z.namelist());self.assertIn('composite.png',z.namelist())
if __name__=='__main__':unittest.main()
