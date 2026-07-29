from sqlalchemy import select,delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status


            
from src.products.models import Product, ProductVariant
from src.orders.models import Cart, CartItem,Order,OrderItem
    
from src.orders.schemas import( CartItemCreateSchema,CartItemUpdateSchema,
                               CreateOrderSchema)
from decimal import Decimal


async def add_to_cart(
    user_id: int,
    request: CartItemCreateSchema,
    db: AsyncSession,
):

    ##   Get user cart
    cart = await db.scalar(
        select(Cart).where(
            Cart.user_id == user_id
        )
    )

    # Create cart
    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        await db.flush()

    # Check product
    product = await db.scalar(
        select(Product).where(
            Product.id == request.product_id
        )
    )

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    # Check variant
    variant = None

    if request.variant_id:

        variant = await db.scalar(
            select(ProductVariant).where(
                ProductVariant.id == request.variant_id,
                ProductVariant.product_id == request.product_id
            )
        )

        if not variant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product variant not found"
            )

        # Check stock
        if variant.stock < request.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient stock"
            )

    # Check existing cart item
    cart_item = await db.scalar(
        select(CartItem).where(
            CartItem.cart_id == cart.id,
            CartItem.product_id == request.product_id,
            CartItem.variant_id == request.variant_id
        )
    )

    # Update quantity
    if cart_item:

        new_quantity = (
            cart_item.quantity + request.quantity
        )

        if variant and variant.stock < new_quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient stock"
            )

        cart_item.quantity = new_quantity

    # Create new cart item
    else:

        cart_item = CartItem(
            cart_id=cart.id,
            product_id=request.product_id,
            variant_id=request.variant_id,
            quantity=request.quantity,
        )

        db.add(cart_item)

    # Save changes
    await db.commit()

    # Reload relationships
    cart_item = await db.scalar(
        select(CartItem)
        .where(
            CartItem.id == cart_item.id
        )
        .options(
            selectinload(CartItem.product),
            selectinload(CartItem.variant).selectinload(
                ProductVariant.images
            )
        )
    )

    return cart_item


async def get_cart_service(user_id:int,db:AsyncSession):
    
    cart = await db.scalar(
        select(Cart)
        .where(
            Cart.user_id == user_id
        )
        .options(
            selectinload(Cart.cart_items)
            .selectinload(CartItem.product),

            selectinload(Cart.cart_items)
            .selectinload(CartItem.variant)
            .selectinload(ProductVariant.images)
        )
    )

  
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found."
        )


    return cart    




async def update_cart_item(
    user_id: int,
    item_id: int,
    request: CartItemUpdateSchema,
    db: AsyncSession
):
   
    cart_item = await db.scalar(
        select(CartItem)
        .join(Cart)
        .where(
            CartItem.id == item_id,
            Cart.user_id == user_id
        )
        .options(
            selectinload(CartItem.product),
            selectinload(CartItem.variant)
            .selectinload(ProductVariant.images)
        )
    )

    #  Check cart item exists
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found."
        )

    #  Validate stock
    if (
        cart_item.variant
        and cart_item.variant.stock < request.quantity
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient stock."
        )

    # update quantiy 
    cart_item.quantity = request.quantity

   
    await db.commit()

    
    cart_item = await db.scalar(
        select(CartItem)
        .where(CartItem.id == item_id)
        .options(
            selectinload(CartItem.product),
            selectinload(CartItem.variant)
            .selectinload(ProductVariant.images)
        )
    )

    return cart_item        
    
async def delete_cart_item(user_id:int,item_id:int,db:AsyncSession):

    
        cart_item = await db.scalar(
            select(CartItem)
            .join(Cart)
            .where(
                CartItem.id == item_id,
                Cart.user_id == user_id
            )
        )
    
      
        if not cart_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found."
            )
    
       
        await db.delete(cart_item)
    
       
        await db.commit()
    
      
        return {
            "message": "Cart item deleted successfully."
        }
    

 

async def clear_user_cart(user_id:int,db:AsyncSession):


   
    cart = await db.scalar(
        select(Cart).where(
            Cart.user_id == user_id
        )
    )

    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found."
        )

   
    await db.execute(
        delete(CartItem).where(
            CartItem.cart_id == cart.id
        )
    )

  
    await db.commit()

    return {
        "message": "Cart cleared successfully."
    }   
    


