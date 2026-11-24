from test_web import WebTests
import app as web
import unittest,tempfile,time
from pathlib import Path
from unittest.mock import patch
from fastapi.testclient import TestClient
class PhoneTests(unittest.TestCase):
 def test_phone_transfer_is_single_use_and_private(self):
  with tempfile.TemporaryDirectory() as tmp,patch.object(web,'UPLOAD_ROOT',Path(tmp)),patch.object(web,'phone_host',return_value='192.168.1.20'),TestClient(web.app) as pc,TestClient(web.app) as mobile,TestClient(web.app) as stranger:
   pc.get('/');mobile.get('/phone');stranger.get('/')
   data=pc.post('/api/phone-pairs').json();pid=data['id'];token=web.PAIRS[pid]['token'];endpoint=f'/api/phone-pairs/{pid}'
   self.assertEqual(pc.get(data['qr']).status_code,200)
   self.assertEqual(stranger.get(endpoint).status_code,404)
   payload={'photo':('image.png',WebTests().image())}
   self.assertEqual(mobile.post(endpoint+'/upload',files=payload).status_code,404)
   self.assertEqual(mobile.post(endpoint+'/upload',headers={'X-Upload-Token':token},files=payload).status_code,200)
   got=pc.get(endpoint).json();self.assertEqual(got['state'],'received')
   self.assertEqual(pc.get(got['photo']['preview']).status_code,200)
   self.assertEqual(mobile.get(got['photo']['preview']).status_code,404)
   self.assertEqual(mobile.post(endpoint+'/upload',headers={'X-Upload-Token':token},files=payload).status_code,409)
   new=pc.post('/api/phone-pairs').json();self.assertNotEqual(new['id'],pid);self.assertEqual(pc.get(endpoint).json()['state'],'received')
   web.PAIRS[new['id']]['expires']=time.time()-1
   self.assertEqual(pc.get('/api/phone-pairs/'+new['id']).json()['state'],'expired')

 def test_switching_to_hotspot_refreshes_qr_and_accepts_new_host(self):
  with patch.object(web,'PUBLIC_BASE',''),patch.object(web,'phone_host',return_value='192.168.1.20') as address,TestClient(web.app) as pc:
   first=pc.post('/api/phone-pairs').json()
   address.return_value='172.20.10.2'
   self.assertEqual(pc.get('/api/phone-pairs/'+first['id']).json()['state'],'expired')
   second=pc.post('/api/phone-pairs').json()
   self.assertTrue(web.PAIRS[second['id']]['url'].startswith('http://172.20.10.2:7860/phone#'))
   self.assertEqual(pc.get('/phone',headers={'Host':'172.20.10.2:7860'}).status_code,200)
   self.assertEqual(pc.get('/phone',headers={'Host':'192.168.1.20:7860'}).status_code,400)
   self.assertEqual(pc.get('/phone',headers={'Host':'unrelated.example'}).status_code,400)

 def test_multiple_tabs_keep_scanned_pair_valid(self):
  with tempfile.TemporaryDirectory() as tmp,patch.object(web,'UPLOAD_ROOT',Path(tmp)),patch.object(web,'PUBLIC_BASE',''),patch.object(web,'phone_host',return_value='192.168.1.20'),TestClient(web.app) as pc,TestClient(web.app) as mobile:
   first=pc.post('/api/phone-pairs').json();pid=first['id']
   token=web.PAIRS[pid]['token']
   for _ in range(8):
    self.assertEqual(pc.post('/api/phone-pairs').json()['id'],pid)
    self.assertEqual(pc.get('/api/phone-pairs/'+pid).json()['state'],'waiting')
   result=mobile.post('/api/phone-pairs/'+pid+'/upload',headers={'X-Upload-Token':token},files={'photo':('test.png',WebTests().image())})
   self.assertEqual(result.status_code,200)
   pc.post('/api/phone-pairs')
   self.assertEqual(pc.get('/api/phone-pairs/'+pid).json()['state'],'received')

 def test_temporary_address_lookup_failure_does_not_expire_pair(self):
  with patch.object(web,'PUBLIC_BASE',''),patch.object(web,'phone_host',return_value='192.168.1.20') as address,TestClient(web.app) as pc:
   pid=pc.post('/api/phone-pairs').json()['id']
   address.return_value=None
   self.assertEqual(pc.get('/api/phone-pairs/'+pid).json()['state'],'waiting')
