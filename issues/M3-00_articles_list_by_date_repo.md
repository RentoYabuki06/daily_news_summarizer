---
title: "[M3-00] repositories: 当日記事の取得 `articles.list_by_date`"
phase: M3
id: M3-00
---

- 目的
  - ダイジェスト生成用に当日(YYYY-MM-DD)の記事一覧を取得する repository 関数を追加する。
- 実装手順
  - `app/repositories/articles.py` に `def list_by_date(date: str) -> list[dict]` を実装。
    - `published_at` の日付一致、または `created_at` の日付一致で当日分を返す（最小要件では created_at 基準でも可）。
  - `app/services/pipeline.py` のダイジェスト生成からこの関数を使用。
- 受け入れ基準(AC)
  - 指定日付のレコードが 0件以上の配列で返る。
- テスト観点
  - ダミーデータを挿入し、当日/前日で件数が変わること。
- 依存関係
  - [M2-01] SQLite 初期化と repositories 実装