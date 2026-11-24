const $=id=>document.getElementById(id);
const [pair,token]=location.hash.slice(1).split(':');
let file=null,url=null,busy=false;
if(!pair || !token){$('status').textContent='请扫描电脑页面上的二维码进入。';$('pick').disabled=true;}
$('pick').onclick=()=>{if(!busy)$('file').click();};
$('file').onchange=()=>{
 file=$('file').files[0];if(!file)return;
 if(url)URL.revokeObjectURL(url);
 url=URL.createObjectURL(file);$('preview').src=url;$('preview').hidden=false;$('hint').hidden=true;
 $('status').textContent=file.name;$('send').disabled=false;
};
$('preview').onerror=()=>{$('preview').hidden=true;$('hint').hidden=false;$('hint').textContent='已选择照片';};
$('send').onclick=async()=>{
 if(!file || busy)return;busy=true;$('send').disabled=true;$('pick').disabled=true;$('status').textContent='正在传送照片，请保持页面打开…';
 try{
  const data=new FormData();data.append('photo',file);
  const res=await fetch('/api/phone-pairs/'+encodeURIComponent(pair)+'/upload',{method:'POST',headers:{'X-Upload-Token':token},body:data});
  const result=await res.json();if(!res.ok)throw new Error(result.detail || '发送失败，请重试');
  $('status').textContent='照片已送达电脑。请回到电脑写下你的回忆。';$('send').textContent='已发送';
 }catch(e){$('status').textContent=e.message;$('send').disabled=false;$('pick').disabled=false;}finally{busy=false;}
};
