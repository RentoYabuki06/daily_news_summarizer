from fastapi import FastAPI

from app.routers import admin, digest

app = FastAPI(title="Daily News Summarizer")

app.include_router(admin.router)
app.include_router(digest.router)

@app.get("/")
async def root():
    return {"message": "Daily News Summarizer API"}
