import time
from typing import List, Optional

from fastapi import APIRouter, Depends
from fastapi.params import Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.database_conf import get_session
from core.sqlalchemy.crud import Crud
from core.sqlalchemy.orm import Orm
from models.participants import ParticipantReadModel, GenderEnum
from services.calculations import get_participants_within_distance
from tables.participants import Participant
from views.participants import auth

list_router = APIRouter()
crud = Crud(Participant)


@list_router.get("/list", response_model=List[ParticipantReadModel])
async def get_list_participants(
    first_name: Optional[str] = Query(None, description="Фильтрация по имени"),
    last_name: Optional[str] = Query(None, description="Фильтрация по фамилии"),
    gender: Optional[GenderEnum] = Query(None, description="Фильтрация по полу"),
    distance_km: float = Query(None, description="Дистанция в км"),
    sort_field: Optional[str] = Query(None, description="Поле для сортировки"),
    sort_order: Optional[str] = Query(
        "asc", description="Порядок сортировки: asc или desc"
    ),
    session: AsyncSession = Depends(get_session),
    credentials: ParticipantReadModel = Depends(auth.get_request_user),
):
    request_user = await Orm.scalar(
        Participant, session, Participant.email == credentials.email
    )

    filtered_participants = await crud.list(
        session=session,
        sort_field=sort_field,
        sort_order=sort_order,
        first_name=first_name,
        last_name=last_name,
        gender=gender,
    )

    if distance_km is not None:
        return await get_participants_within_distance(
            request_user, filtered_participants, distance_km
        )

    return filtered_participants
