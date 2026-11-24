# Memory / Reconstruction — 教师审阅版

2026-11-24 项目快照。包含可阅读、可安装运行的完整源程序，不是免安装应用。

## 先看什么
- `web/`：黑色双页网页、上传预览、逐步展示、二维码手机上传。
- `src/`：图像准备、语义理解、分割、累计处理、生成补充、条带拼合与下载。
- `prompts/`：作品的语义映射、生成边界和自动检查提示词。
- `docs/语义与效果总表.csv`：当前效果及开放条件。
- `tests/`：本地自动测试。
- `docs/DEVELOPMENT_HISTORY.md`：历史开发记录，其中早期阶段说明不代表目前功能状态。

## 作品流程
上传 RAW / JPEG / PNG / HEIC → 输入回忆 → 视觉观察与语义理解 → 按需分割 → 在上一阶段上继续修改并保存 → 原图在左、各阶段在右取对应位置条带拼合 → 下载结果与记录。
R 表示 RAW 来源处理，E 表示非生成加工，G 表示生成补充。JPEG/PNG 不冒充传感器实验。新增物体需明确添加授权或具体回忆依据，通过视觉检查后执行；不因一般愿望或隐喻自动添加物体。

## 安装（建议 Python 3.13，与制作环境一致）
需要联网安装依赖、下载模型；百炼 API 需要老师自己的有效密钥与模型权限。包内没有作者密钥、原始照片、历史实验图片、运行结果、虚拟环境或模型权重。

macOS / Linux，在解压后的目录运行：
```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env
```
Windows PowerShell：
```powershell
py -3.13 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```
编辑 `.env`，填写自己的 DASHSCOPE_API_KEY。默认服务地域为中国内地北京；文本、视觉与图像生成模型需在对应账号可用。不要把密钥发给他人。

下载本地分割和深度权重（只需首次，使用时遵守模型各自许可）：
```sh
.venv/bin/python src/segmentation.py --download
.venv/bin/python src/perceptual_effects.py --download
```
Windows 将上述 `.venv/bin/python` 改为 `.venv\Scripts\python.exe`。

## 打开网页
macOS 可双击 `Start_Mac.command`；Windows 双击 `Start_Windows.cmd`。也可以运行：
```sh
.venv/bin/python src/app.py
```
电脑浏览器打开 http://127.0.0.1:7860/ 。保持终端运行，关闭服务后网址不可访问。手机上传需要手机和电脑在可互通的同一局域网，并允许本机网络访问。它不是已经部署的公共网站。

## 检查与限制
```sh
OMP_NUM_THREADS=1 .venv/bin/python -m unittest discover -s tests
```
`tested_versions.json` 是打包机器的依赖版本记录，不是跨平台兼容性保证。API 模型可用性由服务商账号决定；模型下载可能需要可访问 Hugging Face 的网络。不同模型调用与硬件环境的结果不保证一致。仅阅读程序、提示词与表格不需要 API；本地测试不代表云端生成已经在老师电脑上验证。

本包不含任何试验照片或输出图片；`samples/` 和 `outputs/` 只保留目录占位。运行后新结果会写入 outputs/。
