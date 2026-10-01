from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.products.models import (
    Product,
    Category,
    ProductVariant,
    DocumentChunkModel,
)
from src.ai.embedding import create_embedding


async def search_similar_products(
    db: AsyncSession,
    query: str,
    limit: int = 3,
):
    query_embedding = create_embedding(query)

    distance = DocumentChunkModel.embedding.cosine_distance(
        query_embedding
    )

    result = await db.execute(
        select(
            DocumentChunkModel,
            distance.label("distance"),
        )
        .options(
            # Product → Category
            selectinload(
                DocumentChunkModel.product
            ).selectinload(
                Product.category
            ),

            # Product → Variants
            selectinload(
                DocumentChunkModel.product
            ).selectinload(
                Product.variants
            ),
        )
        .where(
            DocumentChunkModel.embedding.is_not(None)
        )
        .order_by(distance)
        .limit(limit)
    )

    return result.all()