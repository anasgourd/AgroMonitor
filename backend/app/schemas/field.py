from pydantic import BaseModel

# user_id comes from the endpoint path (/users/{user_id}/fields),
# so it is not included in the request body schema.
class FieldCreate(BaseModel):
    field_name: str
    type: str
    area: float
    
class FieldResponse(BaseModel):
    field_id: int
    user_id: int
    field_name: str
    type: str
    area: float

    model_config = {
        "from_attributes": True
    }