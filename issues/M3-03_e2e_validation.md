---
title: "[M3-03] E2E 最小検証（/run-now → /digest/{today}）"
phase: M3
id: M3-03
---

- 目的
  - 仕様の受け入れ基準(9)を E2E レベルで確認する。
- 実装手順
  - collect/extract をモックし、1件以上の記事が流れる状態を作る。
  - `POST /run-now` 実行後、`GET /digest/{today}` が 200 を返し、Markdown が非空であることを確認。
- 受け入れ基準(AC)
  - `data/news.db` が存在し、`articles` に1件以上挿入される。
  - `digests` に本日の日付の Markdown が保存される。
  - `GET /digest/{today}` が 200 を返す。
- テスト観点
  - API レスポンス検証、DB レコード数、Markdown 非空の確認。
- 依存関係
  - [M3-02] GET /digest/{date} API 実装