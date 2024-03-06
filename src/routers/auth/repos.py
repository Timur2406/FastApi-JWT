from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.database.model import User
from src.database._abcrepos import Repository

from .schemas import UserBase, UserAuth

from src.auth.security import PasswordHash


class AuthRepository(Repository):
    model: User = User
    session: AsyncSession


    async def create(self,
                     user: UserBase
                     ) -> User | None:
        async with self.session as session:
            try:
                hashed_password: str = await PasswordHash.hash(password=user.password.get_secret_value())
                user_db: User = User(
                    username=user.username,
                    hashed_password=hashed_password
                )
                session.add(user_db)
                await session.commit()

            except IntegrityError:
                return 'IntegrityError'
 
            except:
                return None
            
            return user_db
        

    async def update():
        ...


    async def get(
            self,
            user: UserBase
    ) -> User | None:
        async with self.session as session:
            user_db: User | None = session.get(User, user.username)
        return user_db
    

    async def delete():
        ...


    async def verify(
            self,
            user: UserAuth
    ) -> User | None:
        async with self.session as session:
            user_db: User | None = await session.get(User, user.username)
            if user_db and await PasswordHash.veify_password(password=user.password.get_secret_value(), hash=user_db.hashed_password):
                return user_db
        
