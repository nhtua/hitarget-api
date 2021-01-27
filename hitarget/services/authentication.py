from typing import Optional

from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from starlette import requests, status
from starlette.exceptions import HTTPException as StarletteHTTPException

from hitarget.core.mongodb import AsyncIOMotorDatabase, get_database
from hitarget.core.config import settings
from hitarget.core.errors import EntityDoesNotExist
from hitarget.models.user import UserInResponse
from hitarget.business.user import find_user_by
from hitarget.resources import strings
from .jwt import get_user_id_from_token


class HitargetAPIKeyHeader(APIKeyHeader):
    async def __call__(
        self,
        request: requests.Request,
    ) -> Optional[str]:
        try:
            return await super().__call__(request)
        except StarletteHTTPException as original_auth_exc:
            raise HTTPException(
                status_code=original_auth_exc.status_code,
                detail=strings.AUTHENTICATION_REQUIRED,
            )


def _get_authorization_header(
    api_key: str = Security(HitargetAPIKeyHeader(name="Authorization"))
) -> str:
    try:
        token_prefix, token = api_key.split(" ")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.WRONG_TOKEN_PREFIX,
        )

    if token_prefix != settings.JWT_TOKEN_PREFIX:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.WRONG_TOKEN_PREFIX,
        )

    return token


async def get_current_authorized_user(
    db: AsyncIOMotorDatabase = Depends(get_database),
    token: str = Depends(_get_authorization_header)
) -> UserInResponse:
    try:
        user_id = get_user_id_from_token(token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.MALFORMED_PAYLOAD,
        )

    try:
        return await find_user_by(user_id=user_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.MALFORMED_PAYLOAD,
        )
