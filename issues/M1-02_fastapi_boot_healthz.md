---
title: "[M1-02] FastAPI起動と /healthz 実装"
phase: M1
id: M1-02
---

- 目的
  - FastAPI アプリ起動。GET /healthz が常に 200 で {"ok": true} を返す。
- 実装手順
  - `app/main.py` に FastAPI アプリを作成し、ルータをマウント。
  - `app/routers/admin.py` に `/healthz` を実装。
- スケルトン（参考）
  - `app/main.py`
    
    from fastapi import FastAPI
    from app.routers import admin, digest

    app = FastAPI(title="Daily News Summarizer")

    app.include_router(admin.router, tags=["admin"])
    app.include_router(digest.router, prefix="/digest", tags=["digest"])
    
  - `app/routers/admin.py`
    
    from fastapi import APIRouter

    router = APIRouter()

    @router.get("/healthz")
    async def healthz():
        return {"ok": True}
    
- 受け入れ基準(AC)
  - サーバ起動後、GET /healthz が 200 / {"ok": true}。
- テスト観点
  - TestClient で `/healthz` のステータス/ボディ。
- 依存関係
  - [M1-01] ディレクトリと空ファイルの作成