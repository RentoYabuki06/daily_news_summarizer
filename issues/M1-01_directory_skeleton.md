---
title: "[M1-01] ディレクトリと空ファイルの作成"
phase: M1
id: M1-01
---

- 目的
  - 仕様書の固定ディレクトリ構成を作成し、空ファイルを配置する。
- 実装手順
  - 以下のディレクトリ/ファイルを作成（中身は空または雛形）。
    - app/{__init__.py, main.py, config.py, deps.py}
    - app/routers/{digest.py, admin.py}
    - app/services/{scheduler.py, pipeline.py, collect.py, extract.py, summarize.py}
    - app/repositories/{db.py, articles.py, digests.py}
    - app/models/{article.py, digest.py}
    - data/{feeds.yml, news.db}
    - tests/{test_collect.py, test_extract.py, test_summarize.py}
    - .env.example, requirements.txt, README.md, Makefile
- 受け入れ基準(AC)
  - 上記の全ファイルとディレクトリが存在する。
- テスト観点
  - ファイル/ディレクトリの存在確認（スクリプト or 手動）。
- 依存関係
  - なし