

from fastapi import APIRouter ,Depends,status

from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.db import get_db
from src.users.schemas import (UserRegisterSchema,UserResponseSchema,UserLoginSchema,TokenSchema,UpdateProfileRequest,
                               UserProfileResponse,ForgotPasswordRequest,ResetPasswordRequest,ChangePasswordRequest)
from src.users.service import (register,login,profile,activate_account_service,update_profile,forget_password,reset_password,change_password)
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



@user_router.get("/activate/{token}")

async def activate_account(token:str,db:AsyncSession=Depends(get_db)):


     return await activate_account_service(token,db)

@user_router.patch("/profile",response_model=UserProfileResponse)

async def profile_update(request:UpdateProfileRequest,user:UserModel=Depends(get_current_user),
                         db:AsyncSession=Depends(get_db)):

    return await update_profile( 
        request,
        user.id,
        db
        )


@user_router.post("/forget-password")
async def forget_user_password (request:ForgotPasswordRequest, db:AsyncSession=Depends(get_db)):

  return  await forget_password(
        db,email=request.email
    )


@user_router.post("/reset-password", status_code=status.HTTP_200_OK)
async def resets_password(
    request: ResetPasswordRequest,
    db: AsyncSession = Depends(get_db),
):
    return await reset_password(
        db=db,
        email=request.email,
        otp=request.otp,
        new_password=request.new_password,
    )


@user_router.patch("/change-password")
async def user_change_password(
    request: ChangePasswordRequest,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await change_password(
        user=current_user,
        current_password=request.current_password,
        new_password=request.new_password,
        confirm_password=request.confirm_password,
        db=db,
    )