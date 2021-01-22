from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from hitarget.models.user import User, ResponseUser
from hitarget.core.mongodb import AsyncIOMotorDatabase, get_database
from hitarget.business.user import create_user

router = APIRouter(prefix='/users')


@router.post("/register", response_description="Register a new user account")
async def register_user(user: User,
                        db: AsyncIOMotorDatabase = Depends(get_database)):
    created_user = await create_user(db, user)
    response = ResponseUser(**created_user.dict())
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content=jsonable_encoder(response))
