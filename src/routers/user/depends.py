from fastapi import Depends, Request, status
from fastapi_jwt import JwtAuthorizationCredentials

from src.auth.security import Credentials
from src.auth.schemas import Subject

from src.scopes.scopes import Scopes

from src.core.exception import BaseHTTPException


class PermissionDependency:
    async def __call__(self, request: Request, credentials: JwtAuthorizationCredentials = Depends(Credentials.access_credentials)):
        subject: Subject = await Credentials.subject(credentials)
        if route := request.scope.get('route'):
            scopes: int | None = Scopes.scope_methods.get(route.name)
        if scopes not in self.get_permission_nums(subject.scopes):
            raise BaseHTTPException(status_code=status.HTTP_403_FORBIDDEN, msg="no permissions")

    @staticmethod
    def get_permission_nums(scopes):
        return tuple([ind for ind, val in enumerate(bin(scopes)[2:][::-1]) if val=='1'])
    

async def availability(credentials: JwtAuthorizationCredentials = Depends(Credentials.access_credentials)):
    subject: Subject = await Credentials.subject(credentials)
    if subject.banned:
        raise BaseHTTPException(status_code=status.HTTP_403_FORBIDDEN, msg="Banned")

