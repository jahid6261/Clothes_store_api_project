from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.products.models import Product, DocumentChunkModel
from src.ai.embedding import create_embedding


async def sync_product_rag(
    product_id: int,
    db: AsyncSession
):
    # Product + Category + Variants একসাথে load
    result = await db.execute(
        select(Product)
        .options(
            selectinload(Product.category),
            selectinload(Product.variants)
        )
        .where(Product.id == product_id)
    )

    product = result.scalar_one_or_none()

    if not product:
        return


    # -------------------------
    # Build RAG text
    # -------------------------

    variant_text = []

    for variant in product.variants:

        variant_text.append(
            f"""
            Size: {variant.size}
            Color: {variant.color}
            Stock: {variant.stock}
            SKU: {variant.sku}
            """
        )

    variants = "\n".join(variant_text)


    content = f"""
    Product Name: {product.name}

    Category: {product.category.name if product.category else "N/A"}

    Price: {product.price}

    Description: {product.description}

    Available: {product.is_available}

    Product Variants:
    {variants}
    """


    # -------------------------
    # Create embedding
    # -------------------------

    embedding = create_embedding(content)


    # -------------------------
    # Find existing chunk
    # -------------------------

    result = await db.execute(
        select(DocumentChunkModel)
        .where(
            DocumentChunkModel.product_id == product_id
        )
    )

    chunk = result.scalar_one_or_none()


    # -------------------------
    # Update / Create
    # -------------------------

    if chunk:

        chunk.content = content
        chunk.embedding = embedding

    else:

        chunk = DocumentChunkModel(
            product_id=product_id,
            content=content,
            embedding=embedding
        )

        db.add(chunk)


    await db.commit()

    return chunk