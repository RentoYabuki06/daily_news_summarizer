---
title: "[M2-03] 本文抽出サービス `fetch_and_extract`"
phase: M2
id: M2-03
---

- 目的
  - 非同期並列で HTML を取得し、trafilatura で本文抽出。160文字未満はスキップ。
- 実装手順
  - `app/services/extract.py` に `async def fetch_and_extract(items: list[dict]) -> list[dict]` を実装。
  - `tests/test_extract.py` で短文/正常/HTTP失敗をモックして検証。
- スケルトン（参考）
  
  import httpx, asyncio
  import trafilatura

  async def _fetch(client, item):
      try:
          r = await client.get(item["url"])
          r.raise_for_status()
          content = trafilatura.extract(r.text) or ""
          if len(content) < 160:
              return None
          return {**item, "content": content}
      except Exception:
          return None

  async def fetch_and_extract(items):
      async with httpx.AsyncClient(timeout=15.0) as client:
          results = await asyncio.gather(*[_fetch(client, it) for it in items])
      return [r for r in results if r]
  
- 受け入れ基準(AC)
  - 正常ケースで `content` 付き dict を返す。
  - 短文/HTTP失敗はスキップ。
- テスト観点
  - 正常/短文/HTTP失敗の網羅。
- 依存関係
  - [M2-02] RSS 収集サービス `collect_from_rss`