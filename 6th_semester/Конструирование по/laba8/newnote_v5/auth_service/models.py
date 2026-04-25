from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from auth_service.database import Base

class User(Base):
    __tablename__ = "users"
    id               = Column(Integer, primary_key=True, index=True)
    email            = Column(String, unique=True, index=True, nullable=False)
    phone            = Column(String, unique=True, nullable=True)
    password_hash    = Column(String, nullable=True)
    role             = Column(String, default="user", nullable=False)
    sms_code         = Column(String, nullable=True)
    sms_code_expires = Column(DateTime, nullable=True)
    created_at       = Column(DateTime, default=datetime.utcnow)
