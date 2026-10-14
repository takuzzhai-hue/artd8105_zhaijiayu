#!/usr/bin/env python3
"""Local parameter server. The browser edits; this process builds the mesh."""

from __future__ import annotations

import json
import struct
import threading
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from generate import STAGES, generate, load_schema, params_from_obj

ROOT = Path(__file__).resolve().parent
WEB = ROOT / "web"
OUT = ROOT / "output"
HOST = "127.0.0.1"
PORT = 8765

LOCK = threading.Lock()
JOBS = {}


def strip_mesh(result):
    return {key: value for key, value in result.items() if key not in ("verts", "faces")}


def mesh_bytes(meta, verts, faces):
    payload = json.dumps(meta).encode("utf-8")
    v = np_float32(verts)
    f = np_uint32(faces)
    header = struct.pack("<III", len(payload), len(v), len(f))
    return header + payload + v.tobytes() + f.tobytes()


def np_float32(verts):
    import numpy as np

    return np.ascontiguousarray(verts, dtype=np.float32)


def np_uint32(faces):
    import numpy as np

    return np.ascontiguousarray(faces, dtype=np.uint32)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print("[server]", fmt % args, flush=True)

    def _send(self, code, body, content_type, extra=None):
        data = body if isinstance(body, (bytes, bytearray)) else body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        if extra:
            for key, value in extra.items():
                self.send_header(key, value)
        self.end_headers()
        self.wfile.write(data)

    def _json(self, code, obj):
        self._send(code, json.dumps(obj), "application/json")

    def _read_json(self):
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length else b"{}"
        return json.loads(raw.decode("utf-8"))

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/schema":
            self._json(200, load_schema())
            return
        if path.startswith("/api/job/"):
            job_id = path.rsplit("/", 1)[-1]
            job = JOBS.get(job_id)
            if not job:
                self._json(404, {"error": "unknown job"})
                return
            self._json(200, job)
            return
        if path == "/api/stl":
            stl = OUT / "object.stl"
            if not stl.exists():
                self._json(404, {"error": "no STL yet"})
                return
            self._send(200, stl.read_bytes(), "model/stl", {"Content-Disposition": "attachment; filename=object.stl"})
            return
        if path == "/" or path == "/index.html":
            self._send(200, (WEB / "index.html").read_bytes(), "text/html; charset=utf-8")
            return
        rel = path.lstrip("/")
        file_path = (WEB / rel).resolve()
        if not str(file_path).startswith(str(WEB.resolve())) or not file_path.is_file():
            self._json(404, {"error": "not found"})
            return
        kind = "text/plain; charset=utf-8"
        if file_path.suffix == ".js":
            kind = "text/javascript; charset=utf-8"
        elif file_path.suffix == ".css":
            kind = "text/css; charset=utf-8"
        elif file_path.suffix == ".json":
            kind = "application/json"
        self._send(200, file_path.read_bytes(), kind)

    def do_POST(self):
        path = urlparse(self.path).path
        try:
            body = self._read_json()
        except json.JSONDecodeError:
            self._json(400, {"error": "parameter JSON could not be read"})
            return
        if path == "/api/preview":
            self._preview(body)
            return
        if path == "/api/generate":
            self._start_generate(body)
            return
        self._json(404, {"error": "not found"})

    def _preview(self, body):
        resolution = body.pop("preview_resolution_override", None)
        try:
            flat, warnings = params_from_obj(body)
        except Exception as exc:  # noqa: BLE001
            self._json(400, {"error": str(exc)})
            return
        if resolution:
            flat["preview_resolution"] = int(resolution)
        if not LOCK.acquire(blocking=False):
            self._json(409, {"error": "busy"})
            return
        try:
            result = generate(flat, preview=True, quiet=True)
        except Exception as exc:  # noqa: BLE001
            self._json(500, {"error": str(exc), "warnings": warnings})
            return
        finally:
            LOCK.release()
        meta = strip_mesh(result)
        meta["warnings"] = warnings + meta.get("warnings", [])
        payload = mesh_bytes(meta, result["verts"], result["faces"])
        self._send(200, payload, "application/octet-stream")

    def _start_generate(self, body):
        try:
            flat, warnings = params_from_obj(body)
        except Exception as exc:  # noqa: BLE001
            self._json(400, {"error": str(exc)})
            return
        job_id = uuid.uuid4().hex[:12]
        JOBS[job_id] = {
            "id": job_id,
            "stage": STAGES[0],
            "stages": STAGES,
            "done": False,
            "error": None,
            "result": None,
        }

        def run():
            def progress(stage):
                JOBS[job_id]["stage"] = stage

            with LOCK:
                try:
                    result = generate(flat, preview=False, out_dir=OUT, progress=progress, quiet=True)
                    public = strip_mesh(result)
                    public["warnings"] = warnings + public.get("warnings", [])
                    JOBS[job_id]["result"] = public
                    JOBS[job_id]["stage"] = "Complete"
                except Exception as exc:  # noqa: BLE001
                    JOBS[job_id]["error"] = str(exc)
                    JOBS[job_id]["stage"] = "Complete"
            JOBS[job_id]["done"] = True

        threading.Thread(target=run, daemon=True).start()
        self._json(200, {"job": job_id, "stages": STAGES})


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"open http://{HOST}:{PORT}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
