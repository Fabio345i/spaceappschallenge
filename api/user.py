from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from bson import ObjectId
from api.models import PyObjectId

class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    name: str
    email: EmailStr

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True