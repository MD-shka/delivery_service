from typing import Tuple

import aio_pika


async def get_connection_and_channel(
    rabbitmq_url: str, queue_name: str
) -> Tuple[aio_pika.abc.AbstractRobustConnection, aio_pika.abc.AbstractChannel]:
    connection = await aio_pika.connect_robust(rabbitmq_url)
    async with connection:
        channel = await connection.channel()
        await channel.declare_queue(queue_name, durable=True)
    return connection, channel
