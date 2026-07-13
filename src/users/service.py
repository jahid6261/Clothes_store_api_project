

from src.users.models import UserModel,UserRole
from src.users.schemas import UserRegisterSchema,UserLoginSchema,UserResponseSchema,TokenSchema

from sqlalchemy import select
from fastapi import HTTPException,status

from sqlalchemy.ext.asyncio import AsyncSession 
from src.utils.security import hash_password,verify_password,encode_access_token
from src.utils.security import settings
from sqlalchemy.exc  import IntegrityError,SQLAlchemyError

async def register(request:UserRegisterSchema,db:AsyncSession):


       # Check email
    email_query = await db.scalar(
        select(UserModel).where(
            UserModel.email == request.email.strip().lower()
        )
    )

    if email_query:
        raise HTTPException(
            status_code=400,
            detail="Email already exists."
        )

    # Create user
    new_user = UserModel(
        first_name=request.first_name.strip(),
        last_name=request.last_name.strip(),
        email=request.email.strip().lower(),
        password=hash_password(request.password),
        number=request.number.strip(),
        address=request.address.strip(),
        role=UserRole.user,
    )

    db.add(new_user)

    try:
        await db.commit()
        await db.refresh(new_user)

    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Email already exists."
        )

    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error occurred."
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

    if not user or not verify_password(request.password, user.password):
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
    
   

    
 

   