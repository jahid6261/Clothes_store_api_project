

from src.users.models import UserModel,UserRole,PasswordOTP
from src.users.schemas import (UserRegisterSchema,UserLoginSchema,UserResponseSchema,TokenSchema,
                               UpdateProfileRequest,ResetPasswordRequest,ChangePasswordRequest,ForgotPasswordRequest)

from sqlalchemy import select
from fastapi import HTTPException,status

from sqlalchemy.ext.asyncio import AsyncSession 
from src.utils.security import hash_password,verify_password,encode_access_token,hash_otp
from src.utils.security import settings
from sqlalchemy.exc  import IntegrityError,SQLAlchemyError

from src.utils.verification_token import generate_activation_token,generate_otp
from src.core.task import send_activation_email,send_password_reset_otp_email
from datetime import datetime, timedelta, timezone


from datetime import datetime ,timedelta
async def register(
    request: UserRegisterSchema,
    db: AsyncSession,
):
    # Check email
    email_query = await db.scalar(
        select(UserModel).where(
            UserModel.email == request.email.strip().lower()
        )
    )

    if email_query:
        raise HTTPException(
            status_code=400,
            detail="Email already exists.",
        )

    # Generate verification token
    token = generate_activation_token()

    # Token expiry time
    expire = datetime.utcnow() + timedelta(minutes=15)

    # Create user
    new_user = UserModel(
        first_name=request.first_name.strip(),
        last_name=request.last_name.strip(),
        email=request.email.strip().lower(),
        password=hash_password(request.password),
        number=request.number.strip(),
        address=request.address.strip(),
        role=UserRole.user,
        is_active=False,
        verification_token=token,
        verification_token_expire=expire,
    )

    db.add(new_user)

    try:
        await db.commit()
        await db.refresh(new_user)

    except IntegrityError:
        await db.rollback()

        raise HTTPException(
            status_code=400,
            detail="Email already exists.",
        )

    except SQLAlchemyError:
        await db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Database error occurred.",
        )

    # Send activation email through Celery + RabbitMQ
    send_activation_email(
        to_email=new_user.email,
        first_name=new_user.first_name,
        activation_token=token,
    )

    return UserResponseSchema(
        id=new_user.id,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        email=new_user.email,
        number=new_user.number,
        address=new_user.address,
        role=new_user.role,
        is_active=new_user.is_active,
        created_at=new_user.created_at,
        updated_at=new_user.updated_at,
    )


async def login(request: UserLoginSchema, db: AsyncSession):

    email = request.email.strip().lower()

    user = await db.scalar(
        select(UserModel).where(UserModel.email == email)
    )

    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please verify your email before logging in."
        )

   
    if not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = encode_access_token(
        user.id,
        user.email,
        user.role.value,
    )

    return TokenSchema(
        access_token=access_token,
    )


async def profile(user:UserModel):

 
    
        return UserResponseSchema(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            number=user.number,
            role=user.role,
            address=user.address,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
            
        )


async def activate_account_service(token:str,db:AsyncSession):

     result = await db.execute(
          select(UserModel).where(
               UserModel.verification_token==token
          )
     )        
    
     user = result.scalar_one_or_none()

     if not user:
          raise HTTPException(
               status_code=status.HTTP_404_BAD_REQUEST,
               detail="Invalid verification link"
          )
     if user.is_active:
          raise HTTPException(
               status_code=status.HTTP_404_BAD_REQUEST,
               detail="Account is already activated"
          )
     
     if (
          user.verification_token_expire
          and datetime.utcnow() > user.verification_token_expire
     ):
          raise HTTPException(
               status_code=status.HTTP_404_BAD_REQUEST,
               detail="verification link has expired "
          )
          

     user.is_active = True
     user.verification_token = None
     user.verification_expire = None

     await db.commit()
     await db.refresh(user)

     return {
        "message": "Account activated successfully."
     }


async def update_profile(request:UpdateProfileRequest,user_id:int,db:AsyncSession):

    result= await db.execute(
        select(UserModel).where(
            UserModel.id == user_id
        ))
    

    user= result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    
    if request.first_name is not None:
        user.first_name = request.first_name.strip()

    if request.last_name is not None:
        user.last_name = request.last_name.strip()

    if request.number is not None:
        user.number = request.number.strip()

    if request.address is not None:
        user.address = request.address.strip()

    try:
        await db.commit()
        await db.refresh(user)

    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

    return user

async def forget_password(
    db: AsyncSession,
    email: str,
):
    email = email.strip().lower()

    result = await db.execute(
        select(UserModel).where(
            UserModel.email == email
        )
    )

    user = result.scalar_one_or_none()

    # Do not reveal whether email exists
    if not user:
        return {
            "message": (
                "If this email exists, a password reset OTP "
                "has been sent."
            )
        }

    # Generate OTP
    otp = generate_otp()

    # Hash OTP before storing
    otp_hash = hash_otp(otp)

    # OTP expiry: 5 minutes
    expires_at = (
        datetime.now(timezone.utc)
        + timedelta(minutes=5)
    )

    reset_otp = PasswordOTP(
        user_id=user.id,
        otp=otp_hash,
        expires_at=expires_at,
        is_used=False,
    )

    db.add(reset_otp)

    try:
        await db.commit()

    except SQLAlchemyError:
        await db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )

    # Send OTP asynchronously through Celery + RabbitMQ
    send_password_reset_otp_email(
        to_email=user.email,
        first_name=user.first_name,
        otp=otp,
    )

    return {
        "message": (
            "If this email exists, a password reset OTP "
            "has been sent."
        )
    }

async def reset_password(
    db: AsyncSession,
    email: str,
    otp: str,
    new_password: str,
):
    email = email.strip().lower()

    # Find user
    user = await db.scalar(
        select(UserModel).where(
            UserModel.email == email
        )
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or OTP.",
        )

    # Get latest unused OTP
    result = await db.execute(
        select(PasswordOTP)
        .where(
            PasswordOTP.user_id == user.id,
            PasswordOTP.is_used == False,
        )
        .order_by(
            PasswordOTP.created_at.desc()
        )
    )

    reset_otp = result.scalars().first()

    if not reset_otp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP not found or already used.",
        )

    # Check expiry
    now = datetime.now(timezone.utc)

    expires_at = reset_otp.expires_at

    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(
            tzinfo=timezone.utc
        )

    if expires_at < now:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP has expired.",
        )

    # Verify OTP
    if hash_otp(otp) != reset_otp.otp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or OTP.",
        )

    # Change password
    user.password = hash_password(new_password)

    # OTP can only be used once
    reset_otp.is_used = True

    await db.commit()

    return {
        "message": "Password reset successfully."
    }


async def change_password(
    user: UserModel,
    current_password: str,
    new_password: str,
    confirm_password: str,
    db: AsyncSession,
):
    # Check current password
    if not verify_password(
        current_password,
        user.password,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect.",
        )

    # Check password confirmation
    if new_password != confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password and confirm password do not match.",
        )

    # Prevent using the same password
    if verify_password(
        new_password,
        user.password,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be different from current password.",
        )

    # Hash new password
    user.password = hash_password(new_password)

    await db.commit()
    await db.refresh(user)

    return {
        "message": "Password changed successfully.",
    }
     
   

    
 

   