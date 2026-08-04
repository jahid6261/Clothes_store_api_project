from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.ai.models import phi3
from src.ai.prompt import build_prompt
from src.products.service import get_products_for_ai


async def chat_service(
    db: AsyncSession,
    question: str,
):
    products = await get_products_for_ai(db)

    context = ""

    if products:
        for product in products:
            context += f"""
Product Name: {product.name}
Category: {product.category.name}
Price: {product.price}
Description: {product.description}
Available: {"Yes" if product.is_available else "No"}
"""

            
            for variant in product.variants:
                context += f"""
Size: {variant.size}
Color: {variant.color}
Stock: {variant.stock}
SKU: {variant.sku}
"""

            context += "\n--------------------------------\n"

    else:
        context = "No products available."

    
    prompt = build_prompt(
        user_question=question,
        context=context,
    )

    
    messages = [
        {
            "role": "user",
            "content": prompt,
        },
    ]

    def generate():
        try:
            stream = phi3(messages)

            for chunk in stream:
                if "message" in chunk:
                    yield chunk["message"]["content"]

        except Exception as e:
            yield f"\nError: {str(e)}"

    return StreamingResponse(
        generate(),
        media_type="text/plain",
    )