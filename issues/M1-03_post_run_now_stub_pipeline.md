---
title: "[M1-03] POST /run-now とダミーpipeline"
phase: M1
id: M1-03
---

- 目的
  - 手動実行 API を追加し、非同期ジョブ起動の土台（ダミー）を作る。
- 実装手順
  - `app/services/pipeline.py` に `async def run_pipeline() -> None` のダミー関数を追加（`await asyncio.sleep(0)`）。
  - `app/routers/admin.py` に `POST /run-now` を追加し、`BackgroundTasks` で fire-and-forget 実行。
- スケルトン（参考）
  - `app/services/pipeline.py`
    
    import asyncio
    async def run_pipeline():
        await asyncio.sleep(0)
    
  - `app/routers/admin.py`
    
    from fastapi import BackgroundTasks

    @router.post("/run-now")
    async def run_now(background_tasks: BackgroundTasks):
        from app.services.pipeline import run_pipeline
        background_tasks.add_task(run_pipeline)
        return {"status": "queued"}
    
- 受け入れ基準(AC)
  - POST /run-now が 200 / {"status": "queued"} を返す。
- テスト観点
  - TestClient で `/run-now` の応答検証。
- 依存関係
  - [M1-02] FastAPI起動と /healthz 実装