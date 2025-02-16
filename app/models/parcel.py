from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from datetime import datetime
from base import Base

class Parcel(Base):
    __tablename__ = 'parcels'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    weight = Column(Float, nullable=False)
    type_id = Column(Integer, ForeignKey('parcel_types.id'), nullable=False)
    content_value_usd = Column(Float, nullable=False)
    delivery_cost_rub = Column(Float, nullable=True)
    session_id = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

class ParcelType(Base):
    __tablename__ = 'parcel_types'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

# Создаем базовые типы посылок
initial_types = [
    ParcelType(name="Одежда"),
    ParcelType(name="Электроника"),
    ParcelType(name="Разное")
]
