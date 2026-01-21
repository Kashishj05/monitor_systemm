from pydantic import BaseModel, EmailStr, field_validator, Field
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email:EmailStr
    name:str

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=72)
    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str):
        if len(v.encode("utf-8")) > 72:
            raise ValueError("Password too long (max 72 bytes)")
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

class UserResponse(UserBase):
    id:int
    role:str
    created_at:datetime

    class Config:
        orm_mode = True 

class UserUpadte(BaseModel):
    name: Optional[str] = None

    class Config:
        orm_mode= True


class PasswordChange(BaseModel):
    old_password:str
    new_password:str
