# 春夏秋冬野貓觀察日記 公開預覽版

給一般觀眾看的預覽版：和完整版用同一個閱讀器，但第 4～24 頁蓋上浮水印。
浮水印直接合成進圖片，網頁上拿不掉，也下載不到原圖。

## 更新頁面

```
python convert.py ../預覽合本/合本預覽.pdf
```

- 浮水印圖檔：`浮水印.png`、敬請期待頁的底圖：`浮水印2.png`、中間的字：`期待.png`（都不上傳到 GitHub）
- 要改哪些頁蓋浮水印、透明度、哪些頁全白：修改 `convert.py` 裡的 `WATERMARK_PAGES`、`WATERMARK_OPACITY`、`WHITE_PAGES`
- 改完 commit + push，網站就會更新

## GitHub Pages

Repository：https://github.com/Russell0123/athology_reviewer
網址：https://russell0123.github.io/athology_reviewer/

Settings → Pages → Source 選 `Deploy from a branch`，Branch 選 `main`，資料夾選 **`/docs`**。
