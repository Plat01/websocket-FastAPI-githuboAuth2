from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

from config import SETTINGS
from routers import auth, number_sender

app = FastAPI()


@app.get("/")
async def root():
    return {'message': 'Hello world'}


app.include_router(auth.router, tags=['auth'])
app.include_router(number_sender.router, tags=['random'])

if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app',
                host=SETTINGS.SERVICE_HOST,
                port=SETTINGS.SERVICE_PORT,
                reload=True)
