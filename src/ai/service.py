from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.ai.prompt import build_prompt
from src.ai.models import phi3
from src.ai.vector_search import search_similar_products

async def chat_service(
    db: AsyncSession,
    question: str,
):
    # 1. Search relevant document chunks using RAG
    results = await search_similar_products(
        db=db,
        query=question,
        limit=3,
    )

    context = ""

    # 2. Build context from retrieved chunks
    if results:
        for chunk, distance in results:

            product = chunk.product

            if not product:
                continue

            context += f"""
Product Name: {product.name}
Category: {product.category.name if product.category else "N/A"}
Price: {product.price}
Description: {product.description}
Available: {"Yes" if product.is_available else "No"}

Relevant Information:
{chunk.content}
"""

            # Product variants
            for variant in product.variants:
                context += f"""
Size: {variant.size}
Color: {variant.color}
Stock: {variant.stock}
SKU: {variant.sku}
"""

            context += "\n--------------------------------\n"

    else:
        context = "No relevant product information found."

    # 3. Build LLM prompt
    prompt = build_prompt(
        user_question=question,
        context=context,
    )

    # 4. Prepare messages
    messages = [
        {
            "role": "user",
            "content": prompt,
        }
    ]

    # 5. Stream LLM response
    def generate():
        try:
            stream = phi3(messages)

            for chunk in stream:
                if "message" in chunk:
                    yield chunk["message"]["content"]

        except Exception as e:
            yield f"\nError: {str(e)}"

    # 6. Return streaming response
    return StreamingResponse(
        generate(),
        media_type="text/plain",
    )