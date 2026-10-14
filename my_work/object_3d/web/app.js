import * as THREE from "three";
import { OrbitControls } from "./vendor/OrbitControls.js";

const FORMULA = {
  gyroid: "sin X cos Y + sin Y cos Z + sin Z cos X",
  diamond: "sin X sin Y sin Z + sin X cos Y cos Z + cos X sin Y cos Z + cos X cos Y sin Z",
  primitive: "cos X + cos Y + cos Z",
};

const statusEl = document.querySelector("#status");
const dimsEl = document.querySelector("#dims");
const formulaEl = document.querySelector("#formula");
const stageNote = document.querySelector("#stage-note");
const groupsEl = document.querySelector("#groups");
const resultEl = document.querySelector("#result");
const progressEl = document.querySelector("#progress");
const presetNote = document.querySelector("#preset-note");
const compareCount = document.querySelector("#compare-count");

let schema = null;
let params = null;
let controls = [];
let history = [];
let historyIndex = -1;
let compareSlots = [];
let compareMode = false;
let compareViews = [];
let showSurface = true;
let showWire = false;
let showBox = true;
let generating = false;

const canvas = document.querySelector("#view");
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
renderer.setClearColor(0xf3f2ef, 1);

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(32, 1, 0.1, 2000);
camera.up.set(0, 0, 1);
const orbit = new OrbitControls(camera, canvas);
orbit.enableDamping = true;
orbit.dampingFactor = 0.08;

scene.add(new THREE.AmbientLight(0xffffff, 0.62));
const key = new THREE.DirectionalLight(0xffffff, 0.95);
key.position.set(80, -120, 140);
scene.add(key);
const fill = new THREE.DirectionalLight(0xffffff, 0.35);
fill.position.set(-100, 40, 60);
scene.add(fill);

const material = new THREE.MeshStandardMaterial({
  color: 0x4a4a4a,
  roughness: 0.78,
  metalness: 0,
  side: THREE.DoubleSide,
  wireframe: false,
});
const mesh = new THREE.Mesh(new THREE.BufferGeometry(), material);
scene.add(mesh);
const wireMesh = new THREE.Mesh(
  mesh.geometry,
  new THREE.MeshBasicMaterial({ color: 0x2a2a2a, wireframe: true })
);
wireMesh.visible = false;
scene.add(wireMesh);
const bounds = new THREE.LineSegments(
  new THREE.EdgesGeometry(new THREE.BoxGeometry(1, 1, 1)),
  new THREE.LineBasicMaterial({ color: 0x9a968e })
);
scene.add(bounds);

function getPath(obj, path) {
  return path.split(".").reduce((node, key) => node[key], obj);
}

function setPath(obj, path, value) {
  const parts = path.split(".");
  let node = obj;
  for (let i = 0; i < parts.length - 1; i += 1) node = node[parts[i]];
  node[parts[parts.length - 1]] = value;
}

function merge(base, over) {
  const out = structuredClone(base);
  Object.keys(over || {}).forEach((key) => {
    const value = over[key];
    if (value && typeof value === "object" && !Array.isArray(value)) out[key] = merge(out[key] ?? {}, value);
    else out[key] = structuredClone(value);
  });
  return out;
}

function decimals(step) {
  const text = String(step);
  return text.includes(".") ? text.split(".")[1].length : 0;
}

function format(control, value) {
  if (control.type !== "number") return String(value);
  return Number(value).toFixed(decimals(control.step));
}

function coerce(control, raw) {
  if (control.type === "bool") return Boolean(raw);
  if (control.type === "select") {
    const sample = getPath(schema.defaults, control.key);
    return typeof sample === "number" ? Number(raw) : String(raw);
  }
  return Number(raw);
}

function commit() {
  const snap = JSON.stringify(params);
  if (history[historyIndex] === snap) return;
  history = history.slice(0, historyIndex + 1);
  history.push(snap);
  historyIndex += 1;
  if (history.length > 60) {
    history.shift();
    historyIndex -= 1;
  }
}

function restore(index) {
  historyIndex = index;
  params = JSON.parse(history[historyIndex]);
  syncControls();
  updateReadouts();
  schedule(false);
}

function controlActive(control) {
  const rule = control.activeWhen;
  if (!rule) return true;
  const value = getPath(params, rule.key);
  if (rule.equals !== undefined) return value === rule.equals;
  if (rule.not !== undefined) return value !== rule.not;
  if (rule.in) return rule.in.includes(value);
  return true;
}

