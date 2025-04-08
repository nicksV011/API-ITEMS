from pydantic import BaseModel, Field, model_validator
from bson import ObjectId
from datetime import datetime
from typing import Optional

class ItemBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    price: float = Field(..., gt=0, description="Precio debe ser mayor a cero")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: str = Field(alias="_id")

    @classmethod
    def from_db(cls, data: dict):
        if "_id" in data:
            data["_id"] = str(data["_id"])
        return cls(**data)

    class Config:
        from_attributes = True  
        populate_by_name = True  
        json_encoders = {
            ObjectId: lambda v: str(v)
        }

    # Validador para conversiones automáticas
    @model_validator(mode='before')
    def convert_objectid(cls, data: dict) -> dict:
        if isinstance(data.get('_id'), ObjectId):
            data['_id'] = str(data['_id'])
        return data