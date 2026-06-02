from datetime import datetime
from pydantic import BaseModel

class AuthRequest(BaseModel):
    username: str
    password: str

class UserRegisterRequest(BaseModel):
    id: int
    email: str
    password: str
    role: str
    org_id: int
    is_active: bool
    created_at: datetime
