from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder

from hitarget.core.mongodb import AsyncIOMotorDatabase, get_database
from hitarget.models.user import UserInResponse
from hitarget.services.authentication import get_current_authorized_user
from hitarget.services.jwt import create_access_token_for_user

router = APIRouter(prefix='/users', tags=["User"])


@router.get("/me", response_description="Get current user information")
async def my_info(
    db: AsyncIOMotorDatabase = Depends(get_database),
    user: UserInResponse = Depends(get_current_authorized_user)
):
    user.token = create_access_token_for_user(user)
    return jsonable_encoder(user)
