from fastapi import APIRouter

router = APIRouter(
    responses={404: {"description": "Not found"}}
)


@router.get("/health")
async def health_check():
    return {"health": "OK"}
