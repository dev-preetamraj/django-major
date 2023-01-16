from sqlalchemy import Column, String, Integer, TIMESTAMP, text
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    username = Column(String(100), unique=True)
    email = Column(String(150), unique=True)
    password = Column(String(500), nullable=False)
    profile_picture = Column(String(255))
    is_active = Column(TINYINT, server_default=text('1'))
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))