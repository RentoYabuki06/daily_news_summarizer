---
title: "[M2-04] 要約サービス `summarize_batch`（句点区切りダミー）"
phase: M2
id: M2-04
---

- 目的
  - Content を句点「。」で分割し、上位 k 文（最大5）を結合して summary を返す。
- 実装手順
  - `app/services/summarize.py` に `def summarize_batch(arts: list[dict], k: int = 5) -> list[dict]` を実装。
  - `tests/test_summarize.py` を追加（最大5文、境界値）。
- スケルトン（参考）
  
  def summarize_batch(arts, k=5):
      out = []
      for a in arts:
          sents = [s for s in a["content"].split("。") if s.strip()]
          summary = "。".join(sents[:k])
          if summary and not summary.endswith("。"):
              summary += "。"
          out.append({**a, "summary": summary})
      return out
  
- 受け入れ基準(AC)
  - 最大5文に要約される。
- テスト観点
  - 0文/少数文/ちょうど5文/6文以上の境界。
- 依存関係
  - [M2-03] 本文抽出サービス `fetch_and_extract`