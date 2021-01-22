from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from hitarget.models.user import UserInDB, UserInResponse, FormLogin
from hitarget.core.mongodb import AsyncIOMotorDatabase, get_database
from hitarget.business.user import create_user

router = APIRouter(prefix='/users')


@router.post("/register", response_description="Register a new user account")
async def register_user(user: UserInDB,
                        db: AsyncIOMotorDatabase = Depends(get_database)):
    created_user = await create_user(db, user)
    response = UserInResponse(**created_user.dict())
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content=jsonable_encoder(response))


@router.post("/login", response_description="Login to get your token")
async def login(user: FormLogin,
                db: AsyncIOMotorDatabase = Depends(get_database)):
    return user
