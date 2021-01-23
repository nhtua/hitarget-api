from fastapi import APIRouter


router = APIRouter(tags=["Utils"])


@router.get("/health")
async def health_check():
    return {"health": "OK"}
