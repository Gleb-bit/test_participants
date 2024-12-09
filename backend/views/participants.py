import random

from fastapi import Depends, APIRouter, HTTPException, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from config.database_conf import get_session
from core.fastapi.email import send_email
from core.utils.image import base64_to_image_with_format
from services.avatar import add_watermark
from tables.participants import Participant, avatars_folder_path
from models.participants import ParticipantModel, ParticipantReadModel, TokenModel
from config.settings import SECRET_KEY
from core.fastapi.auth import AuthEmail
from core.sqlalchemy.orm import Orm

auth = AuthEmail(SECRET_KEY, TokenModel)
participants_router = APIRouter()


@participants_router.post("/{id}/match/")
async def match_participants(
    id: int,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
    credentials: TokenModel = Depends(auth.get_request_user),
):
    request_user = await Orm.scalar(
        Participant, session, Participant.email == credentials.email
    )
    if request_user.estimates_number == 5:
        raise HTTPException(400, "Вы исчерпали дневной лимит")

    participant = await Orm.scalar(Participant, session, Participant.id == id)
    if not participant:
        raise HTTPException(400, "К сожалению, без взаимной симпатии")

    participant_email = participant.email

    background_tasks.add_task(
        send_email,
        [participant_email],
        f"Вы понравились {request_user.first_name}!\n",
        f"Почта участника: {request_user.email}",
    )

    await Orm.update_field(  # обновляем счетчик
        Participant,
        {"estimates_number": Participant.estimates_number + 1},
        session,
        Participant.id == request_user.id,
    )

    return {"email": participant_email}


@participants_router.post("/create/", response_model=ParticipantReadModel)
async def register(
    participant: ParticipantModel,
    session: AsyncSession = Depends(get_session),
):
    hashed_password = auth.get_password_hash(participant.password)
    longitude = random.uniform(0, 200)
    latitude = random.uniform(0, 200)

    data = {
        "email": participant.email,
        "hashed_password": hashed_password,
        "first_name": participant.first_name,
        "last_name": participant.last_name,
        "gender": participant.gender,
        "longitude": longitude,
        "latitude": latitude,
    }

    if participant.avatar_base64:
        avatar_path = avatars_folder_path + participant.avatar_title
        base64_to_image_with_format(participant.avatar_base64, avatar_path)

        add_watermark(avatar_path, "etc_files/watermark.png", avatar_path)
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
