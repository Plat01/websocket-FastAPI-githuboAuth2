import logging

import httpx
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse

from schemas import OAuthTokenResponse
from src.config import SETTINGS
from src.dependencys import get_routs_logger

router = APIRouter()


@router.get("/login")
async def login():
    return {"message": "login"}


@ router.get("/github-login")
async def github_login(logger: logging.Logger = Depends(get_routs_logger)):
    logger.debug('%s, %s',f"client_id={SETTINGS.GITHUB_CLIENT_ID}",
                 f"http://{SETTINGS.HOST}:{SETTINGS.PORT}/{SETTINGS.GITHUB_CALLBACK_URL}")

    return RedirectResponse(url=f"https://github.com/login/oauth/authorize?"
                                f"client_id={SETTINGS.GITHUB_CLIENT_ID}&"
                                f"redirect_uri=http://{SETTINGS.HOST}:{SETTINGS.PORT}/{SETTINGS.GITHUB_CALLBACK_URL}",
                            status_code=302  # redirect
                            )


@router.get('/github-callback', response_model=OAuthTokenResponse)
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

    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, headers=headers, data=data)
        response.raise_for_status()

    return OAuthTokenResponse(**response.json())


@ router.get("/logaut")
async def logaut(logger: logging.Logger = Depends(get_routs_logger)):
    pass




