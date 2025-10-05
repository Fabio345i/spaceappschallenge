from bson import ObjectId
from pydantic import BaseModel

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)
    
class SubsetRequest(BaseModel):
    start: str
    end: str  
    minlon: float
    maxlon: float
    minlat: float
    maxlat: float
    variables: list[str] = ["TQV", "TQL", "TQI"]