from fastapi import FastAPI

from config import SETTINGS
from routers import auth

app = FastAPI()


@app.get("/")
async def root():
    return {'message': 'Hello world'}


app.include_router(auth.router, tags=['auth'])

if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app',
                host=SETTINGS.SERVICE_HOST,
                port=SETTINGS.SERVICE_PORT,
                reload=True)
