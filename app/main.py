import uvicorn
from fastapi import FastAPI
from loguru import logger

from app.api.routers.parcels import router

app = FastAPI()

logger.add(
    "src.log",
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
    logger.info("Starting the FastAPI src.")
    uvicorn.run("main:src", reload=True)


if __name__ == "__main__":
    main()
