from datetime import datetime
from enum import Enum

from sqlalchemy import Column, Integer, String, Boolean, Enum as alchemy_Enum, DateTime
from config import Base

avatars_folder_path = "etc_files/avatars/"


class GenderEnum(Enum):
    Male = "Male"
    Female = "Female"


class Participant(Base):
    """Таблица участника"""

    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    first_name = Column(String, nullable=False)
    last_name = Column(String)

    avatar_url = Column(String)
    gender = Column(alchemy_Enum(GenderEnum), nullable=False)

    created_at = Column(DateTime, default=datetime.now)
    is_active = Column(Boolean, default=True)
