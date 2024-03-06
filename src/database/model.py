from sqlalchemy import Column, Integer, String, Boolean
from datetime import datetime

from .manager import db_manager


class User(db_manager.Base):
    __tablename__ = 'user'

    username = Column(String(32), primary_key=True)
    hashed_password = Column(String, nullable=False)
    email = Column(String)
    registration_date = Column(Integer, nullable=False, default=lambda: int(datetime.now().timestamp()))
    scopes = Column(Integer, nullable=False, default=1)
    banned = Column(Boolean, nullable=False, default=False)

