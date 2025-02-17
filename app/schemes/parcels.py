from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ParcelBase(BaseModel):
    name: Annotated[str, Field(description="Name of the parcel")]
    weight: Annotated[float, Field(gt=0, description="Weight in kg")]
    type_id: Annotated[int, Field(description="Type of the parcel")]
    content_value_usd: Annotated[float, Field(gt=0, description="USD value of the parcel")]


class ParcelCreate(ParcelBase):
    pass


class ParcelInDB(ParcelBase):
    id: Annotated[int, Field(description="Parcel ID", ge=1)]
    delivery_cost_rub: Annotated[float | None, Field(gt=0, description="Delivery cost in RUB")]
    session_id: Annotated[str, Field(default=None, description="Session ID")]
    created_at: Annotated[datetime, Field(description="Creation date")]


class ParcelDetial(ParcelInDB):
    _parcel_type: Annotated[object | None, Field(default=None, description="Type of the parcel")]
    type_name: Annotated[str | None, Field(default=None, description="Type name of the parcel")]

    @model_validator(mode="before")
    def set_type_name_from_parcel_type(cls, values):
        parcel_type = values.get("_parcel_type")
        if parcel_type is not None:
            if hasattr(parcel_type, "name"):
                values["type_name"] = parcel_type.name
            elif isinstance(parcel_type, dict):
                values["type_name"] = parcel_type.get("type_name")
        else:
            values["type_name"] = None
        return values

    model_config = ConfigDict(
        orm_mode=True,
        fields={
            "type_id": {"exclude": True},
            "_parcel_type": {"exclude": True},
        },
    )
