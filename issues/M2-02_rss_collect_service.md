---
title: "[M2-02] RSS 収集サービス `collect_from_rss`"
phase: M2
id: M2-02
---

- 目的
  - `feeds.yml` を巡回し、重複URLを除いた `{url,title,published_at,source}` の配列を返す。
- 実装手順
  - `app/services/collect.py` に `def collect_from_rss(feeds_path: str) -> list[dict]` を実装。
  - `tests/test_collect.py` を作成し、重複除去を検証。
- スケルトン（参考）
  
  import feedparser, yaml

  def collect_from_rss(feeds_path: str) -> list[dict]:
      with open(feeds_path, "r") as f:
          feeds = yaml.safe_load(f)
      items, seen = [], set()
      for feed in feeds:
          d = feedparser.parse(feed["rss"])
          for e in d.entries:
              url = getattr(e, "link", None)
              if not url or url in seen:
                  continue
              seen.add(url)
              items.append({
                  "url": url,
                  "title": getattr(e, "title", None),
                  "published_at": getattr(e, "published", None),
                  "source": feed["name"],
              })
      return items
  
- 受け入れ基準(AC)
  - 配列が返り、URL 重複が除去されている。
- テスト観点
  - 重複URLの除去。
  - 取得失敗エントリのスキップ。
- 依存関係
  - [M2-01] SQLite 初期化と repositories 実装