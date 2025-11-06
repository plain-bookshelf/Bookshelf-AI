from fastapi import APIRouter
from .data_loader import load_rented_book_titles
from .recommendation_engine import recommend_page_books, init_if_needed
from .model import BookUserName

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/book_post")
async def book_post(u_n: BookUserName):
    titles = load_rented_book_titles(u_n.user_name)
    recs = recommend_page_books(titles, u_n.user_name)
    return recs
    # recs = load_rented_book_titles(u_n.user_name)
    # return recs


# taskkill /F /IM python.exe
# uvicorn Reco_System.main:app --reload
# uvicorn Reco_System.main:app --host 0.0.0.0 --port 8000 --reload