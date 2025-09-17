---
title: "[M3-01] ダイジェスト生成と保存"
phase: M3
id: M3-01
---

- 目的
  - 当日分の記事から Markdown ダイジェストを生成し、`digests.save(date, markdown)` で保存する（再実行は上書き）。
- 実装手順
  - `app/services/pipeline.py` に当日(Asia/Tokyo)の日付 `YYYY-MM-DD` 算出処理を追加。
  - 当日分の記事を repositories から取得する関数を追加（例：`articles.list_by_date(date)`）。
  - タイトル/要約/ソースから簡易 Markdown を組み立て、`digests.save` を呼ぶ。
- マークダウン例
  - `# Daily Digest (YYYY-MM-DD)`
  - `- [source] title` / `  - summary...`
- 受け入れ基準(AC)
  - `/run-now` 後に `digests` に本日の日付で1件保存される。
  - 再実行で上書きされる。
- テスト観点
  - 生成 Markdown にタイトル/要約/ソースが含まれる。
  - 上書き動作の確認。
- 依存関係
  - [M2-05] パイプライン実装と `articles.upsert`