function updateActive() {
  controls.forEach((entry) => {
    entry.root.classList.toggle("is-inactive", !controlActive(entry.control));
  });
}

function updateBounds() {
  const [sx, sy, sz] = params.size;
  bounds.geometry.dispose();
  bounds.geometry = new THREE.EdgesGeometry(new THREE.BoxGeometry(sx, sy, sz));
  bounds.position.set(0, 0, sz / 2);
  bounds.visible = showBox;
}

function updateReadouts() {
  const [sx, sy, sz] = params.size;
  dimsEl.textContent = `${sx} × ${sy} × ${sz} mm`;
  formulaEl.textContent = FORMULA[params.family] || "";
  updateBounds();
  updateActive();
}

function setStatus(kind, text) {
  statusEl.className = `status ${kind || ""}`;
  statusEl.textContent = text;
}

function buildControl(control) {
  const root = document.createElement("div");
  root.className = "ctrl";
  if (control.type === "bool") {
    const label = document.createElement("label");
    label.className = "check";
    const input = document.createElement("input");
    input.type = "checkbox";
    input.checked = Boolean(getPath(params, control.key));
    input.addEventListener("change", () => {
      setPath(params, control.key, input.checked);
      commit();
      updateReadouts();
      schedule(false);
    });
    label.append(input, document.createTextNode(control.label));
    root.append(label);
    const help = document.createElement("p");
    help.className = "help";
    help.textContent = control.help;
    root.append(help);
    controls.push({ control, root, input });
    return root;
  }

  const label = document.createElement("div");
  label.className = "ctrl-label";
  const name = document.createElement("b");
  name.textContent = control.label;
  const value = document.createElement("span");
  value.className = "unit";
  label.append(name, value);
  root.append(label);

  if (control.type === "select") {
    const select = document.createElement("select");
    control.options.forEach((option) => {
      const item = document.createElement("option");
      item.value = option;
      item.textContent = option;
      select.append(item);
    });
    select.value = String(getPath(params, control.key));
    select.addEventListener("change", () => {
      setPath(params, control.key, coerce(control, select.value));
      commit();
      updateReadouts();
      schedule(false);
    });
    root.append(select);
    controls.push({ control, root, select, value });
  } else {
    const row = document.createElement("div");
    row.className = "slider-row";
    const slider = document.createElement("input");
    slider.type = "range";
    slider.min = control.min;
    slider.max = control.max;
    slider.step = control.step;
    const number = document.createElement("input");
    number.type = "number";
    number.min = control.min;
    number.max = control.max;
    number.step = control.step;
    const current = getPath(params, control.key);
    slider.value = current;
    number.value = format(control, current);
    value.textContent = `${format(control, current)}${control.unit ? ` ${control.unit}` : ""}`;
    const write = (raw, low) => {
      let next = Number(raw);
      if (Number.isNaN(next)) return;
      next = Math.min(control.max, Math.max(control.min, next));
      setPath(params, control.key, next);
      slider.value = next;
      number.value = format(control, next);
      value.textContent = `${format(control, next)}${control.unit ? ` ${control.unit}` : ""}`;
      updateReadouts();
      schedule(low);
    };
    slider.addEventListener("input", () => write(slider.value, true));
    slider.addEventListener("change", () => {
      write(slider.value, false);
      commit();
    });
    number.addEventListener("change", () => {
      write(number.value, false);
      commit();
    });
    row.append(slider, number);
    root.append(row);
    controls.push({ control, root, slider, number, value });
  }
  const help = document.createElement("p");
  help.className = "help";
  help.textContent = control.help;
  root.append(help);
  return root;
}

function syncControls() {
  controls.forEach((entry) => {
    const current = getPath(params, entry.control.key);
    if (entry.control.type === "bool") entry.input.checked = Boolean(current);
    if (entry.control.type === "select") entry.select.value = String(current);
    if (entry.control.type === "number") {
      entry.slider.value = current;
      entry.number.value = format(entry.control, current);
      entry.value.textContent = `${format(entry.control, current)}${entry.control.unit ? ` ${entry.control.unit}` : ""}`;
    }
  });
}

function buildGroups() {
  groupsEl.replaceChildren();
  controls = [];
  schema.ui.forEach((group, index) => {
    const details = document.createElement("details");
    if (index < 2) details.open = true;
    const summary = document.createElement("summary");
    summary.textContent = group.label;
    details.append(summary);
    if (group.note) {
      const note = document.createElement("p");
      note.className = "group-note";
      note.textContent = group.note;
      details.append(note);
    }
    group.controls.forEach((control) => details.append(buildControl(control)));
    groupsEl.append(details);
  });
  const preset = document.querySelector("#preset");
  preset.replaceChildren();
  Object.keys(schema.presets).forEach((name) => {
    const option = document.createElement("option");
    option.value = name;
    option.textContent = name;
    preset.append(option);
  });
}

