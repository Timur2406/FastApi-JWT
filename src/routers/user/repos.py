from sqlalchemy import Result, Select, Sequence, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.database.model import User
from src.database._abcrepos import Repository

from .schemas import UserUpdate, UserDTO

from src.core.serializer import SerializatorDTO


class UserRepository(Repository):
    model: User = User
    session: AsyncSession


    async def create():
        ...
        

    @SerializatorDTO(UserDTO)
    async def update(self,
                    username: str,
                    user: UserUpdate) -> UserDTO | None:
        async with self.session as session:
            user_db: User = await session.get(User, username)
            if user_db:
                try:
                    [setattr(user_db, attr, value) for attr, value in user.model_dump(exclude_none=True).items()]
                    await session.commit()
                except IntegrityError:
                    return 'IntegrityError'
                except:
                    return 'Unknown'
            return user_db


    @SerializatorDTO(UserDTO)
    async def get(
            self,
            user: UserUpdate,
            many: bool = True
    ) -> UserDTO | Sequence[UserDTO] | None:
        async with self.session as session:
            stmt: Select = select(self.model).filter_by(**user.model_dump(exclude_none=True))
            result: Result = await session.execute(stmt)
            if many:
                return result.scalars().all()
            return result.scalar_one_or_none()
    

    async def delete():
        ...

