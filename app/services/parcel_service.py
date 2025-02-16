import json
import uuid

import aio_pika
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import rabbitmq_settings
from app.models.parcel import Parcel, ParcelType
from app.schemes.parcels import ParacelDetial, ParcelCreate
from app.services.queue import get_connection_and_channel

RABBITMQ_URL = rabbitmq_settings.RABBITMQ_URL
QUEUE_NAME = rabbitmq_settings.QUEUE_NAME


async def register_parcel_service(parcel_data: ParcelCreate, session_id: str) -> str:
    """Sends a parcel to the RabbitMQ queue, returns a temp_id."""
    temp_id = str(uuid.uuid4())
    message_dict = {
        "name": parcel_data.name,
        "weight": parcel_data.weight,
        "type_id": parcel_data.type_id,
        "content_value_usd": parcel_data.content_value_usd,
        "session_id": session_id,
        "temp_id": temp_id,
    }
    connection, channel = await get_connection_and_channel(RABBITMQ_URL, QUEUE_NAME)
    async with connection:
        body = json.dumps(message_dict).encode()
        await channel.default_exchange.publish(aio_pika.Message(body=body), routing_key=QUEUE_NAME)
        logger.info(f"Parcel with temp_id {temp_id} sent to the queue.")
    return temp_id


async def get_parcel_types_service(db: AsyncSession) -> list[dict[str, object]]:
    """Returns a list of all parcel types(id, name)."""
    result = await db.execute(select(ParcelType))
    tupes = result.scalars().all()
    return [{"id": t.id, "name": t.name} for t in tupes]


async def get_parcels_service(
    db: AsyncSession,
    session_id: str,
    page: int,
    page_size: int,
    type_id: int | None = None,
    delivery_cost_rub: bool | None = None,
) -> list[dict[str, object]]:
    """
    Returns a list of parcels for the current session with optional filters (type, presence of delivery_cost).
    """
    offset = (page - 1) * page_size
    query = select(Parcel).options(selectinload(Parcel.parcel_type)).where(Parcel.session_id == session_id)
    if type_id is not None:
        query = query.where(Parcel.type_id == type_id)
    if delivery_cost_rub is not None:
        if delivery_cost_rub:
            query = query.where(Parcel.delivery_cost_rub.isnot(None))
        else:
            query = query.where(Parcel.delivery_cost_rub.is_(None))

    query = query.offset(offset).limit(page_size)
    result = await db.execute(query)
    parcels = result.scalars().all()

    return [
        {
            "id": p.id,
            "name": p.name,
            "weight": p.weight,
            "parcel_type": p.parcel_type.name if p.parcel_type else None,
            "content_value_usd": p.content_value_usd,
            "delivery_cost_rub": p.delivery_cost_rub,
            "created_at": p.created_at,
        }
        for p in parcels
    ]


async def get_parcel_detail_service(db: AsyncSession, session_id: str, parcel_id: int) -> ParacelDetial | None:
    """
    Returns details of a specific parcel by ID for the current session or None if not found.
    """
    stmt = (
        select(Parcel)
        .options(selectinload(Parcel.parcel_type))
        .where(Parcel.id == parcel_id, Parcel.session_id == session_id)
    )
    result = await db.execute(stmt)
    parcel = result.scalars().first()

    if parcel is None:
        return None

    return ParacelDetial(
        id=parcel.id,
        name=parcel.name,
        weight=parcel.weight,
        type_id=parcel.type_id,
        type_name=parcel.parcel_type.name if parcel.parcel_type else None,
        content_value_usd=parcel.content_value_usd,
        delivery_cost_rub=parcel.delivery_cost_rub,
        session_id=parcel.session_id,
        created_at=parcel.created_at,
        _parcel_type=parcel.parcel_type,
    )
