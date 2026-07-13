from fastapi import Depends, HTTPException,status
from sqlalchemy import select
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.security import decode_access_token
from src.utils.db import get_db
from src.users.models import UserModel

security = HTTPBearer()


async def get_current_user(credentials:HTTPAuthorizationCredentials=Depends(security),
                           db:AsyncSession=Depends(get_db)):

    
    try:
        payload=decode_access_token(credentials.credentials)

        user= await db.scalar(
            select(UserModel).where(UserModel.id==payload["user_id"]))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"www-Authenticate":"Bearer"}
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your account is inactive.",
            )

        return user

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )