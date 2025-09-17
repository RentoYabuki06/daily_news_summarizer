---
title: "[M1-04] Makefile と README の最小整備"
phase: M1
id: M1-04
---

- 目的
  - ローカル実行・テストを簡略化し、最小の README を提供する。
- 実装手順
  - `Makefile` を追加
    - `run`: `uvicorn app.main:app --reload`
    - `test`: `pytest -q`
    - `fmt`: `trufflehog -v || true`
  - `README.md` に起動方法・エンドポイント一覧・環境変数を記載。
- 受け入れ基準(AC)
  - `make run` でサーバが起動する。
  - README の記述が仕様と一致。
- テスト観点
  - コマンドの実行性（開発者確認）。
- 依存関係
  - [M1-02] FastAPI起動と /healthz 実装