---
title: "[M4-02] ロギング最小実装（info レベル）"
phase: M4
id: M4-02
---

- 目的
  - 収集開始/終了、収集件数、抽出成功件数、要約成功件数、ダイジェスト保存などを info ログで出力する。
- 実装手順
  - `app/main.py` 起動時に logging.basicConfig(level=INFO) を設定。
  - `pipeline` の各ステップで info ログ、エラーは warning ログ。
  - `digests.save` 実行時に保存完了ログ。
- 受け入れ基準(AC)
  - `/run-now` 実行時に主要イベントが順に info ログとして出力される。
- テスト観点
  - ログキャプチャで主要メッセージの存在確認。
- 依存関係
  - [M2-05] パイプライン実装と `articles.upsert`