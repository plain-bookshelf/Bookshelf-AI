from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .data_loader import load_rented_book_titles
from .recommendation_engine import recommend_page_books
from .model import BookUserName

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 또는 ["https://your-frontend.vercel.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/book_post")
async def book_post(u_n: BookUserName):
    titles = load_rented_book_titles(u_n.user_name)
    recs = recommend_page_books(titles[:2], u_n.user_name)
    return recs
    # recs = load_rented_book_titles(u_n.user_name)
    # return recs


# taskkill /F /IM python.exe
# uvicorn Reco_System.main:app --reload
# uvicorn Reco_System.main:app --host 0.0.0.0 --port 8000 --reload