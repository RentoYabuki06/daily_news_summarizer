# 仕様書: Daily News Summarizer（最小要件 / FastAPI + RSS）

## 0. 目的（LLMが最小単位に分解しやすい要約）
- **毎日 07:30 JST に RSS を巡回**し、新着記事の本文を抽出、**簡易要約（TextRank）**を生成して保存する。
- 当日のまとめ（Markdownダイジェスト）を生成し、APIで取得できる。
- 外部通知（LINE/メール）や生成系要約モデルは**後付け**前提。まずは**最小動作**を確実にする。

---

## 1. スコープ / 非スコープ
### スコープ（MVP）
- RSS一覧（`data/feeds.yml`）の巡回
- 本文抽出（`trafilatura`）
- 簡易要約（句点区切り or TextRankダミー）
- SQLite 永続化（記事・ダイジェスト）
- スケジューラ（APScheduler, 07:30 JST）
- API:
  - `GET /healthz`
  - `POST /run-now`（手動実行）
  - `GET /digest/{date}`（YYYY-MM-DD）

### 非スコープ（次フェーズ）
- 外部通知（LINE/メール/X）
- 生成系LLMによる高品質要約
- ユーザー管理・認可
- 記事重複の類似判定（SimHash 等）

---

## 2. システム構成
- **FastAPI**（REST）
- **APScheduler**（Cron: 07:30 JST）
- **feedparser**（RSS）
- **httpx**（非同期取得）
- **trafilatura**（本文抽出）
- **SQLite**（永続化）
- **pydantic-settings**（環境変数）

---

## 3. ディレクトリ構成（固定）
```

news-summarizer/
├─ app/
│  ├─ **init**.py
│  ├─ main.py
│  ├─ config.py
│  ├─ deps.py
│  ├─ routers/
│  │  ├─ digest.py
│  │  └─ admin.py
│  ├─ services/
│  │  ├─ scheduler.py
│  │  ├─ pipeline.py
│  │  ├─ collect.py
│  │  ├─ extract.py
│  │  └─ summarize.py
│  ├─ repositories/
│  │  ├─ db.py
│  │  ├─ articles.py
│  │  └─ digests.py
│  └─ models/
│     ├─ article.py
│     └─ digest.py
├─ data/
│  ├─ feeds.yml
│  └─ news.db
├─ tests/
│  ├─ test\_collect.py
│  ├─ test\_extract.py
│  └─ test\_summarize.py
├─ .env.example
├─ requirements.txt
├─ README.md
└─ Makefile

```

---

## 4. 依存関係（固定バージョン例）
```

fastapi==0.112.2
uvicorn\[standard]==0.30.6
apscheduler==3.10.4
httpx==0.27.2
feedparser==6.0.11
trafilatura==1.12.2
pydantic-settings==2.4.0

```

---

## 5. 環境変数
`.env`（必須ではない / 既定値あり）
- `APP_TZ=Asia/Tokyo`
- `CRON_HOUR=7`
- `CRON_MINUTE=30`
- `DB_PATH=data/news.db`
- `FEEDS_PATH=data/feeds.yml`

---

## 6. データモデル（SQLiteスキーマ）
- `articles`  
  - `url TEXT PRIMARY KEY`  
  - `title TEXT`  
  - `content TEXT`  
  - `summary TEXT`  
  - `source TEXT`（feeds.yml の name）  
  - `published_at TEXT`（ISO8601; null可）  
  - `created_at TEXT DEFAULT CURRENT_TIMESTAMP`

- `digests`  
  - `date TEXT PRIMARY KEY`（YYYY-MM-DD）  
  - `markdown TEXT`  
  - `created_at TEXT DEFAULT CURRENT_TIMESTAMP`

---

## 7. API 仕様（最小）
### GET `/healthz`
- 200 / `{"ok": true}`

### POST `/run-now`
- 即時に巡回ジョブを非同期発火
- 200 / `{"status":"queued"}`

### GET `/digest/{date}`
- `date`: `YYYY-MM-DD`
- 200 / `{"date":"...", "markdown":"..."}`  
- 404 / `{"detail":"no digest"}`

---

## 8. パイプライン仕様（処理手順）
1. `collect_from_rss()`  
   - `feeds.yml` を読み込み / RSS を巡回  
   - `[{url,title,published_at,source}, ...]` を返す  
   - **重複URL除去**（set）

2. `fetch_and_extract(items)`  
   - `httpx.AsyncClient` で並列取得（timeout 15s）  
   - `trafilatura.extract(html)` で本文抽出  
   - 抽出本文が **160文字未満はスキップ**

3. `summarize_batch(arts, k=5)`  
   - まずは **句点区切りの上位 k 文**（TextRankダミー）  
   - 後日、生成系に差し替え可能な関数構造

4. `articles.upsert(a)`  
   - `url` を PK として UPSERT（タイトル/要約/本文更新）

5. `digests.save(date, markdown)`  
   - 当日分の Markdown を保存（再実行時は上書き）

---

## 9. 受け入れ基準（Acceptance Criteria）
- `make run` で起動後、`POST /run-now` を叩くと以下が満たされる:
  - `data/news.db` が存在し、`articles` に **1件以上**挿入される
  - `digests` に **本日の日付**の Markdown が保存される
  - `GET /digest/{今日}` が **200** を返し、Markdown が含まれる
- `GET /healthz` が **常に 200** を返す
- `feeds.yml` の RSS を1つだけにしても **成功する**

---

## 10. エラーハンドリング/リトライ（最小）
- RSS/HTTP 取得エラー：その項目は **スキップ**（ログ出力）
- 本文抽出が短すぎる：**スキップ**
- 例外は API 応答を落とさない（/healthz は常時200）

---

## 11. ロギング（最小）
- 標準出力に info レベルで以下を出す：
  - 巡回開始/終了、収集件数、抽出成功件数、要約成功件数、ダイジェスト保存

---

## 12. テスト（最小）
- `tests/test_collect.py`  
  - `feeds.yml` をモックし、`collect_from_rss()` が重複を除去して配列を返す
- `tests/test_extract.py`  
  - 短文HTMLはスキップ / 正常HTMLはcontent付きで返す
- `tests/test_summarize.py`  
  - 入力テキストから **最大5文** を返すこと

---

## 13. Makefile（最小）
```

run:
\tuvicorn app.main\:app --reload
test:
\tpytest -q
fmt:
\trufflehog -v || true  # 任意（シークレット誤コミット防止）

````

---

## 14. 初期データ（feeds.yml）
```yaml
- name: NHK_主要
  rss: https://www3.nhk.or.jp/rss/news/cat0.xml
- name: BBC_Japanese
  rss: https://www.bbc.com/japanese/index.xml
````

---

## 15. マイルストーン & イシュー雛形

### マイルストーン

* **M1: 骨組み起動**（/healthz, /run-now, ディレクトリ生成）
* **M2: RSS収集 → 本文抽出 → 要約 → DB保存**
* **M3: ダイジェスト生成 → `/digest/{date}` 公開**
* **M4: スケジューラ（07:30 JST）常時運転**

### GitHub Issue テンプレ（YAML）

```yaml
name: Task
description: 単一タスクを定義
title: "[Task] <短い命名>"
labels: [task, mvp]
body:
  - type: textarea
    id: goal
    attributes:
      label: 目的
      description: 成果物と完了の定義を明記
  - type: textarea
    id: steps
    attributes:
      label: 実装手順
  - type: textarea
    id: ac
    attributes:
      label: 受け入れ基準
  - type: textarea
    id: notes
    attributes:
      label: 備考
```

