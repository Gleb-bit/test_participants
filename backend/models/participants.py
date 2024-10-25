from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum


class GenderEnum(str, Enum):
    male = "Male"
    female = "Female"


class ParticipantModel(BaseModel):
    email: EmailStr
    password: str

    first_name: str
    last_name: Optional[str] = None

    avatar_base64: Optional[str] = None
    avatar_title: Optional[str] = None

    gender: Optional[GenderEnum]


class ParticipantReadModel(BaseModel):
    id: int
    email: EmailStr

    first_name: str
    last_name: Optional[str]

    avatar_url: Optional[str]
    gender: Optional[GenderEnum]

    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


class TokenModel(BaseModel):
    email: EmailStr
