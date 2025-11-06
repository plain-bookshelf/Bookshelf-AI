import os
import numpy as np
from sentence_transformers import SentenceTransformer
from .config import EMBED_MODEL
from .db import load_books_from_db

def combine_info(row):
    parts = [
        f"제목: {row.get('title', '')}",
        f"작가: {row.get('writer', '')}",
        f"출판사: {row.get('publisher', '')}",
        f"학교: {row.get('school', '')}",
        f"등록번호: {row.get('id_number', '')}",
        f"청구번호: {row.get('call_num', '')}",
        f"출판일: {row.get('pubdata', '')}",
        f"카테고리: {row.get('catgory', '')}",
        f"내용: {row.get('description', '')}",
    ]
    return " / ".join([p for p in parts if str(p).strip()])


#print("RDS에서 책 데이터 불러오는 중")
books = load_books_from_db()
books["combined_text"] = books.apply(combine_info, axis=1)

#print("임베딩 모델 로딩 중")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
embedder = SentenceTransformer(EMBED_MODEL)
# embedder = SentenceTransformer("sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens")

embedding_path = "./book_embeddings_rds.npy"
if os.path.exists(embedding_path):
    #print("캐시된 임베딩 불러오기 중")
    book_embeddings = np.load(embedding_path)
else:
    #print("DB 데이터 기반 임베딩 계산 중")
    book_embeddings = embedder.encode(
        books["combined_text"].fillna(""),
        convert_to_tensor=False,
        show_progress_bar=True,
    )
    np.save(embedding_path, book_embeddings)
    #print("임베딩 저장 완료")

def retrieve_context(query: str, top_k=50) -> str:
    # print(book_embeddings.shape)
    q_emb = embedder.encode([query], convert_to_tensor=False)[0]
    sims = np.dot(book_embeddings, q_emb) / (
        np.linalg.norm(book_embeddings, axis=1) * np.linalg.norm(q_emb)
    )
    # idx_1984 = books[books["title"].str.contains("1984")].index[0]
    # print("1984 유사도:", sims[idx_1984])
    # print("Top 30 유사도들:", sorted(sims, reverse=True)[:30])
    top_idx = np.argsort(-sims)[:top_k]
    context = "\n\n".join(books.iloc[i]["combined_text"] for i in top_idx)
    return context