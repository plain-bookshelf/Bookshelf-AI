from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .data_loader import load_rented_book_titles
from .recommendation_engine import recommend_page_books, init_if_needed
from .model import BookUserName

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 또는 ["https://your-frontend.vercel.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 앱 시작할 때 가벼운 초기화 + 백그라운드 워밍업 시작
@app.on_event("startup")
async def _startup():
    init_if_needed()


@app.post("/book_post")
async def book_post(u_n: BookUserName):
    titles = load_rented_book_titles(u_n.user_name)[:2]
    recs = recommend_page_books(titles, u_n.user_name)
    return recs
    # recs = load_rented_book_titles(u_n.user_name)
    # return recs


# taskkill /F /IM python.exe
# uvicorn Reco_System.main:app --reload
# uvicorn Reco_System.main:app --host 0.0.0.0 --port 8000 --reload