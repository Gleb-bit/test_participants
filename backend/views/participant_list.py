from typing import List, Optional

from fastapi import APIRouter, Depends
from fastapi.params import Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.database_conf import get_session
from core.sqlalchemy.crud import Crud
from models.participants import ParticipantReadModel, GenderEnum
from tables.participants import Participant

list_router = APIRouter()
crud = Crud(Participant)


@list_router.get("/list", response_model=List[ParticipantReadModel])
async def get_list_participants(
    first_name: Optional[str] = Query(None, description="Фильтрация по имени"),
    last_name: Optional[str] = Query(None, description="Фильтрация по фамилии"),
    gender: Optional[GenderEnum] = Query(None, description="Фильтрация по полу"),
    sort_field: Optional[str] = Query(None, description="Поле для сортировки"),
    sort_order: Optional[str] = Query(
        "asc", description="Порядок сортировки: asc или desc"
    ),
    session: AsyncSession = Depends(get_session),
):
    return await crud.list(
        session=session,
        sort_field=sort_field,
        sort_order=sort_order,
        first_name=first_name,
        last_name=last_name,
        gender=gender,
    )
