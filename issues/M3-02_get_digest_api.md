---
title: "[M3-02] GET /digest/{date} API 実装"
phase: M3
id: M3-02
---

- 目的
  - 指定日付 `YYYY-MM-DD` のダイジェストを取得する API を実装する。
- 実装手順
  - `app/routers/digest.py` に `GET /digest/{date}` を実装。
  - `digests.get(date)` を呼び、未保存時は 404 `{ "detail": "no digest" }`。
- スケルトン（参考）
  
  from fastapi import APIRouter, HTTPException
  from app.repositories import digests

  router = APIRouter()

  @router.get("/{date}")
  async def get_digest(date: str):
      row = digests.get(date)
      if not row:
          raise HTTPException(status_code=404, detail="no digest")
      return {"date": date, "markdown": row["markdown"]}
  
- 受け入れ基準(AC)
  - 既存日の取得で 200 / {"date":"...","markdown":"..."}。
  - 未保存日は 404 / {"detail":"no digest"}。
- テスト観点
  - 正常/404 の応答検証。
- 依存関係
  - [M3-01] ダイジェスト生成と保存