let queued = null;
let inflight = false;
let timer = 0;

function schedule(low) {
  queued = low;
  window.clearTimeout(timer);
  timer = window.setTimeout(() => pump(), low ? 90 : 220);
}

async function pump() {
  if (inflight || generating || queued === null) return;
  const low = queued;
  queued = null;
  inflight = true;
  stageNote.textContent = low ? "Updating a coarse preview." : "Updating preview.";
  try {
    await loadPreview(low);
  } finally {
    inflight = false;
    if (queued !== null) pump();
  }
}

async function loadPreview(low) {
  const body = structuredClone(params);
  if (low) body.preview_resolution_override = 48;
  const response = await fetch("/api/preview", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (response.status === 409) {
    queued = low;
    return;
  }
  const type = response.headers.get("content-type") || "";
  if (!response.ok) {
    const err = type.includes("json") ? await response.json() : { error: response.statusText };
    stageNote.textContent = err.error || "Preview failed.";
    setStatus("", "Preview");
    return;
  }
  const buffer = await response.arrayBuffer();
  const view = new DataView(buffer);
  const jsonLen = view.getUint32(0, true);
  const nVerts = view.getUint32(4, true);
  const nFaces = view.getUint32(8, true);
  const meta = JSON.parse(new TextDecoder().decode(new Uint8Array(buffer, 12, jsonLen)));
  let offset = 12 + jsonLen;
  const positions = new Float32Array(buffer.slice(offset, offset + nVerts * 12));
  offset += nVerts * 12;
  const indices = new Uint32Array(buffer.slice(offset, offset + nFaces * 12));
  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute("position", new THREE.BufferAttribute(positions, 3));
  geometry.setIndex(new THREE.BufferAttribute(indices, 1));
  geometry.computeVertexNormals();
  mesh.geometry.dispose();
  mesh.geometry = geometry;
  wireMesh.geometry = geometry;
  mesh.visible = showSurface;
  wireMesh.visible = showWire;
  stageNote.textContent = meta.experimental?.length
    ? `Experimental preview. ${meta.experimental[0]}`
    : "Preview geometry. Not validated for export.";
  setStatus("", "Preview");
  if (!compareMode) frameCamera(false);
}

function frameCamera(force) {
  const sz = params.size[2] || 80;
  if (!force && orbit.target.lengthSq() > 1) {
    orbit.target.set(0, 0, sz / 2);
    return;
  }
  camera.position.set(sz * 1.7, -sz * 1.9, sz * 1.2);
  orbit.target.set(0, 0, sz / 2);
  orbit.update();
}

function resize() {
  const rect = canvas.parentElement.getBoundingClientRect();
  renderer.setSize(rect.width, rect.height, false);
  camera.aspect = rect.width / Math.max(rect.height, 1);
  camera.updateProjectionMatrix();
}

function animate() {
  requestAnimationFrame(animate);
  orbit.update();
  if (compareMode) compareViews.forEach((view) => view.render());
  else renderer.render(scene, camera);
}

function applyPreset(name) {
  commit();
  params = merge(schema.defaults, schema.presets[name] || {});
  syncControls();
  updateReadouts();
  presetNote.textContent = schema.presetNotes?.[name] || "";
  commit();
  schedule(false);
}

function randomIn(control, safe) {
  const lo = safe ? (control.safeMin ?? control.min) : (control.randomMin ?? control.min);
  const hi = safe ? (control.safeMax ?? control.max) : (control.randomMax ?? control.max);
  const step = control.step || 1;
  const steps = Math.round((hi - lo) / step);
  return lo + step * Math.floor(Math.random() * (steps + 1));
}

function randomize(safe) {
  commit();
  schema.ui.forEach((group) => {
    group.controls.forEach((control) => {
      if (control.type === "number") setPath(params, control.key, randomIn(control, safe));
      if (control.type === "bool") setPath(params, control.key, safe ? false : Math.random() < 0.35);
      if (control.type === "select" && !safe) {
        const option = control.options[Math.floor(Math.random() * control.options.length)];
        setPath(params, control.key, coerce(control, option));
      }
    });
  });
  if (safe) {
    params.family = "gyroid";
    params.twist.mode = Math.random() < 0.45 ? "linear" : "off";
    params.thickness.mode = "constant";
    params.density.gradient = Math.random() < 0.3 ? "z" : "off";
    params.transform.mirror = [false, false, false];
  }
  syncControls();
  updateReadouts();
  commit();
  schedule(false);
}

function downloadParams() {
  const blob = new Blob([JSON.stringify(params, null, 2)], { type: "application/json" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "gyroid-params.json";
  link.click();
  URL.revokeObjectURL(link.href);
}

async function showResult(job) {
  generating = false;
  progressEl.querySelectorAll("li").forEach((item) => {
    item.classList.remove("on");
    item.classList.add("done");
  });
  if (job.error) {
    setStatus("bad", "Not printable");
    resultEl.innerHTML = `<p class="fail">${job.error}</p>`;
    return;
  }
  const result = job.result;
  if (result.validated) {
    setStatus("good", "Validated for export");
    resultEl.innerHTML = `<p>The independent check passed. This file is the printable one.</p><p><a href="/api/stl">Download STL</a></p>`;
  } else {
    setStatus("bad", "Not printable");
    const items = (result.failures || []).map((item) => `<li>${item}</li>`).join("");
    const lines = (result.verification?.lines || []).filter((line) => line.startsWith("[FAIL]"));
    const extra = lines.map((line) => `<li>${line}</li>`).join("");
    resultEl.innerHTML = `<p class="fail">Validation failed. This mesh is not labeled printable.</p><ul>${items}${extra}</ul><p><a href="/api/stl">Download unvalidated STL</a></p>`;
  }
}

async function generateSTL() {
  if (generating) return;
  generating = true;
  document.querySelector("#generate").disabled = true;
  setStatus("", "Generating");
  stageNote.textContent = "Running the high-resolution pipeline.";
  resultEl.replaceChildren();
  progressEl.hidden = false;
  progressEl.replaceChildren();
  const response = await fetch("/api/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params),
  });
  const start = await response.json();
  if (!response.ok) {
    generating = false;
    document.querySelector("#generate").disabled = false;
    setStatus("bad", "Not printable");
    resultEl.innerHTML = `<p class="fail">${start.error || "Could not start."}</p>`;
    return;
  }
  start.stages.forEach((stage) => {
    const item = document.createElement("li");
    item.textContent = stage;
    item.dataset.stage = stage;
    progressEl.append(item);
  });
  const poll = window.setInterval(async () => {
    const job = await fetch(`/api/job/${start.job}`).then((res) => res.json());
    progressEl.querySelectorAll("li").forEach((item) => {
      const index = start.stages.indexOf(item.dataset.stage);
      const current = start.stages.indexOf(job.stage);
      item.classList.toggle("on", item.dataset.stage === job.stage && !job.done);
      item.classList.toggle("done", index < current || (job.done && index <= current));
    });
    if (job.done) {
      window.clearInterval(poll);
      document.querySelector("#generate").disabled = false;
      await showResult(job);
    }
  }, 800);
}

function makeView(slot, host) {
  const viewCanvas = document.createElement("canvas");
  host.append(viewCanvas);
  const viewRenderer = new THREE.WebGLRenderer({ canvas: viewCanvas, antialias: true });
  viewRenderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.5));
  viewRenderer.setClearColor(0xf3f2ef, 1);
  const viewScene = new THREE.Scene();
  viewScene.add(new THREE.AmbientLight(0xffffff, 0.62));
  const light = new THREE.DirectionalLight(0xffffff, 0.95);
  light.position.set(80, -120, 140);
  viewScene.add(light);
  const viewCamera = new THREE.PerspectiveCamera(32, 1, 0.1, 2000);
  viewCamera.up.set(0, 0, 1);
  const sz = slot.params.size[2] || 80;
  viewCamera.position.set(sz * 1.7, -sz * 1.9, sz * 1.2);
  viewCamera.lookAt(0, 0, sz / 2);
  const viewMesh = new THREE.Mesh(new THREE.BufferGeometry(), material.clone());
  viewScene.add(viewMesh);
  return {
    render() {
      const rect = host.getBoundingClientRect();
      viewRenderer.setSize(rect.width, rect.height, false);
      viewCamera.aspect = rect.width / Math.max(rect.height, 1);
      viewCamera.updateProjectionMatrix();
      viewRenderer.render(viewScene, viewCamera);
    },
    async load() {
      const response = await fetch("/api/preview", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...slot.params, preview_resolution_override: 64 }),
      });
      if (!response.ok) return;
      const buffer = await response.arrayBuffer();
      const view = new DataView(buffer);
      const jsonLen = view.getUint32(0, true);
      const nVerts = view.getUint32(4, true);
      const nFaces = view.getUint32(8, true);
      let offset = 12 + jsonLen;
      const positions = new Float32Array(buffer.slice(offset, offset + nVerts * 12));
      offset += nVerts * 12;
      const indices = new Uint32Array(buffer.slice(offset, offset + nFaces * 12));
      const geometry = new THREE.BufferGeometry();
      geometry.setAttribute("position", new THREE.BufferAttribute(positions, 3));
      geometry.setIndex(new THREE.BufferAttribute(indices, 1));
      geometry.computeVertexNormals();
      viewMesh.geometry = geometry;
    },
  };
}

