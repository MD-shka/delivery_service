from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from new.models.base import Base


class Parcel(Base):
    __tablename__ = "parcels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    weight: Mapped[float] = mapped_column(Float, nullable=False)
    type_id: Mapped[int] = mapped_column(Integer, ForeignKey("parcel_types.id"), nullable=False)
    content_value_usd: Mapped[float] = mapped_column(Float, nullable=False)
    delivery_cost_rub: Mapped[float] = mapped_column(Float, nullable=True)
    session_id: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    parcel_type = relationship("ParcelType", back_populates="parcels")


class ParcelType(Base):
    __tablename__ = "parcel_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    parcels = relationship("Parcel", back_populates="parcel_type", cascade="all, delete-orphan")


# Создаем базовые типы посылок
initial_types = [ParcelType(name="Одежда"), ParcelType(name="Электроника"), ParcelType(name="Разное")]
