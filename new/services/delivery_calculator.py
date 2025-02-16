from loguru import logger


async def calculate_delivery_cost(weight: float, item_value_usd: float, usd_to_rub_rate: float) -> float:
    try:
        cost = (weight * 0.5 + item_value_usd * 0.01) * usd_to_rub_rate
        logger.info(f"Calculated delivery cost: {cost} RUB")
        return round(cost, 2)
    except Exception as e:
        logger.error(f"Error calculating delivery cost: {e}")
        raise
