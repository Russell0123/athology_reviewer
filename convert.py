"""把 PDF 轉成網頁用的圖片（公開預覽版：指定頁面會蓋上浮水印）。

用法：
    python convert.py ../預覽合本/合本預覽.pdf

會清空 docs/pages/，重新產生每一頁的 WebP 圖片和 pages.json。
浮水印直接合成進圖片裡，網頁上無法拿掉。
需要先安裝一次：pip install pymupdf pillow
"""
import json
import sys
import time
from pathlib import Path

import pymupdf
from PIL import Image

PAGE_HEIGHT = 2400   # 每頁圖片高度（像素）；越高放大越清楚，檔案也越大
QUALITY = 85         # WebP 畫質（0–100）
WM_QUALITY = 75      # 有浮水印的頁面畫質（浮水印的顆粒很佔空間，調低一點檔案小很多，肉眼看不出差別）

HERE = Path(__file__).parent
WATERMARK = HERE / '浮水印.png'
WATERMARK_PAGES = range(4, 25)   # 第 4～24 頁蓋浮水印（PDF 頁碼，含頭尾）

OUT = HERE / 'docs' / 'pages'


def main():
    if len(sys.argv) != 2:
        sys.exit('用法：python convert.py 你的檔案.pdf')
    doc = pymupdf.open(Path(sys.argv[1]))
    watermark = Image.open(WATERMARK).convert('RGBA')

    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob('*'):
        old.unlink()

    files, total = [], 0
    for i, page in enumerate(doc, start=1):
        zoom = PAGE_HEIGHT / page.rect.height
        pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), alpha=False)
        img = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
        if i in WATERMARK_PAGES:
            wm = watermark.resize(img.size, Image.LANCZOS)
            img = Image.alpha_composite(img.convert('RGBA'), wm).convert('RGB')
        name = f'{i:03d}.webp'
        img.save(OUT / name, 'WEBP', quality=WM_QUALITY if i in WATERMARK_PAGES else QUALITY, method=6)
        files.append(name)
        total += (OUT / name).stat().st_size
        print(f'\r轉檔中 {i}/{doc.page_count}', end='', flush=True)

    manifest = {
        'width': img.width,
        'height': img.height,
        'pages': files,
        'version': int(time.time()),  # 讓瀏覽器知道圖片更新了
    }
    (OUT / 'pages.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'\n完成：{len(files)} 頁（第 {WATERMARK_PAGES.start}～{WATERMARK_PAGES.stop - 1} 頁已加浮水印），'
          f'共 {total / 1e6:.1f} MB → {OUT}')


if __name__ == '__main__':
    main()
