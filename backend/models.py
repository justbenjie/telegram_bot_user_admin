from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean, text
from .db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    gender = Column(String, nullable=False)


class Admin(Base):
    __tablename__ = "admins"

    user_id = Column(
        Integer,
        # ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
