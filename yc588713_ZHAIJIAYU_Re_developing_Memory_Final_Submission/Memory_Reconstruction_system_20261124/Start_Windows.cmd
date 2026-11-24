@echo off
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (
 echo Please install dependencies following README.md first.
 pause
 exit /b 1
)
set OMP_NUM_THREADS=1
.venv\Scripts\python.exe src\app.py
pause
