from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from hitarget.models.user import UserInDB, UserInResponse, FormLogin
from hitarget.core.mongodb import AsyncIOMotorDatabase, get_database
from hitarget.core.errors import EntityDoesNotExist
from hitarget.core import security
from hitarget.business import user as user_bus
from hitarget.resources import strings
from hitarget.services import jwt

router = APIRouter(prefix='/users')


@router.post("/register", response_description="Register a new user account")
async def register_user(user: UserInDB,
                        db: AsyncIOMotorDatabase = Depends(get_database)):
    created_user = await user_bus.create_user(db, user)
    response = UserInResponse(**created_user.dict())
    return JSONResponse(status_code=HTTP_201_CREATED,
                        content=jsonable_encoder(response))


@router.post("/login", response_description="Login to get your token")
async def login(form: FormLogin,
                db: AsyncIOMotorDatabase = Depends(get_database)):
    wrong_login_error = HTTPException(
        status_code=HTTP_400_BAD_REQUEST,
        detail=strings.INCORRECT_LOGIN_INPUT,
    )
    try:
        u = await user_bus.find_user_by(db, email=form.email)
    except EntityDoesNotExist as error:
        raise wrong_login_error from error
    u = UserInDB(**u)
    if not u.check_password(form.password):
        raise wrong_login_error

    response = UserInResponse(**u.dict())
    token = jwt.create_access_token_for_user(response)
    response.token = token
    return JSONResponse(status_code=HTTP_200_OK, content=jsonable_encoder(response))
