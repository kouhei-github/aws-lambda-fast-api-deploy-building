from pydantic import BaseModel
from .user import ShowUser

class SalesTarget(BaseModel):
    company_name: str
    email: str
    phone: str
    url: str
    user_id: int

    class Config:
        orm_mode = True

class SalesTargetRelateUser(BaseModel):
    id: int
    company_name: str
    email: str
    phone: str
    url: str
    user_id: int
    owners: ShowUser

    class Config:
        orm_mode = True
