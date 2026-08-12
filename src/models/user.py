from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from src.utils.db import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(100), nullable=False)

    email = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    password = Column(String(255), nullable=False)

    role = Column(
        String(50),
        nullable=False,
        # default="Employee"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )