import asyncio
import json

from loguru import logger

from app.core.config import rabbitmq_settings
from app.models.parcel import Parcel
from app.services.currency_service import get_usd_to_rub_rate
from app.services.db import get_session
from app.services.delivery_calculator import calculate_delivery_cost
from app.services.queue import get_connection_and_channel

RABBITMQ_URL = rabbitmq_settings.RABBITMQ_URL
QUEUE_NAME = rabbitmq_settings.QUEUE_NAME


async def process_parcel(parcel_data: dict[str, float]):
    try:
        usd_to_rub_rate = await get_usd_to_rub_rate()
        delivery_cost = await calculate_delivery_cost(
            weight=parcel_data["weight"], item_value_usd=parcel_data["item_value"], usd_to_rub_rate=usd_to_rub_rate
        )

        async with get_session() as session:
            new_parcel = Parcel(
                name=parcel_data["name"],
                weight=parcel_data["weight"],
                type_id=parcel_data["parcel_type_id"],
                content_value_usd=parcel_data["item_value"],
                delivery_cost_rub=delivery_cost,
            )
            session.add(new_parcel)
            await session.commit()

        logger.info(f"Parcel registered successfully: {new_parcel.id}")
    except Exception as e:
        logger.error(f"Failed to process parcel: {e}")


async def handle_message(message):
    parcel_data = json.loads(message.body.decode())
    logger.info(f"Received parcel data: {parcel_data}")
    await process_parcel(parcel_data)


async def consume_from_queue():
    rabbitmq_url = RABBITMQ_URL
    connection, channel = await get_connection_and_channel(rabbitmq_url, QUEUE_NAME)

    async with connection:
        queue = await channel.get_queue(QUEUE_NAME)
        async with queue.iterator() as queue_iterator:
            async for message in queue_iterator:
                async with message.process():
                    await handle_message(message)


if __name__ == "__main__":
    asyncio.run(consume_from_queue())
