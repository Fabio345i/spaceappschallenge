from pydantic import BaseModel, EmailStr
from pydantic import BaseModel, Field
from typing import List

class Location(BaseModel):
    name: str
    lat: float
    lon: float

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserPublic(BaseModel):
    id: str
    username: str
    email: EmailStr
    locations: List[Location] = Field(default_factory=list)