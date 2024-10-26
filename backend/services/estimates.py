from config.database_conf import get_session
from core.sqlalchemy.orm import Orm
from tables.participants import Participant


async def reset_estimates_number():
    async for session in get_session():
        await Orm.update_field(Participant, {"estimates_number": 0}, session)
