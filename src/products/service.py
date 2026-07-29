
from src.products.models import Category,Product,ProductVariant,ProductImage
from src.products.schemas import (CategorySchema,CategoryResponseSchema,CategoryUpdateSchema,CategoryPatchSchema,
CategoryBulkDeleteSchema,ProductSchema,ProductResponseSchema,ProductPutSchema,
ProductPatchSchema,ProductVariantCreateSchema,ProductVariantResponseSchema,ProductBulkDeleteSchema

                                  )
from sqlalchemy import select,delete, and_, or_,    asc,   desc, func
from decimal import Decimal   


 
   
from fastapi import HTTPException, status,UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.db import DB_Session
from sqlalchemy.orm import selectinload
from src.utils.cloudinary import upload_image ,delete_image
from typing import List,Optional
from sqlalchemy.exc import  IntegrityError,SQLAlchemyError


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


## Product  CRUD Operation start 


async def create_product (request:ProductSchema,db:AsyncSession):
    new_product=Product(
        name=request.name.strip(),
        slug=request.slug.strip(),
        description=request.description.strip(),
        price=request.price,
        category_id=request.category_id,
        is_available=request.is_available


    )

    db.add(new_product)

    try:
         await db.commit() 
         await db.refresh(new_product)
    except IntegrityError :

         await db.rollback()

         raise HTTPException(
             status_code=400,
             detail=" slug already exsits"
         )
    
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to create"
        )
    
    return new_product

async def create_bulk_products(
    request: list[ProductSchema],
    db: AsyncSession
):

    products = [
        Product(**item.model_dump())
        for item in request
    ]

    db.add_all(products)

    try:
        await db.commit()

        for product in products:
            await db.refresh(product)

        return products

    except IntegrityError:
        await db.rollback()

        raise HTTPException(
            status_code=400,
            detail="Duplicate slug"
        )

    except SQLAlchemyError:
        await db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Failed to create products"
        )

async def product_by_id(product_id: int, db: AsyncSession):

    try:
        product = await db.scalar(
            select(Product)
            .where(Product.id == product_id)
            .options(
                selectinload(Product.category),
                selectinload(Product.variants)
                .selectinload(ProductVariant.images),
            )
        )

        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found."
            )

        return product

    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch product."
        )
        
   

    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch product."
        )


async def get_product_service(
    db: AsyncSession,
    search: str | None = None,
    category_id: int | None = None,
    min_price: Decimal | None = None,
    max_price: Decimal | None = None,
    sort: str = "latest",
    page: int = 1,
    limit: int = 10,
):

    try:
        query = select(Product)

        # Search Filter
        if search:
            query = query.where(
                or_(
                    Product.name.ilike(f"%{search}%"),
                    Product.slug.ilike(f"%{search}%"),
                    Product.description.ilike(f"%{search}%"),
                )
            )

        
        if category_id is not None:
            query = query.where(
                Product.category_id == category_id
            )

   
        if min_price is not None:
            query = query.where(
                Product.price >= min_price
            )

        if max_price is not None:
            query = query.where(
                Product.price <= max_price
            )


      
        count_query = select(
            func.count()
        ).select_from(
            query.subquery()
        )

        total = await db.scalar(count_query)


      
        if sort == "price_asc":
            query = query.order_by(
                Product.price.asc()
            )

        elif sort == "price_desc":
            query = query.order_by(
                Product.price.desc()
            )

        elif sort == "oldest":
            query = query.order_by(
                Product.created_at.asc()
            )

        elif sort == "name":
            query = query.order_by(
                Product.name.asc()
            )

        else:
            query = query.order_by(
                Product.created_at.desc()
            )


        query = query.options(
            selectinload(Product.category),
            selectinload(Product.variants)
            .selectinload(ProductVariant.images)
        )


        offset = (page - 1) * limit

        query = query.offset(offset).limit(limit)


        result = await db.execute(query)

        products = result.scalars().all()


        return {
            "total": total,
            "page": page,
            "limit": limit,
            "products": products,
        }


    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch products."
        )

  

async def put_product(
    product_id: int,
    request: ProductPutSchema,
    db: AsyncSession,
):
    try:
        product = await db.scalar(
            select(Product).where(Product.id == product_id)
        )

        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        product.name = request.name.strip()
        product.slug = request.slug.strip()
        product.description = request.description.strip()
        product.price = request.price
        product.is_available = request.is_available
        product.category_id = request.category_id

        await db.commit()
        await db.refresh(product)

        return product

    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product slug already exists."
        )

    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update product."
        )
    


