# hrmos-esa2confluence

python3.8.5 で実施

```
# コンフルのスペース内の記事を削除するスクリプト（1度に1000件しか取得できないので、複数回実行）
python confluence_archive_all_pages.py
```

```
# コンフルにページを作成するスクリプト
# failed count、failed files として表示されたファイルは作成されていないので手動での対応が必要
python confluence_create_pages.py
```

```
# Esaの記事をローカルにダウンロードするスクリプト
python esa_download_posts.py
```
