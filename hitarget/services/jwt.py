from datetime import datetime, timedelta
from typing import Dict

import jwt
from pydantic import ValidationError

from hitarget.models.user import UserInResponse
from hitarget.core.config import settings


def create_jwt_token(
    jwt_content: Dict[str, str],
    secret_key: str,
    expires_delta: timedelta,
) -> str:
    to_encode = jwt_content.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update(dict(
        exp=expire,
        iss=settings.JWT_ISSUER
    ))
    return jwt.encode(to_encode, secret_key, algorithm=settings.JWT_ALGORITHM)


def create_access_token_for_user(user: UserInResponse) -> str:
    return create_jwt_token(
        jwt_content=user.dict(),
        secret_key=settings.JWT_SECRET,
        expires_delta=timedelta(minutes=settings.JWT_TOKEN_EXPIRE_MINUTES),
    )


def get_email_from_token(token: str, secret_key: str) -> str:
    try:
        return jwt.decode(token, secret_key, algorithms=[settings.JWT_ALGORITHM])['email']
    except jwt.PyJWTError as decode_error:
        raise ValueError("unable to decode JWT token") from decode_error
    except ValidationError as validation_error:
        raise ValueError("malformed payload in token") from validation_error
