

from fastapi import APIRouter ,Depends,status

from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.db import get_db
from src.users.schemas import UserRegisterSchema,UserResponseSchema,UserLoginSchema,TokenSchema
from src.users.service import register,login,profile
from src.depends.auth_depends import get_current_user
from src.users.models import UserModel
user_router=APIRouter(prefix="/users",tags=['Users']
                      
                      )


@user_router.post("/register",response_model=UserResponseSchema,status_code=201)

async def register_user(request:UserRegisterSchema,db:AsyncSession=Depends(get_db)):
    return await register(request,db)


@user_router.post("/login",response_model=TokenSchema,status_code=status.HTTP_200_OK)

async def login_user(request:UserLoginSchema,db:AsyncSession=Depends(get_db)):
    return await login(request,db)


@user_router.get("/profile",response_model=UserResponseSchema)

async def get_profile(
    current_user:UserModel=Depends(get_current_user)
):
    return await profile(current_user)