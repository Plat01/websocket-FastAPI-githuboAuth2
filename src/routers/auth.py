import logging
from datetime import timedelta

import httpx
from fastapi import APIRouter, Depends, Security
from fastapi.responses import RedirectResponse

from dependencys.users import get_current_user
from schemas import OAuthTokenResponse, User
from services.redis_client import redis_client
from src.config import SETTINGS
from src.dependencys import get_routs_logger

router = APIRouter()


@router.get("/login")
async def login():
    return {"message": "login"}


@ router.get("/github-login")
async def github_login(logger: logging.Logger = Depends(get_routs_logger)):
    logger.debug('%s, %s',f"client_id={SETTINGS.GITHUB_CLIENT_ID}",
                 f"redirect_uri=http://{SETTINGS.SERVICE_HOST}:{SETTINGS.SERVICE_PORT}/"
                 f"{SETTINGS.GITHUB_CALLBACK}")

    return RedirectResponse(url=f"https://github.com/login/oauth/authorize?"
                                f"client_id={SETTINGS.GITHUB_CLIENT_ID}&"
                                f"redirect_uri=http://{SETTINGS.SERVICE_HOST}:{SETTINGS.SERVICE_PORT}/"
                                f"{SETTINGS.GITHUB_CALLBACK}",
                                status_code=302  # redirect
                            )


@router.get(SETTINGS.GITHUB_CALLBACK, response_model=User)
async def github_callback(code: str,
                          logger: logging.Logger = Depends(get_routs_logger)):
    logger.debug('%s', code)
    token_url = "https://github.com/login/oauth/access_token"
    headers = {"Accept": "application/json"}
    data = {
        "client_id": SETTINGS.GITHUB_CLIENT_ID,
        "client_secret": SETTINGS.GITHUB_CLIENT_SECRET,
        "code": code,
    }

    # send authorization info to github
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, headers=headers, data=data)
        response.raise_for_status()

    oauth_token = OAuthTokenResponse(**response.json())

    # get user information from github
    async with httpx.AsyncClient() as client:
        headers.update({"Authorization": f"Bearer {oauth_token.access_token}"})
        response = await client.get("https://api.github.com/user", headers=headers)
        response.raise_for_status()

        user = User(**response.json(), token=oauth_token.access_token)

        redis_client.setex(
            f"user:{oauth_token.access_token}",
            timedelta(minutes=5),
            user.model_dump_json()
        )

    return user


@ router.get("/logout")
async def logout(logger: logging.Logger = Depends(get_routs_logger),
                 user: User = Security(get_current_user, scopes=['user'])):
    return user
