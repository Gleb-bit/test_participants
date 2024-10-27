import math

from config.settings import redis_client
from core.redis.main import RedisCache
from models.participants import ParticipantReadModel


def calculate_distance(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    earth_radius_km = 6371.0

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return earth_radius_km * c


async def get_participants_within_distance(request_user, all_participants, distance_km):
    cache = RedisCache(redis_client)

    user_longitude = request_user.longitude
    user_latitude = request_user.latitude

    cache_key = f"participants_within_distance:{request_user.email}__{distance_km}"
    cached_result = await cache.get_cache(cache_key)
    if cached_result:
        return cached_result

    close_participants = [
        participant
        for participant in all_participants
        if calculate_distance(
            user_latitude, user_longitude, participant.latitude, participant.longitude
        )
        <= distance_km
    ]

    await cache.set_cache(
        cache_key,
        [
            ParticipantReadModel.from_orm(participant).dict()
            for participant in close_participants
        ],
    )

    return close_participants
