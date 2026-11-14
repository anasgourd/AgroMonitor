from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    full_name: str
    password: str
    
    
class UserUpdate(BaseModel):
    username: str
    full_name: str
    password: str
    
class UserResponse(BaseModel):
    user_id: int
    username: str
    full_name: str

    model_config = {
        "from_attributes": True
    }
