from typing import Annotated
from fastapi import Response, Security, status
from fastapi_jwt.jwt import timedelta
from fastapi_jwt import JwtAuthorizationCredentials, JwtAccessBearerCookie, JwtRefreshBearerCookie
from hashlib import sha256

from config import Settings

from src.core.exception import BaseHTTPException

from .schemas import Subject


class JWTSecurity:
    access_security = JwtAccessBearerCookie(
        secret_key=Settings.JWT_SECRET, 
        access_expires_delta=timedelta(minutes=10),
        refresh_expires_delta=timedelta(hours=1), 
        auto_error=False
        )
    
    refresh_security: JwtRefreshBearerCookie = JwtRefreshBearerCookie.from_other(other=access_security)

    @classmethod
    def set_jwt(
        cls,
        subject: dict,
        response: Response
    ) -> None:
        access_token: str = cls.access_security.create_access_token(subject=subject)
        refresh_token: str = cls.refresh_security.create_refresh_token(subject=subject)
        cls.access_security.set_access_cookie(response=response, access_token=access_token)
        cls.refresh_security.set_refresh_cookie(response=response, refresh_token=refresh_token)

    @classmethod
    def refresh(
        cls,
        credentials: JwtAuthorizationCredentials,
        response: Response
    ) -> None:
        access_token: str = cls.access_security.create_access_token(subject=credentials.subject)
        refresh_token: str = cls.refresh_security.create_refresh_token(subject=credentials.subject)
        cls.access_security.set_access_cookie(response=response, access_token=access_token)
        cls.refresh_security.set_refresh_cookie(response=response, refresh_token=refresh_token)

    @classmethod
    def unset_jwt(
        cls,
        response: Response
    ) -> None:
        cls.access_security.unset_access_cookie(response=response)
        cls.refresh_security.unset_refresh_cookie(response=response)


class Credentials:
    @staticmethod
    async def access_credentials(
                    credentials: Annotated[JwtAuthorizationCredentials, Security(JWTSecurity.access_security)]
        ) -> JwtAuthorizationCredentials:
        if credentials:
            return credentials
        raise BaseHTTPException(status_code=status.HTTP_401_UNAUTHORIZED, msg='Temporary token has expired')

    @staticmethod
    async def refresh_credentials(
                        credentials: Annotated[JwtAuthorizationCredentials, Security(JWTSecurity.refresh_security)]
                        ) -> JwtAuthorizationCredentials:
        if credentials:
            return credentials

    @staticmethod
    async def subject(credentials: JwtAuthorizationCredentials) -> Subject:
        return Subject(**credentials.subject)


class Auth:
    @staticmethod
    async def login(
                    response: Response,
                    subject: dict,
        ) -> None:
        JWTSecurity.set_jwt(response=response, subject=subject)

    @staticmethod 
    async def logout(
        credentials: Annotated[JwtAuthorizationCredentials, Security(Credentials.refresh_credentials)],
        response: Response
    ) -> None:
        if not credentials:
            raise BaseHTTPException(status_code=status.HTTP_401_UNAUTHORIZED, msg='Unauthorized')
        JWTSecurity.unset_jwt(response=response)

    @staticmethod
    async def refresh_access(
                            credentials: Annotated[JwtAuthorizationCredentials, Security(Credentials.refresh_credentials)], 
                            response: Response
                            ) -> None:
        if not credentials:
            raise BaseHTTPException(status_code=status.HTTP_401_UNAUTHORIZED, msg='Unauthorized')
        JWTSecurity.refresh(response=response, credentials=credentials)
    

class PasswordHash:
    @staticmethod
    async def hash(password: str) -> str:
        return sha256(bytes(password, encoding='utf-8')).hexdigest()
    
    @staticmethod
    async def veify_password(password: str, hash: str) -> bool:
        return sha256(bytes(password, encoding='utf-8')).hexdigest() == hash
        
        