---
title: "[M1-05] requirements.txt 固定 & .env.example/feeds.yml の内容整備"
phase: M1
id: M1-05
---

- 目的
  - 実行に必要な依存関係の固定と、環境変数サンプル/初期フィードの用意を行う。
- 実装手順
  - `requirements.txt` を作成/更新（固定バージョン）
    - fastapi==0.112.2
    - uvicorn[standard]==0.30.6
    - apscheduler==3.10.4
    - httpx==0.27.2
    - feedparser==6.0.11
    - trafilatura==1.12.2
    - pydantic-settings==2.4.0
    - pytest（任意だが `test` を使うため追加を推奨）
  - `.env.example` に既定キーを記載
    - APP_TZ=Asia/Tokyo
    - CRON_HOUR=7
    - CRON_MINUTE=30
    - DB_PATH=data/news.db
    - FEEDS_PATH=data/feeds.yml
  - `data/feeds.yml` に初期データを記載
    - 
      - name: NHK_主要
        rss: https://www3.nhk.or.jp/rss/news/cat0.xml
      - name: BBC_Japanese
        rss: https://www.bbc.com/japanese/index.xml
      
- 受け入れ基準(AC)
  - `pip install -r requirements.txt` が成功する。
  - `.env.example` が上記キーを全て含む。
  - `data/feeds.yml` に 2 フィードが定義済み。
- テスト観点
  - requirements の整合性（手動確認）。
  - .env.example / feeds.yml の内容確認。
- 依存関係
  - [M1-01] ディレクトリと空ファイルの作成
