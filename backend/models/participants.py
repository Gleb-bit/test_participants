from pydantic import BaseModel, EmailStr, model_validator
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

    longitude: float
    latitude: float

    avatar_base64: Optional[str] = None
    avatar_title: Optional[str] = None

    gender: Optional[GenderEnum]

    @model_validator(mode="before")
    def check_avatar_fields(cls, values):
        avatar_base64 = values.get("avatar_base64")
        avatar_title = values.get("avatar_title")

        if (avatar_base64 is None) != (avatar_title is None):
            raise ValueError(
                "Both avatar_base64 and avatar_title must be provided or neither."
            )

        return values


class ParticipantReadModel(BaseModel):
    id: int
    email: EmailStr

    first_name: str
    last_name: Optional[str]

    avatar_url: Optional[str]
    gender: Optional[GenderEnum]

    longitude: float
    latitude: float

    estimates_number: int

    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

    def dict(self, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        if "created_at" in data:
            data["created_at"] = data["created_at"].isoformat()

        return data


class TokenModel(BaseModel):
    email: EmailStr