async def patch_product(
    product_id: int,
    request: ProductPatchSchema,
    db: AsyncSession,
):
    try:
        product = await db.scalar(
            select(Product).where(Product.id == product_id)
        )

        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        if request.name is not None:
            product.name = request.name.strip()

        if request.slug is not None:
            product.slug = request.slug.strip()

        if request.description is not None:
            product.description = request.description.strip()

        if request.price is not None:
            product.price = request.price

        if request.is_available is not None:
            product.is_available = request.is_available

        if request.category_id is not None:
            product.category_id = request.category_id

        await db.commit()
        await db.refresh(product)

        return product

    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product name or slug already exists."
        )

    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update product."
        )



async def delete_product(
    product_id: int,
    db: AsyncSession,
):
    try:
        product = await db.scalar(
            select(Product).where(Product.id == product_id)
        )

        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found."
            )

        await db.delete(product)
        await db.commit()

        return {
            "message": "Product deleted successfully."
        }

    except HTTPException:
        raise

    except SQLAlchemyError:
        await db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred."
        )


async def product_bulk_delete(
    request: ProductBulkDeleteSchema,
    db: AsyncSession,
):
    try:
        if not request.ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product IDs are required."
            )

        result = await db.execute(
            delete(Product).where(Product.id.in_(request.ids))
        )

        if result.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No products found."
            )

        await db.commit()

        return {
            "message": f"{result.rowcount} product(s) deleted successfully."
        }

    except HTTPException:
        raise

    except SQLAlchemyError:
        await db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred."
        )



# Product Variant  CRUD 



async def create_product_variant(
    request: ProductVariantCreateSchema,
    db: AsyncSession
):
    result = await db.execute(
        select(Product).where(Product.id == request.product_id)
    )

    product = result.scalar_one_or_none()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    new_product_variant = ProductVariant(
        product_id=request.product_id,
        size=request.size.strip(),
        color=request.color.strip(),
        sku=request.sku.strip(),
        stock=request.stock
    )

    db.add(new_product_variant)

    try:
        await db.commit()
        await db.refresh(new_product_variant)

    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Product variant creation failed"
        )

    return ProductVariantResponseSchema(
        id=new_product_variant.id,
        product_id=new_product_variant.product_id,
        size=new_product_variant.size,
        color=new_product_variant.color,
        sku=new_product_variant.sku,
        stock=new_product_variant.stock
    )


async def create_bulk_variant(
    request: list[ProductVariantCreateSchema],
    db: AsyncSession,
):
    variants = [
        ProductVariant(**item.model_dump())
        for item in request
    ]

    db.add_all(variants)

    try:
        await db.commit()

        for variant in variants:
            await db.refresh(variant)

        return variants

    except SQLAlchemyError:
        await db.rollback()
        raise   

        

    

    




async def get_product_variants(
    product_id: int,
    db: AsyncSession,
):
    # Check if product exists
    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )
    product = result.scalar_one_or_none()

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found."
        )

    # Get all variants for the product
    result = await db.execute(
        select(ProductVariant).where(
            ProductVariant.product_id == product_id
        )
    )

    product_variants = result.scalars().all()

    return product_variants  




## Product Image 
async def upload_variant_image_service(
    variant_id: int,
    image: UploadFile,
    db: AsyncSession
):

    result = await db.execute(
        select(ProductVariant)
        .where(ProductVariant.id == variant_id)
    )

    variant = result.scalar_one_or_none()

    if not variant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Variant not found"
        )

    uploaded = await upload_image(image)

    product_image = ProductImage(
        variant_id=variant_id,
        image_url=uploaded["image_url"],
        public_id=uploaded["public_id"],
    )

    db.add(product_image)

    await db.commit()
    await db.refresh(product_image)

    return product_image



async def delete_product_image(
    image_id: int,
    db: AsyncSession,
):

    image = await db.scalar(
        select(ProductImage)
        .where(ProductImage.id == image_id)
    )

    if image is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )

    try:
        # Delete Cloudinary image
        await delete_image(image.public_id)

        # Delete database record
        await db.delete(image)

        await db.commit()

        return {
            "message": "Image deleted successfully."
        }

    except SQLAlchemyError:
        await db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred."
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete image from Cloudinary."
        )
 
     













    






    




    
    



    


 








    
   





















   













    
