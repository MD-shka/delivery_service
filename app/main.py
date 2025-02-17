import uvicorn
from fastapi import FastAPI
from loguru import logger

from app.api.routers.parcels import router

app = FastAPI()

logger.add(
    "app.log",
    format="{time} {level} {message}",
    level="INFO",
    rotation="10 MB",
    retention="10 days",
    compression="zip",
    serialize=True,
)

app.include_router(router, tags=["parcels"])


@logger.catch
def main():
    """Start the FastAPI src"""
    logger.info("Starting the FastAPI app")
    try:
        uvicorn.run("main:app", reload=True)
    except Exception as e:
        logger.error(f"Error starting the app: {e}")


if __name__ == "__main__":
    main()
