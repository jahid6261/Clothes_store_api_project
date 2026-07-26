from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal


# Category Schema

class CategorySchema(BaseModel):
    name: str
    slug: str
    description: str


class CategoryResponseSchema(BaseModel):
    id: int
    name: str
    slug: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class CategoryUpdateSchema(BaseModel):
    name: str
    slug: str
    description: str


class CategoryPatchSchema(BaseModel):
    name: str | None = None
    slug: str | None = None
    description: str | None = None


class CategoryBulkDeleteSchema(BaseModel):
    ids: list[int]


# Product Schema

class ProductSchema(BaseModel):
    name: str
    slug: str
    description: str
    is_available: bool
    price: Decimal
    category_id: int

    model_config = ConfigDict(from_attributes=True)


class ProductPutSchema(BaseModel):
    name: str
    slug: str
    description: str
    price: Decimal
    is_available: bool
    category_id: int


class ProductPatchSchema(BaseModel):
    name: str | None = None
    slug: str | None = None
    description: str | None = None
    price: Decimal | None = None
    is_available: bool | None = None
    category_id: int | None = None


# Image Schema

class ProductImageResponseSchema(BaseModel):
    id: int
    image_url: str
    public_id: str

    model_config = ConfigDict(from_attributes=True)


# Variant Response

class ProductVariantSimpleResponseSchema(BaseModel):
    id: int
    size: str
    color: str
    stock: int
    sku: str

    images: list[ProductImageResponseSchema] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class ProductBulkDeleteSchema(BaseModel):
    ids: list[int] = Field(
        ...,
        min_length=1,
        examples=[[1, 2, 3]]
    )


class ProductResponseSchema(BaseModel):
    id: int
    name: str
    slug: str
    description: str
    price: Decimal
    is_available: bool
    category_id: int

    category: CategoryResponseSchema
    variants: list[ProductVariantSimpleResponseSchema] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class ProductListResponseSchema(BaseModel):
    total: int
    page: int
    limit: int
    products: list[ProductResponseSchema]


# Variant Schema

class ProductVariantCreateSchema(BaseModel):
    product_id: int
    size: str
    color: str
    stock: int
    sku: str


class ProductVariantResponseSchema(BaseModel):
    id: int
    product_id: int
    size: str
    color: str
    stock: int
    sku: str

    images: list[ProductImageResponseSchema] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)