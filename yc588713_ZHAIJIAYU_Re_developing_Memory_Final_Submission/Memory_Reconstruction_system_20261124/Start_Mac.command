#!/bin/zsh
cd "$(dirname "$0")"
if [[ ! -x .venv/bin/python ]]; then
  echo "请先按照 README.md 安装 Python 虚拟环境和依赖。"
  read "?按回车退出"
  exit 1
fi
export OMP_NUM_THREADS=1
.venv/bin/python src/app.py
read "?服务已结束，按回车关闭"
