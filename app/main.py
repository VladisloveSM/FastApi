from fastapi import FastAPI 
from app.models import Feedback
from typing import Optional

app = FastAPI() 

feedbacks = []

sample_product_1 = {
    "product_id": 123,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 599.99
}

sample_product_2 = {
    "product_id": 456,
    "name": "Phone Case",
    "category": "Accessories",
    "price": 19.99
}

sample_product_3 = {
    "product_id": 789,
    "name": "Iphone",
    "category": "Electronics",
    "price": 1299.99
}

sample_product_4 = {
    "product_id": 101,
    "name": "Headphones",
    "category": "Accessories",
    "price": 99.99
}

sample_product_5 = {
    "product_id": 202,
    "name": "Smartwatch",
    "category": "Electronics",
    "price": 299.99
}

sample_products = [sample_product_1, sample_product_2, sample_product_3, sample_product_4, sample_product_5]


@app.get("/product/{product_id}")
async def read_product(product_id: int):
    for product in sample_products:
        if product["product_id"] == product_id:
            return product
    return {"error": "Product not found"}


@app.get("/products/search")
async def search_products(keyword: str, category: Optional[str] = None, limit: Optional[int] = None):
    results = [product for product in sample_products if keyword.lower() in product["name"].lower()]
    if category is not None:
        results = [product for product in results if product["category"] == category]
    if limit is not None:
        results = results[:limit]
    return results

@app.post("/feedback")
async def create_feedback(feedback: Feedback, is_premium: bool = False):
    feedbacks.append(feedback)
    if is_premium:
        message = f"Спасибо, {feedback.name}! Ваш отзыв сохранён. Ваш отзыв будет рассмотрен в приоритетном порядке."
    else:
        message = f"Спасибо, {feedback.name}! Ваш отзыв сохранён."

    return { "message": message }


@app.get("/comments")
async def read_feedbacks():
    return feedbacks