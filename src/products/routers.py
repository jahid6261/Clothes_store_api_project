from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.db import get_db
from src.products.schemas import( CategorySchema,CategoryResponseSchema,CategoryUpdateSchema,CategoryPatchSchema,
                                 CategoryBulkDeleteSchema

)

from src.products.service import (create_category,all_category,category_by_id,update_category,
                                  patch_category,delete_category,bulk_delete_category
)
products_router=APIRouter(prefix="/products",tags=[" Products"])


@products_router.post("/category",response_model=CategoryResponseSchema)

async def create_categories(request:CategorySchema,db:AsyncSession=Depends(get_db)):

    return await create_category(request,db)

@products_router.get("/all_category",response_model=list[CategoryResponseSchema])

async def all_categories(db:AsyncSession=Depends(get_db)):
    return  await all_category(db)


@products_router.get("/categories/{category_id}")
async def categorirs_by_id(category_id:int,db:AssertionError=Depends(get_db)):
    return await category_by_id(category_id,db)

@products_router.put("/categories/{category_id}",response_model=CategoryResponseSchema)

async def update_categories(category_id:int,request:CategoryUpdateSchema,db:AsyncSession=Depends(get_db)):
    return await update_category(category_id,request,db)

@products_router.patch("/categories/{category_id}",response_model=CategoryResponseSchema)

async def pathc_categories(category_id:int, request:CategoryPatchSchema,db:AsyncSession=Depends(get_db)):
    return await patch_category(category_id,request,db)


@products_router.delete("/categories/{category_id}")

async def delete_categories(category_id:int,db:AsyncSession=Depends(get_db)):
    return await  delete_category(category_id,db)


@products_router.delete("/categories")
async def bulk_delete_categories(request:CategoryBulkDeleteSchema,db:AsyncSession=Depends(get_db)):

    return await bulk_delete_category(request,db)