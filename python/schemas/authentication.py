from pydantic import BaseModel
from typing import Optional

class UserOut(BaseModel):
    email: str
    name: str
    password: str
    id: int

class UserAuth(BaseModel):
    name: str
    email: str
    password: str

class Login(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None

class SendResetPasswordUrlData(BaseModel):
    email: str
    company_id: str

class ResetPasswordData(BaseModel):
    reset_token: str
    new_password: str