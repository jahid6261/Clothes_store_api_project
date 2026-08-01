import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.db import DB_Session  
from src.users.models import UserModel, UserRole
from src.products.models import Category, Product, ProductVariant, ProductImage
from src.orders.models import Cart, CartItem, Order, OrderItem
from src.utils.security import hash_password
from src.utils.settings import settings


async def create_admin(db: AsyncSession):
    
    result = await db.execute(
        select(UserModel).where(UserModel.email == settings.ADMIN_EMAIL)
    )
    admin = result.scalar_one_or_none()

    if admin:
        print("[INFO] Admin user already exists.")
        return admin

    
    new_admin = UserModel(
        first_name="Super",
        last_name="Admin",
        email=settings.ADMIN_EMAIL,
        password=hash_password(settings.ADMIN_PASSWORD),
        role=UserRole.admin,
        number="01828635650",
        address="Chittagong",
        is_active=True,
        verification_token=None,
        verification_token_expire=None,
    )

    
    try:
        db.add(new_admin)
        await db.commit()
        await db.refresh(new_admin)
        print("[SUCCESS] Admin created successfully")
        return new_admin
    except Exception as e:
        await db.rollback()
        print(f"[ERROR] Failed to create admin: {e}")
        raise



async def main():
    async with DB_Session() as db:  
        await create_admin(db)


if __name__ == "__main__":
    asyncio.run(main())