

from datetime import datetime

from pydantic import BaseModel,EmailStr,ConfigDict
from src.users.models import UserRole


class UserRegisterSchema(BaseModel):
    first_name:str
    last_name:str
    email:EmailStr
    password:str
    number:str
    address:str|None=None


class UserLoginSchema(BaseModel):
    email:EmailStr
    password:str

class TokenSchema(BaseModel):
    access_token:str
    token_type:str="bearer"


class UserResponseSchema(BaseModel):

    id:int
    first_name:str
    last_name:str
    email:EmailStr
    number:str
    address:str
    role:UserRole
    is_active:bool
    created_at:datetime
    updated_at:datetime


    
class UpdateProfileRequest(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    number: str | None = None
    address: str | None = None

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str

class ForgotPasswordRequest(BaseModel):
    email: str


class ResetPasswordRequest(BaseModel):
    email: str
    otp: str
    new_password: str  

class UserProfileResponse(BaseModel):
    id:int
    first_name:str
    last_name:str
    email:str
    number:str
    address:str
    role:UserRole
    is_active: bool 
    model_config = ConfigDict(from_attributes=True)
        
        