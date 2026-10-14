#!/bin/sh
set -e
cd "$(dirname "$0")"
PY=python3
if [ -x .venv/bin/python ]; then
  PY=.venv/bin/python
fi
"$PY" generate.py "$@"
"$PY" check_stl.py output/object.stl
