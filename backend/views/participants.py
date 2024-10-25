from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from core.utils.image import base64_to_image_with_format
from services.avatar import add_watermark
from tables.participants import Participant, avatars_folder_path
from models.participants import ParticipantModel, ParticipantReadModel, TokenModel
from config import get_session, SECRET_KEY
from core.fastapi.auth import AuthEmail
from core.sqlalchemy.orm import Orm

auth = AuthEmail(SECRET_KEY, TokenModel)

participants_router = APIRouter()


@participants_router.post("/create/", response_model=ParticipantReadModel)
async def register(
    participant: ParticipantModel,
    session: AsyncSession = Depends(get_session),
):
    hashed_password = auth.get_password_hash(participant.password)
    data = {
        "email": participant.email,
        "hashed_password": hashed_password,
        "first_name": participant.first_name,
        "last_name": participant.last_name,
        "gender": participant.gender,
    }

    if participant.avatar_base64:
        avatar_path = avatars_folder_path + participant.avatar_title
        base64_to_image_with_format(participant.avatar_base64, avatar_path)

        add_watermark(
            avatar_path, "etc_files/watermark.png", avatar_path
        )
        data["avatar_url"] = avatar_path

    return await Orm.create(Participant, data, session)


@participants_router.post("/login/")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    user = await Orm.scalar(
        Participant, session, Participant.email == form_data.username
    )

    if not user:
        raise auth.get_credentials_exc("Invalid email")

    if not auth.verify_password(form_data.password, user.hashed_password):
        raise auth.get_credentials_exc()

    access_token, refresh_token = auth.get_tokens({"sub": user.email})

    return {"access_token": access_token, "refresh_token": refresh_token}
