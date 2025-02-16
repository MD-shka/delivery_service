import aio_pika


async def get_connection_and_channel(rabbitmq_url: str, queue_name: str) -> (aio_pika.connection.Connection, aio_pika.connection.Channel):
    connection = await aio_pika.connect_robust(rabbitmq_url)
    async with connection:
        channel = await connection.channel()
        await channel.declare_queue(queue_name, durable=True)
    return connection, channel
