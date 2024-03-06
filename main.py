from typing import AsyncGenerator
from fastapi import FastAPI

from src import UserRouter, AuthRouter

from src.database import db_manager

from src.core import BaseHTTPException, base_exception_handler


async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    app.include_router(UserRouter); app.include_router(AuthRouter)

    await db_manager.connect(create_all=True, expire_on_commit=False)
    print('Start')
    yield
    print('End')


app = FastAPI(lifespan=lifespan,
                exception_handlers={
                BaseHTTPException: base_exception_handler
                }
                )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', port=80, host='0.0.0.0', reload=True)

