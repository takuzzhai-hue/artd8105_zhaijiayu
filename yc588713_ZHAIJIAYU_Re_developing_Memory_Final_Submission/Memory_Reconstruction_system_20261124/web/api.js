// UI只依赖此适配器；当前连接真实Python后端，不使用模拟图片。
export async function request(url, options = {}) {
  const response = await fetch(url, {credentials: 'same-origin', ...options});
  let body;
  try { body = await response.json(); } catch { throw new Error('连接暂时中断，请稍后重试。'); }
  if (!response.ok) {
    const detail = body.detail;
    const error = new Error(typeof detail === 'string' ? detail : detail?.message || '请求未完成，请检查输入后重试。');
    error.status = response.status;
    error.jobId = detail?.job_id;
    throw error;
  }
  return body;
}
export const api = {
  config: () => request('/api/config'),
  upload: (file, signal) => {const data = new FormData(); data.append('photo', file); return request('/api/uploads', {method:'POST',body:data,signal});},
  start: (uploadId, memory) => request('/api/jobs', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({upload_id:uploadId,memory})}),
  status: id => request(`/api/jobs/${encodeURIComponent(id)}`)
};
