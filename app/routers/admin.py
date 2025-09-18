from fastapi import APIRouter, BackgroundTasks

router = APIRouter(prefix="/admin", tags=["admin"]) 

@router.get("/healthz")
async def healthz():
    return {"status": "ok"}

@router.post("/run-now")
async def run_now(background_tasks: BackgroundTasks):
    from app.services.pipeline import run_pipeline
    background_tasks.add_task(run_pipeline)
    return {"status": "queued"}