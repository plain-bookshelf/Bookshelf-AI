from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from data_loader import load_rented_book_titles
from recommendation_engine import recommend_books, recommend_page_books

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 또는 ["https://your-frontend.vercel.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BookInfo(BaseModel):
    title: str

@app.post("/recommend_books")
async def get_recommendations(book: BookInfo):
    recs = recommend_books(book.title)
    return {
        "recommendations": recs
    }

@app.get("/book_history")
async def get_history():
    recs = recommend_page_books(load_rented_book_titles())
    return {
        "recommendations_history": recs
    }