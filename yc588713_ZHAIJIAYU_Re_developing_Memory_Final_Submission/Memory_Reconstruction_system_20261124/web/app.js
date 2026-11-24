import {api} from './api.js';
const $ = id => document.getElementById(id);
const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
const wait = ms => new Promise(resolve => setTimeout(resolve, ms));
const pad = n => String(n).padStart(2, '0');
let photo = null, config = null, uploadController = null, uploadRevision = 0;
let active = false, starting = false, epoch = 0, page = 'input';
let latest = null, displayed = 0, selected = -1, pumping = false, finished = false, followLatest = true;
const images = [];
function store(key,value) {try {value === null ? sessionStorage.removeItem(key) : sessionStorage.setItem(key,JSON.stringify(value));} catch {}}
function read(key) {try{return JSON.parse(sessionStorage.getItem(key));} catch{return null;}}
function error(id,message) {$(id).textContent=message || ''; $(id).hidden=!message;}
function fitText() {const box=$('memory');box.style.height='auto';box.style.height=`${Math.max(185,box.scrollHeight)}px`;}
function enabled() {$('generate').disabled=!photo || !$('memory').value.trim() || active || starting || !!uploadController;}
function ratio(width,height) {document.documentElement.style.setProperty('--photo-ratio',`${width} / ${height}`);}
async function switchPage(next) {
  if (page===next)return;
  const old=$(page==='input'?'input-page':'reconstruction-page');
  const current=$(next==='input'?'input-page':'reconstruction-page');
  page=next;old.classList.add('leaving');
  await wait(reduced.matches?0:250);
  old.hidden=true;old.classList.remove('leaving');current.classList.add('entering');current.hidden=false;
  $('page-number').textContent=next==='input'?'01 / INPUT':'02 / RECONSTRUCTION';
  history.replaceState(null,'',next==='input'?'#input':'#reconstruction');
  window.scrollTo({top:0,behavior:'instant'});
  requestAnimationFrame(()=>requestAnimationFrame(()=>current.classList.remove('entering')));
}
function showPhoto(data) {
  photo=data;ratio(data.width,data.height);
  const preview=$('upload-preview');preview.src=data.preview;preview.hidden=false;
  $('upload-prompt').hidden=true;$('upload-area').classList.add('has-image');
  $('replace-photo').hidden=false;$('upload-caption').textContent=`${data.name || 'PHOTOGRAPH'} / ${data.width} × ${data.height}`;
  store('memory-upload',data);enabled();
}
async function choose(file) {
  if(!file)return;
  const extension='.'+file.name.split('.').pop().toLowerCase();
  const formats=config?.formats || $('photo-file').accept.split(',');
  if(!formats.includes(extension)){error('upload-error','请选择 RAW、JPEG、PNG、WebP 或 TIFF 照片。');return;}
  if(file.size>(config?.max_bytes || 512*1024*1024)){error('upload-error','照片超过 512 MB，请选择更小的文件。');return;}
  uploadController?.abort();const revision=++uploadRevision;uploadController=new AbortController();
  error('upload-error','');error('form-error','');$('upload-caption').textContent='正在读取照片…';enabled();
  try {
    const data=await api.upload(file,uploadController.signal);
    if(revision!==uploadRevision)return;
    await preload(data.preview);
    showPhoto(data);
  } catch(e) {
    if(e.name==='AbortError' || revision!==uploadRevision)return;
    error('upload-error',e.message);$('upload-caption').textContent=photo?.name || 'RAW / JPEG / PNG / WEBP / TIFF';
  } finally {if(revision===uploadRevision){uploadController=null;enabled();}}
}
function preload(src) {
  return new Promise((resolve,reject)=>{
    const img=new Image();img.decoding='async';
    const timer=setTimeout(()=>reject(new Error('照片加载超时，正在尝试重新连接。')),30000);
    img.onload=()=>{clearTimeout(timer);resolve(img);};img.onerror=()=>{clearTimeout(timer);reject(new Error('照片加载失败，正在尝试重新连接。'));};img.src=src;
  });
}
function select(index,manual=false) {
  if(index<0 || index>=images.length)return;
  if(manual)followLatest=index===images.length-1;
  selected=index;
  images.forEach((image,i)=>{image.classList.toggle('visible',i===index);image.classList.toggle('instant',manual);});
  [...$('stage-nav').children].forEach((button,i)=>button.setAttribute('aria-current',String(i===index)));
  updateCount();
}
function displayStatus(state) {
  const value=state.status;
  const step=value.match(/^第 (\d+) 步已完成/);
  if(step)return `第 ${step[1]} 张影像已完成。`;
  if(value.includes('检查原话'))return '正在理解你记得的内容…';
  if(value.includes('局部轮廓'))return '正在辨认画面中的细节…';
  if(value.includes('制定逐步'))return '正在整理回忆的顺序…';
  if(value.includes('全部阶段已保存'))return '正在拼合这些影像…';
  return value;
}
function updateCount() {
  $('counter').textContent=`${selected>=0?pad(selected+1):'—'} / ${latest?.total?pad(latest.total):'—'}`;
  const label=latest?.labels?.[selected] || '';
  $('stage-label').textContent=label.includes('含AI补充')?label.split(' · ').slice(2).join(' · '):'';
}
function clearResults() {
  images.forEach(img=>img.remove());images.length=0;displayed=0;selected=-1;latest=null;pumping=false;finished=false;followLatest=true;
  $('stage-nav').replaceChildren();$('empty-stage').hidden=false;$('counter').textContent='— / —';$('stage-label').textContent='';
  $('composite-section').hidden=true;$('composite-image').classList.remove('visible');$('composite-image').removeAttribute('src');
  $('result-actions').hidden=true;$('process-notes').hidden=true;$('retry-view').hidden=true;error('result-error','');
}
async function revealAvailable(token) {
  if(pumping || token!==epoch)return;
  pumping=true;
  try {
    while(latest && displayed<latest.images.length && token===epoch) {
      const index=displayed;const img=await preload(latest.images[index]);
      if(token!==epoch)return;
      img.alt=`第 ${index+1} 张累计重构照片`;images.push(img);$('stage-frame').append(img);$('empty-stage').hidden=true;
      const button=document.createElement('button');button.type='button';button.textContent=pad(index+1);button.setAttribute('aria-label',`查看第 ${index+1} 张照片`);
      button.addEventListener('click',()=>select(index,true));$('stage-nav').append(button);
      displayed++;
      await new Promise(requestAnimationFrame);
      if(followLatest || selected<0)select(index);else updateCount();
      await wait(reduced.matches?0:2100);
    }
    if(latest?.phase==='complete' && displayed===latest.images.length && token===epoch)await showFinal(token);
  } catch(e) {if(token===epoch)error('result-error',e.message);}
  finally {if(token===epoch)pumping=false;}
}
async function showFinal(token) {
  if(finished)return;
  if(!latest.composite || !latest.archive)throw new Error('拼合或下载文件尚未准备好。');
  const image=await preload(latest.composite);
  if(token!==epoch)return;
  finished=true;active=false;enabled();error('result-error','');
  $('composite-image').src=image.src;$('composite-section').hidden=false;
  requestAnimationFrame(()=>requestAnimationFrame(()=>$('composite-image').classList.add('visible')));
  $('download').href=latest.archive;$('result-actions').hidden=false;
  $('progress').textContent=`已完成 ${displayed} 张阶段影像。`+(latest.fallback_count?`其中 ${latest.fallback_count} 张为基础明暗调整。`:'')+(latest.skipped_count?' 部分请求未完成，详见处理记录。':'');
  $('process-detail').textContent=latest.status;$('process-notes').hidden=false;
  updateCount();
}
async function monitor(id,token) {
  let failures=0;
  while(token===epoch) {
    try {
      const state=await api.status(id);
      if(token!==epoch)return;
      latest=state;failures=0;ratio(state.width,state.height);updateCount();
      if(!finished)$('progress').textContent=state.phase==='complete'?'正在呈现最终影像…':displayStatus(state);
      if(state.phase==='error') {
        active=false;enabled();error('result-error',state.status);$('retry-view').hidden=false;
        await revealAvailable(token);return;
      }
      error('result-error','');
      void revealAvailable(token);
      if(finished)return;
    } catch(e) {
      if(token!==epoch)return;
      failures++;
      if(e.status===404){active=false;enabled();error('result-error',e.message);$('retry-view').hidden=false;return;}
      $('progress').textContent='连接暂时中断，正在重新连接。已完成的照片会保留。';
    }
    await wait(Math.min(1000*(failures+1),5000));
  }
}
$('memory').addEventListener('input',()=>{fitText();enabled();store('memory-draft',$('memory').value);});
$('upload-area').addEventListener('click',()=>$('photo-file').click());
$('replace-photo').addEventListener('click',()=>$('photo-file').click());
$('photo-file').addEventListener('change',event=>{void choose(event.target.files[0]);event.target.value='';});
for(const type of ['dragenter','dragover'])$('upload-area').addEventListener(type,event=>{event.preventDefault();$('upload-area').classList.add('dragging');});
for(const type of ['dragleave','drop'])$('upload-area').addEventListener(type,event=>{event.preventDefault();$('upload-area').classList.remove('dragging');});
$('upload-area').addEventListener('drop',event=>{if(event.dataTransfer.files.length!==1){error('upload-error','请一次上传一张照片。');return;}void choose(event.dataTransfer.files[0]);});
window.addEventListener('dragover',event=>event.preventDefault());window.addEventListener('drop',event=>event.preventDefault());
$('memory-form').addEventListener('submit',async event=>{
  event.preventDefault();if(!photo || !$('memory').value.trim() || active || starting)return;
  starting=true;active=true;enabled();clearResults();const token=++epoch;
  $('progress').textContent='正在准备重构…';void switchPage('reconstruction');
  try {
    const job=await api.start(photo.id,$('memory').value);store('memory-job',job.id);
    void monitor(job.id,token);
  } catch(e) {
    if(e.jobId){store('memory-job',e.jobId);void monitor(e.jobId,token);}
    else{active=false;error('result-error',e.message);$('retry-view').hidden=false;}
  } finally {starting=false;enabled();}
});
$('retry-view').addEventListener('click',()=>{epoch++;active=false;store('memory-job',null);void switchPage('input');enabled();});
$('home').addEventListener('click',event=>{event.preventDefault();if(!active)void switchPage('input');});
$('restart').addEventListener('click',()=>{
  epoch++;active=false;photo=null;store('memory-job',null);store('memory-upload',null);store('memory-draft',null);
  $('memory').value='';fitText();$('upload-preview').hidden=true;$('upload-preview').removeAttribute('src');
  $('upload-area').classList.remove('has-image');$('upload-prompt').hidden=false;$('replace-photo').hidden=true;$('upload-caption').textContent='RAW / JPEG / PNG / WEBP / TIFF';
  error('upload-error','');error('form-error','');enabled();void switchPage('input');
});
async function initialize() {
  $('memory').value=read('memory-draft') || '';fitText();
  const old=read('memory-upload');
  if(old){try{await preload(old.preview);showPhoto(old);}catch{store('memory-upload',null);}}
  try{config=await api.config();}catch{error('form-error','暂时无法连接，请刷新页面重试。');}
  const jobId=read('memory-job');
  if(jobId && location.hash==='#reconstruction'){
    active=true;enabled();await switchPage('reconstruction');void monitor(jobId,++epoch);
  }else enabled();
}
window.addEventListener('resize',fitText);
void initialize();

