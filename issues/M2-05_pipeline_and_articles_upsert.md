---
title: "[M2-05] パイプライン実装と `articles.upsert`"
phase: M2
id: M2-05
---

- 目的
  - 収集→抽出→要約を連結し、記事を DB に upsert する。
- 実装手順
  - `app/services/pipeline.py` を本実装。
    - `db.init_db()` → `collect_from_rss(settings.FEEDS_PATH)` → `fetch_and_extract(items)` → `summarize_batch(arts)`
    - `articles.upsert(a)` を各記事に対して実行。
- スケルトン（参考）
  
  from app.services.collect import collect_from_rss
  from app.services.extract import fetch_and_extract
  from app.services.summarize import summarize_batch
  from app.repositories import articles, db
  from app.config import settings

  async def run_pipeline():
      db.init_db()
      items = collect_from_rss(settings.FEEDS_PATH)
      arts = await fetch_and_extract(items)
      enriched = summarize_batch(arts, k=5)
      for a in enriched:
          articles.upsert(a)
  
- 受け入れ基準(AC)
  - `POST /run-now` 実行で `data/news.db` が作成され、`articles` に1件以上挿入されうる。
- テスト観点
  - 部分モックで件数推移を確認（収集→抽出→要約→保存）。
- 依存関係
  - [M2-04] 要約サービス `summarize_batch`（句点区切りダミー）