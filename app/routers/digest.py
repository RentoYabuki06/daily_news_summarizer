from fastapi import APIRouter
from datetime import date

router = APIRouter(prefix="/digests", tags=["digests"]) 

@router.get("/{target_date}")
async def get_digest(target_date: date):
    # TODO: implement retrieval logic
    return {"date": target_date.isoformat(), "summary": None, "articles": []}

@router.post("/generate")
async def generate_digest():
    # TODO: implement generation trigger
    return {"status": "accepted"}
