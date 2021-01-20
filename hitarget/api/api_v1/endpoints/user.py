from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from hitarget.models.user import User

router = APIRouter(prefix='/users')


@router.post("", response_description="Register a new user account")
async def register_user(user: User):
    user = jsonable_encoder(user)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=user)
