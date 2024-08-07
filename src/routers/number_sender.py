import asyncio
import random

from fastapi import APIRouter, Request, WebSocket
from fastapi.responses import HTMLResponse
from sse_starlette.sse import EventSourceResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")  # TODO: replace it

router = APIRouter()


# TODO: generate number with Celery
async def number_generator():
    while True:
        yield random.randint(1, 100)
        await asyncio.sleep(5)


@router.get("/stream")
async def message_stream(request: Request):
    async def event_generator():
        async for number in number_generator():
            if await request.is_disconnected():
                break
            yield {"data": str(number)}

    return EventSourceResponse(event_generator())


@router.get("/number", response_class=HTMLResponse)
async def get_number(request: Request):
    return templates.TemplateResponse('main.html', {"request": request})


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            number = random.randint(1, 100)
            await websocket.send_text(str(number))
            await asyncio.sleep(5)
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()
