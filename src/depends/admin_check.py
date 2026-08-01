from fastapi import Depends,HTTPException,status
from src.depends.auth_depends  import get_current_user
from src.users.models import UserRole

async def get_current_admin(current_user=Depends(get_current_user)):

    if current_user.role !=  UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="admin acces required"
        )

    return current_user
