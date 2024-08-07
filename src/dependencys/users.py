import json
from datetime import timedelta

import httpx
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer

from config import SETTINGS
from schemas import User
from services.redis_client import redis_client

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://github.com/login/oauth/authorize",
    tokenUrl="https://github.com/login/oauth/access_token",
    scopes={"user": "Only read", 'admin': "Read and write"}
)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:

    cached_user = redis_client.get(f"user:{token}")
    if cached_user:
        user_dict = json.loads(cached_user)
        return User(**user_dict)

    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized user",
            headers={"WWW-Authenticate": "Bearer"},
        )