let phonePair=null, phoneTimer=null;
async function createPhonePair(){
  clearTimeout(phoneTimer);phonePair=null;
  $('phone-qr').hidden=true;$('phone-status').hidden=true;
  try {
    const response=await fetch('/api/phone-pairs',{method:'POST'});const data=await response.json();
    if(!response.ok)throw new Error(data.detail || '连接失败');
    phonePair=data.id;
    await preload(data.qr);
    if(phonePair!==data.id)return;
    $('phone-qr').src=data.qr;$('phone-qr').hidden=false;
    $('phone-status').textContent='';$('phone-status').hidden=true;
    pollPhone(data.id);
  }catch(e){$('phone-status').hidden=false;$('phone-status').textContent='二维码加载失败，正在重试…';phoneTimer=setTimeout(createPhonePair,4000);}
}
async function pollPhone(id){
  if(phonePair!==id)return;
  try{
    const res=await fetch('/api/phone-pairs/'+id);const data=await res.json();
    if(phonePair!==id)return;
    if(!res.ok || data.state==='expired'){createPhonePair();return;}
    if(data.state==='received'){
      if(active || starting || uploadController){phoneTimer=setTimeout(()=>pollPhone(id),1500);return;}
      await preload(data.photo.preview);
      if(phonePair!==id)return;
      showPhoto(data.photo);error('upload-error','');createPhonePair();return;
    }
    if(data.state==='uploading')$('phone-status').hidden=true;
  }catch(e){$('phone-status').hidden=false;$('phone-status').textContent='连接暂时中断，正在重试…';}
  phoneTimer=setTimeout(()=>pollPhone(id),1500);
}
$('phone-refresh').addEventListener('click',createPhonePair);
createPhonePair();
