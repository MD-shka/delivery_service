from fastapi import APIRouter, Depends, HTTPException, Query, Response
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_session_id
from app.schemes.parcels import ParcelCreate
from app.services.parcel_service import (
    get_parcel_detail_service,
    get_parcel_types_service,
    get_parcels_service,
    register_parcel_service,
)

router = APIRouter()


@router.post("/parcels/register")
async def register_parcel(
    parcel: ParcelCreate,
    response: Response,
    session_id: str = Depends(get_session_id),
):
    """Register a new parcel, return temp_id available in current session"""
    response.set_cookie(key="session_id", value=session_id)
    temp_id = await register_parcel_service(parcel, session_id)
    logger.info(f"Registering parcel, temp_id: {temp_id}")
    return {"temp_id": temp_id}


@router.get("/parcels/types")
async def get_parcel_types(db: AsyncSession = Depends(get_db)):
    """Get all parcel types"""
    return await get_parcel_types_service(db)


@router.get("/parcels")
async def get_parcels(
    page: int = Query(1, gt=0),
    page_size: int = Query(10, gt=0),
    type_id: int = Query(None),
    delivery_cost_rub: bool = Query(None),
    session_id: str = Depends(get_session_id),
    db: AsyncSession = Depends(get_db),
):
    """
    Get a list of parcels for the current session.
    With the ability to filter by type and by calculated value.
    Pagination via page + page_size.
    """
    return await get_parcels_service(
        db=db,
        session_id=session_id,
        page=page,
        page_size=page_size,
        type_id=type_id,
        delivery_cost_rub=delivery_cost_rub,
    )


@router.get("/parcels/{parcel_id}")
async def get_parcel_detail(
    parcel_id: int, session_id: str = Depends(get_session_id), db: AsyncSession = Depends(get_db)
):
    """Get parcel detail by id"""
    parcel_data = await get_parcel_detail_service(db, session_id, parcel_id)
    if not parcel_data:
        raise HTTPException(status_code=404, detail="Parcel not found")
    return parcel_data