async def checkout(user_id:int ,db:AsyncSession):
    result = await db.execute(
        select(Cart)
        .where(Cart.user_id == user_id)
        .options(
            selectinload(Cart.cart_items).selectinload(CartItem.product),
            selectinload(Cart.cart_items).selectinload(CartItem.variant),
        )
    )

    cart = result.scalar_one_or_none()

    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found"
        )

    if not cart.cart_items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Your cart is empty"
        )

    items = []
    total_price = Decimal("0.00")

    for item in cart.cart_items:

        if not item.product.is_available:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{item.product.name} is unavailable"
            )

        if item.variant and item.variant.stock < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient stock"
            )

        subtotal = item.product.price * item.quantity
        total_price += subtotal

        items.append(
            {
                "product_id": item.product.id,
                "product_name": item.product.name,
                "variant_id": item.variant.id if item.variant else None,
                "size": item.variant.size if item.variant else None,
                "color": item.variant.color if item.variant else None,
                "price": item.product.price,
                "quantity": item.quantity,
                "subtotal": subtotal,
            }
        )

    return {
        "items": items,
        "total_price": total_price,
    }


async def create_order_service(
    request: CreateOrderSchema,
    user_id: int,
    db: AsyncSession,
):

    try:
        result = await db.execute(
            select(Cart)
            .where(Cart.user_id == user_id)
            .options(
                selectinload(Cart.cart_items)
                .selectinload(CartItem.product),

                selectinload(Cart.cart_items)
                .selectinload(CartItem.variant),
            )
        )

        cart = result.scalar_one_or_none()

        if not cart:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= "Cart not found",
            )

        if not cart.cart_items:
            raise HTTPException(
                400,
                "Cart is empty",
            )

        total_price = Decimal("0.00")

        for item in cart.cart_items:

            if not item.product.is_available:
                raise HTTPException(
                    400,
                    f"{item.product.name} unavailable",
                )

            if (
                item.variant
                and item.variant.stock < item.quantity
            ):
                raise HTTPException(
                    400,
                    "Insufficient stock",
                )

            total_price += (
                item.product.price * item.quantity
            )

        order = Order(
            user_id=user_id,
            first_name=request.first_name.strip(),
            last_name=request.last_name.strip(),
            email=request.email.strip(),
            phone=request.phone.strip(),
            address=request.address.strip(),
            city=request.city.strip(),
            postal_code=request.postal_code.strip(),
            note=request.note.strip()
            if request.note
            else None,
            total_price=total_price,
            paid=False,
            transaction_id=None,
        )

        db.add(order)

        await db.flush()

        for item in cart.cart_items:

            db.add(
                OrderItem(
                    order_id=order.id,
                    product_id=item.product.id,
                    variant_id=item.variant.id
                    if item.variant
                    else None,
                    quantity=item.quantity,
                    price=item.product.price,
                    total_price=item.product.price
                    * item.quantity,
                )
            )

        await db.commit()

        await db.refresh(order)

        result = await db.execute(
            select(Order)
            .where(Order.id == order.id)
            .options(
                selectinload(Order.order_items)
            )
        )

        return result.scalar_one()

    except HTTPException:
        await db.rollback()
        raise

    except Exception as e:
        await db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


 


async def get_my_orders(user_id:int,db:AsyncSession):

    result= await db.execute(
        select(Order).where(
            Order.user_id==user_id
        )
        .options(
            selectinload(Order.order_items)
        )
        .order_by(Order.created_at.desc())
    )
    orders=result.scalars().all()

    if not orders :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No orders found"
        )

    return orders
async def get_order_by_id(
    user_id: int,
    order_id: int,
    db: AsyncSession,
):

    result = await db.execute(
        select(Order)
        .where(
            Order.id == order_id,
            Order.user_id == user_id,
        )
        .options(
            selectinload(Order.order_items)
        )
    )

    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order

async def cancel_order_service(
    order_id: int,
    user_id: int,
    db: AsyncSession,
):

    result = await db.execute(
        select(Order)
        .where(
            Order.id == order_id,
            Order.user_id == user_id,
        )
        .options(
            selectinload(Order.order_items)
        )
    )

    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found."
        )

    if order.status in ["shipped", "delivered", "cancelled"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Order cannot be cancelled because it is {order.status}."
        )

    if order.paid:

        for item in order.order_items:

            if item.variant_id:

                result = await db.execute(
                    select(ProductVariant).where(
                        ProductVariant.id == item.variant_id
                    )
                )

                variant = result.scalar_one_or_none()

                if variant:
                    variant.stock += item.quantity

    order.status = "cancelled"

    await db.commit()
    await db.refresh(order)

    return {
        "status": "success",
        "message": "Order cancelled successfully."
    }
    


 

        
  
        
       
            
 

    











