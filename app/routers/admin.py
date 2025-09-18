from fastapi import APIRouter

router = APIRouter(prefix="/admin", tags=["admin"]) 

@router.get("/healthz")
async def healthz():
    return {"status": "ok"}
