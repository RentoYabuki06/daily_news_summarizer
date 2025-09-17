---
title: "[M4-03] 設定統合（pydantic-settings）"
phase: M4
id: M4-03
---

- 目的
  - 環境変数でタイムゾーン/cron時刻/DBパス/feedsパスを切り替え可能にする。
- 実装手順
  - `app/config.py` に `Settings` を定義し、既定値を設定。
    - `APP_TZ="Asia/Tokyo"`, `CRON_HOUR=7`, `CRON_MINUTE=30`, `DB_PATH="data/news.db"`, `FEEDS_PATH="data/feeds.yml"`
  - `.env` 読み込み（任意）。
- スケルトン（参考）
  
  from pydantic_settings import BaseSettings

  class Settings(BaseSettings):
      APP_TZ: str = "Asia/Tokyo"
      CRON_HOUR: int = 7
      CRON_MINUTE: int = 30
      DB_PATH: str = "data/news.db"
      FEEDS_PATH: str = "data/feeds.yml"

  settings = Settings()  # type: ignore
  
- 受け入れ基準(AC)
  - 既定値で動作し、環境変数上書きで値が変わる。
- テスト観点
  - 一時的に環境変数を差し替えて値が反映されることを確認。
- 依存関係
  - [M1-01] ディレクトリと空ファイルの作成