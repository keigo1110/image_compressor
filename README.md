# 画像圧縮ツール

指定したサイズに画像を圧縮するGUIツールです。PNG/JPG/JPEG形式に対応しています。

## 機能

- 複数画像の一括圧縮
- 目標サイズの指定（1KB～10000KB）
- 進行状況の表示
- 画質の自動調整
- シンプルで使いやすいインターフェース

## 動作環境

- Python 3.6以上
- Pillow
- tkinter（Pythonに標準搭載）

## インストール方法

```bash
git clone https://github.com/yourusername/image-compression-tool.git
pip install Pillow
```

## 使い方

1. アプリケーションを起動：
```bash
python image_compressor.py
```

2. 「入力フォルダを選択」で圧縮したい画像があるフォルダを選択
3. 「出力フォルダを選択」で圧縮後の画像を保存するフォルダを選択
4. 目標サイズをKB単位で入力（デフォルト：300KB）
5. 「圧縮開始」ボタンをクリック