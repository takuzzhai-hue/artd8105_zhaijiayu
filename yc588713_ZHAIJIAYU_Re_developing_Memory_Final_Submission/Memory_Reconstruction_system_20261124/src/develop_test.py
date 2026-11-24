"""将 RAW 分别以相机白平衡和实验线性设置显影。"""
from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import sys
from zoneinfo import ZoneInfo

import cv2
import rawpy

PROJECT = Path(__file__).resolve().parents[1]
RAW_EXTENSIONS = {'.raw', '.raf', '.cr2', '.cr3', '.crw', '.nef', '.nrw',
                  '.arw', '.srf', '.sr2', '.dng', '.rw2', '.orf', '.pef',
                  '.srw', '.3fr', '.fff', '.iiq', '.kdc', '.mos', '.mrw'}


def choose_raw(path: Path | None) -> Path:
    if path is not None:
        path = path.expanduser().resolve()
        if not path.is_file():
            raise ValueError(f'RAW 文件不存在：{path}')
        return path
    candidates = sorted(p for p in (PROJECT / 'samples').iterdir()
                        if p.is_file() and p.suffix.lower() in RAW_EXTENSIONS)
    if not candidates:
        raise ValueError('samples/ 中没有 RAW 文件，请先放入照片。')
    if len(candidates) > 1:
        raise ValueError('samples/ 中有多张 RAW，请用 --raw 指定一张。')
    return candidates[0]


def save_png(path: Path, rgb) -> None:
    # OpenCV 支持 16 位 RGB PNG，但写入时需要 BGR 通道顺序。
    if not cv2.imwrite(str(path), cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)):
        raise OSError(f'PNG 保存失败：{path}')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--raw', type=Path, help='指定 RAW；默认读取 samples/ 中唯一的 RAW')
    args = parser.parse_args()
    try:
        source = choose_raw(args.raw)
        stamp = datetime.now(ZoneInfo('Asia/Shanghai')).strftime('%Y%m%d_%H%M%S_%f')
        output = PROJECT / 'outputs' / stamp
        print(f'读取：{source}', flush=True)
        with rawpy.imread(str(source)) as raw:
            # 相机白平衡 + LibRaw 常规显影，不是相机厂商 JPEG 风格。
            normal = raw.postprocess(use_camera_wb=True, use_auto_wb=False,
                                     output_bps=16)
            output.mkdir(parents=True, exist_ok=False)
            save_png(output / '01_camera_default.png', normal)
            del normal
            # 仅关闭 camera_wb 会回退到日光白平衡，故显式设置单位增益。
            linear = raw.postprocess(no_auto_bright=True, gamma=(1, 1),
                                     use_camera_wb=False, use_auto_wb=False,
                                     user_wb=[1, 1, 1, 1], output_bps=16)
            save_png(output / '02_linear_no_camera_wb.png', linear)
        print(f'完成，两张 16 位 PNG 已保存到：\n{output}')
        return 0
    except (ValueError, OSError, rawpy.LibRawError) as exc:
        print(f'显影失败：{exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
