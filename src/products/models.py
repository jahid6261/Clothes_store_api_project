from sqlalchemy import Column,Integer,String,Text,DateTime,ForeignKey,Boolean,Numeric
from sqlalchemy.sql import func
from src.utils.db import DBModel
from sqlalchemy.orm import relationship


class Category(DBModel):

    __tablename__ = "categories"

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(100),unique=True,nullable=False)
    slug=Column(String(100),unique=True,nullable=False) 
    description =Column(Text,nullable=False)
    
    created_at=Column(DateTime(timezone=True),server_default=func.now()) 
    updated_at=Column(DateTime(timezone=True), server_default=func.now(),onupdate=func.now())
    products=relationship("Product",back_populates="category",cascade="all,delete-orphan")


class  Product(DBModel):
    __tablename__ = "products"
    id = Column(Integer,primary_key=True,index=True)
    name=Column(String(100),nullable=False)
    slug=Column(String(100),unique=True,nullable=False)
    description=Column(Text,nullable=False)
    is_available=Column(Boolean,default=True)
    price=Column(Numeric(10,2),nullable=False)
    category_id=Column(Integer,ForeignKey("categories.id",ondelete="CASCADE"),nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    category=relationship("Category",back_populates="products")

    variants = relationship( "ProductVariant",back_populates="product",cascade="all, delete-orphan" )      




class ProductVariant(DBModel):
    __tablename__ = "product_variants"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(
        Integer,
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False
    )

    size = Column(String(50), nullable=False)
    color = Column(String(50), nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    sku = Column(String(100), unique=True, nullable=False)
    

    product = relationship("Product", back_populates="variants")
    images = relationship(
    "ProductImage",
    back_populates="variant",
    cascade="all, delete-orphan"
)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
class ProductImage(DBModel):
    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True, index=True)

    variant_id = Column(
        Integer,
        ForeignKey("product_variants.id", ondelete="CASCADE"),
        nullable=False
    )

    image_url = Column(String, nullable=False)
    public_id = Column(String, nullable=False)

    variant = relationship(
        "ProductVariant",
        back_populates="images"
    )
    
 
    