from fastapi import APIRouter,Depends,File,status,UploadFile,Query
from sqlalchemy.ext.asyncio import AsyncSession


from src.utils.db import get_db
from src.products.schemas import( CategorySchema,CategoryResponseSchema,CategoryUpdateSchema,CategoryPatchSchema,
                                 CategoryBulkDeleteSchema,ProductSchema,ProductResponseSchema,ProductPatchSchema,
                                 ProductPutSchema,ProductBulkDeleteSchema, ProductVariantCreateSchema,ProductVariantResponseSchema,
                                 ProductImageResponseSchema ,ProductListResponseSchema

)

from src.products.service import (create_category,all_category,category_by_id,update_category,
  patch_category,delete_category,bulk_delete_category,create_product,
put_product,patch_product,delete_product,product_bulk_delete,create_product_variant,get_product_variants ,
create_bulk_variant ,create_bulk_products ,upload_product_images_service ,get_product_service,
product_by_id ,delete_product_image        
)

from typing import List,Annotated

from decimal import Decimal
products_router=APIRouter(prefix="/products",tags=[" Products"])



# all Category  Routes 
@products_router.post("/categories",response_model=CategoryResponseSchema)

async def create_categories(request:CategorySchema,db:AsyncSession=Depends(get_db)):

    return await create_category(request,db)

@products_router.get("/categories",response_model=list[CategoryResponseSchema])

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



# all Products Routes 


@products_router.post("/",response_model=ProductResponseSchema)

async def  product_create(request:ProductSchema,db:AsyncSession=Depends(get_db)):
    return await create_product(request,db)


@products_router.post(
    "/bulk",
    response_model=list[ProductResponseSchema]
   
)
async def create_bulk_products_api(
    request: list[ProductSchema],
    db: AsyncSession = Depends(get_db),
):
    
    return await create_bulk_products(request, db)



@products_router.get("/{product_id}",response_model=ProductResponseSchema,
                     summary="Get Product by Id")


async def get_product(product_id:int,db:AsyncSession=Depends(get_db)):
    return await product_by_id(
        product_id,db
    )



@products_router.get(
    "/",
    response_model=ProductListResponseSchema,
    summary="Get All Products",
)
async def product_get(
    search: Annotated[str | None, Query(description="Search product")] = None,
    category_id: Annotated[int | None, Query(gt=0)] = None,
    min_price: Annotated[Decimal | None, Query(ge=0)] = None,
    max_price: Annotated[Decimal | None, Query(ge=0)] = None,
    sort: Annotated[str, Query(description="Sort products")] = "latest",
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
    db: AsyncSession = Depends(get_db),
):
    return await get_product_service(
        db=db,
        search=search,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        sort=sort,
        page=page,
        limit=limit,
    )




  
@products_router.put("/products_id",response_model=ProductPutSchema)

async def product_put(product_id:int,request:ProductPutSchema,db:AsyncSession=Depends(get_db)):

    return await put_product(product_id,request,db)



@products_router.patch(
    "/{product_id}",
    response_model=ProductResponseSchema,
    summary="Patch Product",
)
async def product_patch(product_id:int,request:ProductPatchSchema,db:AsyncSession=Depends(get_db)):

    return await patch_product(product_id,request,db)

@products_router.delete("/{product_id}")

async def product_delete(product_id:int,db:AsyncSession=Depends(get_db)):
    return await delete_product(product_id,db)

@products_router.delete("/")

async def bulk_product_delete(request:ProductBulkDeleteSchema,db:AsyncSession=Depends(get_db)):

    return await product_bulk_delete(request,db)


## Variant  Routes 

@products_router.post("variants",response_model=ProductVariantResponseSchema)

async def product_variant_create(request:ProductVariantCreateSchema,db:AsyncSession=Depends(get_db)):
    return await create_product_variant(request,db)


@products_router.get(
    "/{product_id}/variants",
    response_model=list[ProductVariantResponseSchema]
)
async def get_product_variants_api(
    product_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await get_product_variants(product_id, db)


@products_router.post("/variants/bulk",response_model=list[ProductVariantResponseSchema])

async def  variant_bulk_crate_api(request:list[ProductVariantCreateSchema],db:AsyncSession=Depends(get_db)):

    return await create_bulk_variant(request,db)




## Iamge Routes 
@products_router.post("/{product_id}/images", status_code=status.HTTP_201_CREATED)
async def upload_product_images(
    product_id: int,
    
    image:UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    return await upload_product_images_service(
       product_id, image,db
    )



@products_router.delete("/images/{image_id}")
async def delete_image_router(
    image_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await delete_product_image(image_id, db)

