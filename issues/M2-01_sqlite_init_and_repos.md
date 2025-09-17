---
title: "[M2-01] SQLite 初期化と repositories 実装"
phase: M2
id: M2-01
---

- 目的
  - SQLite の初期化・接続関数と articles/digests の CRUD を実装する。
- 実装手順
  - `app/config.py` に `Settings` を定義（DB_PATH 既定: `data/news.db`）。
  - `app/repositories/db.py` に `get_conn()` と `init_db()` を実装。
  - `app/repositories/articles.py` に `upsert(a: dict)` を実装。
  - `app/repositories/digests.py` に `save(date, markdown)` / `get(date)` を実装。
- スケルトン（参考）
  - `app/repositories/db.py`
    
    import sqlite3
    from app.config import settings

    def get_conn():
        conn = sqlite3.connect(settings.DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db():
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS articles (
              url TEXT PRIMARY KEY,
              title TEXT,
              content TEXT,
              summary TEXT,
              source TEXT,
              published_at TEXT,
              created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )""")
            cur.execute("""CREATE TABLE IF NOT EXISTS digests (
              date TEXT PRIMARY KEY,
              markdown TEXT,
              created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )""")
            conn.commit()
    
- 受け入れ基準(AC)
  - `init_db()` 実行で DB と2テーブルが作成される。
  - `upsert` / `save` / `get` が正常動作。
- テスト観点
  - 一時DBへの CRUD テスト（DB_PATH を一時パスに変更）。
- 依存関係
  - [M1-03] POST /run-now とダミーpipeline