async function toggleCompare() {
  const host = document.querySelector("#compare");
  if (compareMode) {
    compareMode = false;
    host.hidden = true;
    canvas.classList.remove("compare-hidden");
    compareViews = [];
    host.replaceChildren();
    return;
  }
  if (compareSlots.length < 2) {
    compareCount.textContent = "Save at least two states before comparing.";
    return;
  }
  compareMode = true;
  canvas.classList.add("compare-hidden");
  host.hidden = false;
  host.replaceChildren();
  compareViews = compareSlots.slice(0, 4).map((slot) => {
    const cell = document.createElement("div");
    cell.className = "cell";
    const caption = document.createElement("span");
    caption.textContent = slot.name;
    cell.append(caption);
    host.append(cell);
    return makeView(slot, cell);
  });
  for (const view of compareViews) await view.load();
}

function wire() {
  document.querySelector("#preset").addEventListener("change", (event) => applyPreset(event.target.value));
  document.querySelector("#undo").addEventListener("click", () => {
    if (historyIndex > 0) restore(historyIndex - 1);
  });
  document.querySelector("#redo").addEventListener("click", () => {
    if (historyIndex < history.length - 1) restore(historyIndex + 1);
  });
  document.querySelector("#reset").addEventListener("click", () => applyPreset("Classic Gyroid"));
  document.querySelector("#random").addEventListener("click", () => randomize(false));
  document.querySelector("#random-safe").addEventListener("click", () => randomize(true));
  document.querySelector("#save").addEventListener("click", downloadParams);
  document.querySelector("#load").addEventListener("click", () => document.querySelector("#load-file").click());
  document.querySelector("#load-file").addEventListener("change", async (event) => {
    const file = event.target.files[0];
    if (!file) return;
    const loaded = JSON.parse(await file.text());
    commit();
    params = merge(schema.defaults, loaded);
    syncControls();
    updateReadouts();
    commit();
    schedule(false);
  });
  document.querySelector("#compare-add").addEventListener("click", () => {
    if (compareSlots.length >= 4) compareSlots.shift();
    compareSlots.push({ name: `State ${compareSlots.length + 1}`, params: structuredClone(params) });
    compareSlots.forEach((slot, index) => {
      slot.name = `State ${index + 1}`;
    });
    compareCount.textContent = `${compareSlots.length} saved for comparison.`;
  });
  document.querySelector("#compare-clear").addEventListener("click", () => {
    compareSlots = [];
    compareCount.textContent = "";
    if (compareMode) toggleCompare();
  });
  document.querySelector("#compare-toggle").addEventListener("click", toggleCompare);
  document.querySelector("#generate").addEventListener("click", generateSTL);
  document.querySelector("#reset-cam").addEventListener("click", () => frameCamera(true));
  document.querySelector("#toggle-surface").addEventListener("click", (event) => {
    showSurface = !showSurface;
    event.currentTarget.setAttribute("aria-pressed", String(showSurface));
    mesh.visible = showSurface;
  });
  document.querySelector("#toggle-wire").addEventListener("click", (event) => {
    showWire = !showWire;
    event.currentTarget.setAttribute("aria-pressed", String(showWire));
    wireMesh.visible = showWire;
  });
  document.querySelector("#toggle-box").addEventListener("click", (event) => {
    showBox = !showBox;
    event.currentTarget.setAttribute("aria-pressed", String(showBox));
    bounds.visible = showBox;
  });
  window.addEventListener("resize", resize);
}

async function main() {
  schema = await fetch("/api/schema").then((response) => response.json());
  params = structuredClone(schema.defaults);
  buildGroups();
  wire();
  commit();
  updateReadouts();
  resize();
  frameCamera(true);
  animate();
  schedule(false);
  presetNote.textContent = schema.presetNotes["Classic Gyroid"];
}

main();
