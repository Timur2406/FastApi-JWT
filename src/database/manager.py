from config import Settings
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from alchemynger import AsyncManager


db_manager: AsyncManager = AsyncManager(path=Settings.DB_DSN)


async def SessionDepend() -> AsyncGenerator[AsyncSession, None]:
    async with db_manager.get_session() as session:
        yield session
        
