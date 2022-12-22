from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean, text
from .db import Base
from sqlalchemy.orm import relationship, backref


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    gender = Column(String, nullable=False)


class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    user = relationship("User")
