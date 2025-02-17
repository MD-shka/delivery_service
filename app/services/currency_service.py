import json

import aiohttp
import redis.asyncio as redis
from loguru import logger

from app.core.config import redis_settings

CACHE_KEY = "usd_to_rub_rate"
CACHE_TTL = 3600
CBR_URL = "https://www.cbr-xml-daily.ru/daily_json.js"
REDIS_HOST = redis_settings.REDIS_HOST
REDIS_PORT = redis_settings.REDIS_PORT


async def get_usd_to_rub_rate() -> float:
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        cached_rate = await r.get(CACHE_KEY)
        if cached_rate:
            logger.info(f"Using cached USD to RUB rate: {cached_rate}")
            return float(cached_rate)

        async with aiohttp.ClientSession() as session:
            async with session.get(CBR_URL) as response:
                text_data = await response.text()
                data = json.loads(text_data)
                rate = data["Valute"]["USD"]["Value"]
                await r.set(CACHE_KEY, rate, ex=CACHE_TTL)
                logger.info(f"Fetched and cached USD to RUB rate: {rate}")
                return float(rate)

    except Exception as e:
        logger.error(f"Failed to get USD to RUB rate: {e}")
        raise
