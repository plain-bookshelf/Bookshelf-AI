from fastapi import FastAPI
from pydantic import BaseModel
from recommendation_engine import recommend_books

app = FastAPI()

class BookInfo(BaseModel):
    title: str

@app.post("/recommend_books")
async def get_recommendations(book: BookInfo):
    recs = recommend_books(book.title)
    return {
        "input_book": book.title,
        "recommendations": recs
    }

# uvicorn main:app --reload