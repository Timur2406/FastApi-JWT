from fastapi import APIRouter, Depends, Response, status
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from src.core.exception import BaseHTTPException
from src.core.response import BaseResponse

from src.auth.security import Auth, Credentials

from src.database import SessionDepend

from .schemas import UserBase, UserAuth
from .repos import AuthRepository, User



router: APIRouter = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@router.post('/registration')
async def user_registration(
                            user: UserBase,
                            session: Annotated[AsyncSession, Depends(SessionDepend)],
                            authorized: Annotated[JwtAuthorizationCredentials, Depends(Credentials.refresh_credentials)]
                            ):
    if authorized:
        raise BaseHTTPException(status_code=status.HTTP_403_FORBIDDEN, msg='Already registred')
    
    user_db: User | str | None = await AuthRepository(session).create(user)

    if isinstance(user_db, User):
        return BaseResponse(status='success', data=f'Hello, {user_db.username}!')
    
    if user_db == 'IntegrityError':
        raise BaseHTTPException(status_code=status.HTTP_400_BAD_REQUEST, msg='Username is already exists')
    
    raise BaseHTTPException(status_code=status.HTTP_400_BAD_REQUEST, msg='Unknown error')


@router.post('/login')
async def user_login(user: UserAuth,
                     session: Annotated[AsyncSession, Depends(SessionDepend)],
                     response: Response,
                     authorized: Annotated[JwtAuthorizationCredentials, Depends(Credentials.refresh_credentials)]
                    ):
    if authorized:
        raise BaseHTTPException(status_code=status.HTTP_403_FORBIDDEN, msg='Already authorized')
    
    if user_db:= await AuthRepository(session).verify(user):
        await Auth.login(subject=dict(username=user_db.username,
                                      scopes=user_db.scopes, 
                                      banned=user_db.banned),
                                      response=response),
        return BaseResponse(status='success', data={'status': 'success'})
    raise BaseHTTPException(status_code=status.HTTP_400_BAD_REQUEST, msg='Bad data')


@router.post('/logout')
async def user_logout(response: Response,
                      credentials: Annotated[JwtAuthorizationCredentials, Depends(Credentials.refresh_credentials)]
                      ):
    await Auth.logout(response=response, credentials=credentials)
    return BaseResponse(status='success', data={'status': 'success'})


@router.put('')
async def user_refresh(response: Response,
                       credentials: Annotated[JwtAuthorizationCredentials, Depends(Credentials.refresh_credentials)]
                       ):
    await Auth.refresh_access(credentials=credentials, response=response)
    return BaseResponse(status='success', data={'status': 'success'})

