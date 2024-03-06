from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from src.database.manager import SessionDepend

from .schemas import UserDTO, UserUpdate, UserResponse

from .repos import UserRepository

from src.core.response import BaseResponse
from src.core.exception import BaseHTTPException

from .depends import PermissionDependency, availability


router: APIRouter = APIRouter(
    prefix='/user',
    tags=['User'],
    dependencies=[Depends(PermissionDependency()), Depends(availability)]
)


@router.get('/{username}', response_model=BaseResponse[UserResponse])
async def user_get(username: Annotated[str, Path(min_length=1, max_length=32)],
                   session: Annotated[AsyncSession, Depends(SessionDepend)]):
    user_schema: UserUpdate = UserUpdate(username=username)
    user_db: UserDTO | None = await UserRepository(session).get(user_schema, many=False)
    if user_db:
        return BaseResponse(status='success', data=user_db)
    raise BaseHTTPException(status_code=status.HTTP_404_NOT_FOUND, msg='Not found')


@router.get('', response_model=BaseResponse[list[UserResponse]])
async def users_get(session: Annotated[AsyncSession, Depends(SessionDepend)]):
    users_db = await UserRepository(session).get(UserUpdate())
    return BaseResponse(status='success', data=(UserResponse.model_validate(user, from_attributes=True) for user in users_db))


@router.put('/{username}/update', response_model=BaseResponse[UserUpdate])
async def user_update(username: Annotated[str, Path(min_length=1, max_length=32)],
                      user: UserUpdate,
                      session: Annotated[AsyncSession, Depends(SessionDepend)]):
    user_db: UserDTO | None | str = await UserRepository(session).update(username=username, user=user)
    if isinstance(user_db, UserDTO):
        return BaseResponse(status='success', data=user_db)
    if user_db == 'IntegrityError':
        raise BaseHTTPException(status_code=status.HTTP_400_BAD_REQUEST, msg='Username is already exists')
    if user_db is None:
        raise BaseHTTPException(status_code=status.HTTP_404_NOT_FOUND, msg='Not found')
    raise BaseHTTPException(status_code=status.HTTP_400_BAD_REQUEST, msg='Unknown error')

