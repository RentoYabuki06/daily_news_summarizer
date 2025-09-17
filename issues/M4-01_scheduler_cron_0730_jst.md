---
title: "[M4-01] APScheduler で毎日 07:30 JST 実行"
phase: M4
id: M4-01
---

- 目的
  - サーバ起動時にスケジューラを起動し、毎日 07:30 JST にパイプラインを実行する。
- 実装手順
  - `app/config.py` に `APP_TZ` / `CRON_HOUR` / `CRON_MINUTE` を追加。
  - `app/services/scheduler.py` に `start_scheduler()` / `shutdown_scheduler()` を実装。
  - `app/main.py` のアプリ起動/終了時に start/shutdown を呼び出す。
- スケルトン（参考）
  
  from apscheduler.schedulers.background import BackgroundScheduler
  from apscheduler.triggers.cron import CronTrigger
  import asyncio
  from app.config import settings
  from app.services.pipeline import run_pipeline

  scheduler = None

  def start_scheduler(app=None):
      global scheduler
      if scheduler:
          return
      scheduler = BackgroundScheduler(timezone=settings.APP_TZ)
      trigger = CronTrigger(hour=settings.CRON_HOUR, minute=settings.CRON_MINUTE, timezone=settings.APP_TZ)
      scheduler.add_job(lambda: asyncio.run(run_pipeline()), trigger, id="daily-pipeline", replace_existing=True)
      scheduler.start()

  def shutdown_scheduler():
      global scheduler
      if scheduler:
          scheduler.shutdown()
          scheduler = None
  
- 受け入れ基準(AC)
  - 起動時にスケジューラ開始のログが出力される。
  - Cron 時刻到来でパイプラインが実行される（検証時は時刻を短縮設定）。
- テスト観点
  - ジョブ登録の存在、タイムゾーン設定が反映されていること。
- 依存関係
  - [M2-05] パイプライン実装と `articles.upsert`