
from src.products.models import Category
from src.products.schemas import (CategorySchema,CategoryResponseSchema,CategoryUpdateSchema,CategoryPatchSchema,
                                  CategoryBulkDeleteSchema
                                  )
from sqlalchemy import select,delete
from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.db import DB_Session


async def create_category(request:CategorySchema,db:AsyncSession):

    new_category=Category(
        name=request.name.strip(),
        slug=request.slug.strip(),
        description=request.description.strip()

    )

    db.add(new_category)

    try:
        await db.commit()
        await db.refresh(new_category)

    except Exception:
        await db.rollback()
        raise Exception("failed to create Category")

    return CategoryResponseSchema(
        

        id=new_category.id,
        name=new_category.name,
        slug=new_category.slug,
        description=new_category.description
        )
    

async def all_category(db:AsyncSession):
    query=select(Category)
    result=await db.execute(query)
    return result.scalars().all()

async def  category_by_id(category_id:int ,db:AsyncSession):
    query=select(Category).where(Category.id==category_id)
    result= await db.execute(query)
    return result.scalars().all()

async def update_category(category_id:int,request:CategoryUpdateSchema,db:AsyncSession):

    result= await db.execute(
        select(Category).where(Category.id==category_id)
    )
    category=result.scalar_one_or_none()

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    category.name=request.name.strip()
    category.slug=request.slug.strip()
    category.description=request.description.strip()

    await db.commit()

    await db.refresh(category)

    return category


async def  patch_category(category_id:int ,request: CategoryPatchSchema, db:AsyncSession):

    result= await db.execute(
        select(Category).where(Category.id == category_id)
    )

    category= result.scalar_one_or_none()

    if category  is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    if request.name is not None:
        category.name= request.name.strip()

    if request.slug is not None:
        category.slug=request.slug.strip()

    if request.description is not None:
        category.description=request.description.strip()

    await db.commit()
    await db.refresh(category)

    return category        
    
async def delete_category(category_id:int,db:AsyncSession
)    :
    
    result= await db.execute(
        select(Category).where(Category.id==category_id)
    )
    category= result.scalar_one_or_none()

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    await db.delete(category)
    await db.commit()

    return  {
        "message": "category deleted successfully"
    }


async def bulk_delete_category(request:CategoryBulkDeleteSchema,db:AsyncSession):

    if not request.ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="categories ids are required"
        )
    
    result= await db.execute(
        delete(Category).where(Category.id.in_(request.ids))
    )

    await db.commit()

    return {
        "message": f"{result.rowcount} category deleted successfully "
    }






