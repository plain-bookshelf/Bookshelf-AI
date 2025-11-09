# import numpy as np
# import pandas as pd
# import random
# from sentence_transformers import SentenceTransformer
# from sklearn.metrics.pairwise import cosine_similarity
# from .data_loader import load_and_preprocess_data, extract_genres, extract_authors, get_user_school_id
#
#
# # 모델 및 데이터 초기화
# model = SentenceTransformer("sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens")
# data = load_and_preprocess_data()
# genre_list = extract_genres(data)
# author_list = extract_authors(data)
#
#
# def jac(list1, list2):
#     s1, s2 = set(list1), set(list2)
#     union_size = len(s1.union(s2))
#     return float(len(s1.intersection(s2)) / union_size) if union_size != 0 else 0.0
#
#
# # 자카드 기반 후보 도서군 생성
# def build_candidates(threshold=0.2):
#     n = len(genre_list)
#     jac_list = np.zeros((n, n))
#     for i in range(n):
#         for j in range(n):
#             jac_list[i][j] = jac(genre_list[i], genre_list[j])
#
#     candidates_dict = {
#         i: [j for j, sim in enumerate(jac_list[i]) if sim >= threshold and i != j]
#         for i in range(n)
#     }
#     return candidates_dict
#
#
# def cosine_sim(title):
#     idx = data[data['title'] == title].index[0]
#     input_desc = data.at[idx, 'description']
#     candidate_indices = build_candidates()[idx]
#     candidate_descs = data['description'].iloc[candidate_indices].tolist()
#
#     emb_input = model.encode([input_desc], normalize_embeddings=True)
#     emb_candidates = model.encode(candidate_descs, normalize_embeddings=True)
#     return cosine_similarity(emb_input, emb_candidates)[0]
#
#
# def genre_sim(title):
#     idx = data[data['title'] == title].index[0]
#     input_genres = genre_list[idx]
#     return np.array([jac(input_genres, genre_list[i]) for i in build_candidates()[idx]])
#
#
# def author_sim(title):
#     idx = data[data['title'] == title].index[0]
#     input_authors = author_list[idx]
#     return np.array([jac(input_authors, author_list[i]) for i in build_candidates()[idx]])
#
#
# def _to_py(obj):
#     if isinstance(obj, np.generic):
#         return obj.item()
#     if isinstance(obj, np.ndarray):
#         return obj.tolist()
#     if isinstance(obj, pd.Timestamp):
#         return obj.isoformat()
#     return obj
#
#
# def recommend_page_books(titles, user_name, total_k=20):
#     if not titles:
#         return []
#
#     # 빌린 책이 20 초과인 경우 랜덤으로 10권 뽑아서 titles 리스트로 반환
#     max_input = 20
#     if len(titles) > max_input:
#         titles = random.sample(titles, 10)
#
#     # 각 책당 추천할 개수 계산
#     num_books = len(titles)
#     per_book = total_k // num_books
#     remainder = total_k % num_books  # 나머지는 앞에서부터 하나씩 더 줌
#
#     all_recs = []
#     used_indices = set()  # 중복 제거용
#
#     for i, title in enumerate(titles):
#         try:
#             idx = data[data['title'] == title].index[0]
#         except IndexError:
#             continue
#
#         candidate_indices = build_candidates()[idx]
#
#         scores = (
#             0.5 * cosine_sim(title) +
#             0.3 * genre_sim(title) +
#             0.2 * author_sim(title)
#         )
#
#         ranked = sorted(zip(candidate_indices, scores), key=lambda x: x[1], reverse=True)
#
#         # 이 책이 가져갈 추천 개수
#         num_recs = per_book + (1 if i < remainder else 0)
#
#         count = 0
#         for j, _ in ranked:
#             if j not in used_indices:
#                 used_indices.add(j)
#                 all_recs.append(j)
#                 count += 1
#             if count >= num_recs:
#                 break
#
#     result = []
#     for idx in all_recs:
#         row = data.iloc[idx]
#
#         # id
#         try:
#             _id = int(row["id"])
#         except Exception:
#             _id = row["id"]
#
#         # school_id (NaN/None 대비)
#         _school_id = row.get("school_id")
#         try:
#             _school_id = int(_school_id)
#         except Exception:
#             _school_id = None
#
#         # 날짜는 문자열로
#         _book_date = row["publication_date"]
#         try:
#             _book_date = _book_date.isoformat()  # Timestamp면
#         except Exception:
#             _book_date = str(_book_date)  # 그 외는 문자열화
#
#         item = {
#             "id": _id,
#             "title": row["title"],
#             "writer": row["writer"],
#             "publisher": row["publisher"],
#             "description": row["description"],
#             "book_date": _book_date,
#             "img": row["img"],
#             "school_id": _school_id,  # 플래그 계산용
#         }
#         result.append(item)
#
#     if user_name:
#         school_id = get_user_school_id(user_name)
#         if school_id is not None:
#             try:
#                 school_id = int(school_id)
#             except Exception:
#                 school_id = None
#         if school_id is not None:
#             for item in result:
#                 item["is_school"] = (item.get("school_id") == school_id)
#         else:
#             for item in result:
#                 item["is_school"] = False
#
#     for item in result:
#         item.pop("school_id", None)
#
#     return result


#--------------------------
# 1차 수정

# import numpy as np
# import pandas as pd
# import random
# from sentence_transformers import SentenceTransformer
# from .data_loader import load_and_preprocess_data, extract_genres, extract_authors, get_user_school_id
# import heapq
# from functools import lru_cache
#
# # 모델 및 데이터 초기화
# # paraphrase-multilingual-MiniLM-L12-v2
# model = SentenceTransformer("sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens")
# data = load_and_preprocess_data()
# genre_list = extract_genres(data)
# author_list = extract_authors(data)
#
# # 전 책 설명 임베딩을 "한 번만" 미리 계산
# EMB = model.encode(
#     data["description"].tolist(),
#     normalize_embeddings=True
# )
#
#
# # 자카드 기반 후보 도서군 생성
# # 후보 사전도 "한 번만" 만들고 재사용
# def build_candidates(threshold=0.2):
#     # (기존 O(N^2) 그대로여도) 서버 기동 시 1회만 수행되게끔 유지
#     n = len(genre_list)
#     jac_list = np.zeros((n, n))
#     for i in range(n):
#         gi = set(genre_list[i])
#         for j in range(n):
#             if i == j:
#                 continue
#             gj = set(genre_list[j])
#             u = len(gi | gj)
#             jac_list[i, j] = (len(gi & gj) / u) if u else 0.0
#     return {i: [j for j, sim in enumerate(jac_list[i]) if sim >= threshold] for i in range(n)}
#
# CANDIDATES = build_candidates()
#
#
# def cosine_sim(title):
#     idx = data[data['title'] == title].index[0]
#     cand = CANDIDATES[idx]
#     if not cand:
#         return np.array([])
#
#     # 새로 인코딩하지 말고, 미리 만든 EMB로 바로 코사인(dotp) 계산
#     # normalize_embeddings=True였으니 dot == cosine
#     v = EMB[idx]                   # (d,)
#     M = EMB[cand]                  # (k, d)
#     return M @ v                   # (k,)
#
#
# def genre_sim(title):
#     idx = data[data['title'] == title].index[0]
#     cand = CANDIDATES[idx]
#     if not cand:
#         return np.array([])
#
#     s1 = set(genre_list[idx])
#     out = []
#     for j in cand:
#         s2 = set(genre_list[j])
#         u = len(s1 | s2)
#         out.append((len(s1 & s2) / u) if u else 0.0)
#     return np.array(out)
#
#
# def author_sim(title):
#     idx = data[data['title'] == title].index[0]
#     cand = CANDIDATES[idx]
#     if not cand:
#         return np.array([])
#
#     s1 = set(author_list[idx])
#     out = []
#     for j in cand:
#         s2 = set(author_list[j])
#         u = len(s1 | s2)
#         out.append((len(s1 & s2) / u) if u else 0.0)
#     return np.array(out)
#
#
# @lru_cache(maxsize=4096)
# def _cosine_sim_by_title(title: str):
#     return tuple(cosine_sim(title))  # numpy array는 hash 불가 → tuple로
#
# @lru_cache(maxsize=4096)
# def _genre_sim_by_title(title: str):
#     return tuple(genre_sim(title))
#
# @lru_cache(maxsize=4096)
# def _author_sim_by_title(title: str):
#     return tuple(author_sim(title))
#
#
# def _to_py(obj):
#     if isinstance(obj, np.generic):
#         return obj.item()
#     if isinstance(obj, np.ndarray):
#         return obj.tolist()
#     if isinstance(obj, pd.Timestamp):
#         return obj.isoformat()
#     return obj
#
#
# def recommend_page_books(titles, user_name, total_k=20):
#     if not titles:
#         return []
#
#     # 빌린 책이 20 초과인 경우 랜덤으로 10권 뽑아서 titles 리스트로 반환
#     max_input = 20
#     if len(titles) > max_input:
#         titles = random.sample(titles, 10)
#
#     # 각 책당 추천할 개수 계산
#     num_books = len(titles)
#     per_book = total_k // num_books
#     remainder = total_k % num_books  # 나머지는 앞에서부터 하나씩 더 줌
#
#     all_recs = []
#     used_indices = set()  # 중복 제거용
#
#     for i, title in enumerate(titles):
#         try:
#             idx = data[data['title'] == title].index[0]
#         except IndexError:
#             continue
#
#
#         scores = (
#                 0.5 * np.array(_cosine_sim_by_title(title)) +
#                 0.3 * np.array(_genre_sim_by_title(title)) +
#                 0.2 * np.array(_author_sim_by_title(title))
#         )
#
#         #ranked = sorted(zip(candidate_indices, scores), key=lambda x: x[1], reverse=True)
#         ranked = heapq.nlargest(
#             per_book + 1,  # 넉넉히 약간 더 뽑아도 OK
#             zip(CANDIDATES[idx], scores),
#             key=lambda x: x[1]
#         )
#
#         # 이 책이 가져갈 추천 개수
#         num_recs = per_book + (1 if i < remainder else 0)
#
#         count = 0
#         for j, _ in ranked:
#             if j not in used_indices:
#                 used_indices.add(j)
#                 all_recs.append(j)
#                 count += 1
#             if count >= num_recs:
#                 break
#
#     result = []
#     for idx in all_recs:
#         row = data.iloc[idx]
#
#         # id
#         try:
#             _id = int(row["id"])
#         except Exception:
#             _id = row["id"]
#
#         # school_id (NaN/None 대비)
#         _school_id = row.get("school_id")
#         try:
#             _school_id = int(_school_id)
#         except Exception:
#             _school_id = None
#
#         # 날짜는 문자열로
#         _book_date = row["publication_date"]
#         try:
#             _book_date = _book_date.isoformat()  # Timestamp면
#         except Exception:
#             _book_date = str(_book_date)  # 그 외는 문자열화
#
#         item = {
#             "id": _id,
#             "title": row["title"],
#             "writer": row["writer"],
#             "publisher": row["publisher"],
#             "description": row["description"],
#             "book_date": _book_date,
#             "img": row["img"],
#             "school_id": _school_id,  # 플래그 계산용
#         }
#         result.append(item)
#
#     if user_name:
#         school_id = get_user_school_id(user_name)
#         if school_id is not None:
#             try:
#                 school_id = int(school_id)
#             except Exception:
#                 school_id = None
#         if school_id is not None:
#             for item in result:
#                 item["is_school"] = (item.get("school_id") == school_id)
#         else:
#             for item in result:
#                 item["is_school"] = False
#
#     for item in result:
#         item.pop("school_id", None)
#
#     return result


#-------------------
# 2차 수정

# import os
# import threading
# import random
# import numpy as np
# import pandas as pd
# import heapq
# from collections import defaultdict
# from sentence_transformers import SentenceTransformer
#
# from .data_loader import (
#     load_and_preprocess_data,
#     extract_genres,
#     extract_authors,
#     get_user_school_id,
# )
#
# # -------- 전역 캐시/상태 --------
# _model = None
# _data = None
# _genre_list = None
# _author_list = None
# _EMB = None
# _GENRE_INV = None     # 장르 토큰 -> 인덱스 집합
# _READY = False        # 풀모드(코사인) 준비 완료 플래그
#
# EMB_PATH = "embeddings.npy"  # 임베딩 캐시 파일 경로
#
#
# def _build_genre_inv():
#     """장르 역인덱스(빠른 후보 생성)"""
#     inv = defaultdict(set)
#     for i, toks in enumerate(_genre_list):
#         for t in toks:
#             inv[t].add(i)
#     return inv
#
#
# def _warmup():
#     """무거운 초기화: 백그라운드 1회 실행 (모델 로드 + 임베딩 준비 + 역인덱스 보강)"""
#     global _model, _EMB, _GENRE_INV, _READY
#     try:
#         if _model is None:
#             # 가벼운 다국어 모델 권장 (속도↑, 품질 적절)
#             #_model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
#             _model = SentenceTransformer("sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens")
#         # 임베딩: 파일이 있으면 mmap 즉시 오픈, 없으면 계산 후 저장
#         if os.path.exists(EMB_PATH):
#             _EMB = np.load(EMB_PATH, mmap_mode="r")
#         else:
#             descs = _data["description"].tolist()
#             _EMB = _model.encode(
#                 descs,
#                 normalize_embeddings=True,
#                 batch_size=128,
#                 show_progress_bar=False,
#             )
#             np.save(EMB_PATH, _EMB)
#
#         # 역인덱스(이미 기본 생성되어 있지만 재확인)
#         if _GENRE_INV is None:
#             _GENRE_INV = _build_genre_inv()
#
#         _READY = True
#     except Exception:
#         _READY = False
#         raise
#
#
# def init_if_needed():
#     """가벼운 부분은 동기 초기화, 무거운 건 백그라운드 워밍업"""
#     global _data, _genre_list, _author_list, _GENRE_INV
#     if _data is None:
#         _data = load_and_preprocess_data()               # DB -> DataFrame
#         _genre_list = extract_genres(_data)              # 장르 토큰 리스트
#         _author_list = extract_authors(_data)            # 작가 토큰 리스트
#         _GENRE_INV = _build_genre_inv()                  # O(N)
#     if not _READY:
#         threading.Thread(target=_warmup, daemon=True).start()
#
#
# def _candidates_for(idx: int):
#     """장르 역인덱스 합집합으로 후보 생성 (O(∑토큰))"""
#     cand = set()
#     for t in _genre_list[idx]:
#         cand |= _GENRE_INV.get(t, set())
#     cand.discard(idx)
#     return list(cand)
#
#
# def _cosine_scores(idx, cand):
#     if not _READY or _EMB is None:
#         return np.zeros(len(cand), dtype=float)
#     v = _EMB[idx]     # (d,)
#     M = _EMB[cand]    # (k, d)
#     return M @ v      # normalize=True → dot == cosine
#
#
# def _genre_scores(idx, cand):
#     s1 = set(_genre_list[idx])
#     out = []
#     for j in cand:
#         s2 = set(_genre_list[j])
#         u = len(s1 | s2)
#         out.append((len(s1 & s2) / u) if u else 0.0)
#     return np.array(out)
#
#
# def _author_scores(idx, cand):
#     s1 = set(_author_list[idx])
#     out = []
#     for j in cand:
#         s2 = set(_author_list[j])
#         u = len(s1 | s2)
#         out.append((len(s1 & s2) / u) if u else 0.0)
#     return np.array(out)
#
#
# def _to_py(o):
#     if isinstance(o, np.generic):
#         return o.item()
#     if isinstance(o, np.ndarray):
#         return o.tolist()
#     if isinstance(o, pd.Timestamp):
#         return o.isoformat()
#     return o
#
#
# def recommend_page_books(titles, user_name, total_k=20):
#     """
#     - 서버 즉시 응답: init_if_needed()로 라이트모드(장르/작가) 즉시 사용
#     - 백그라운드 워밍업 완료되면 코사인까지 포함(품질↑)
#     """
#     init_if_needed()
#
#     if not titles:
#         return []
#
#     max_input = 20
#     if len(titles) > max_input:
#         titles = random.sample(titles, 10)
#
#     num_books = len(titles)
#     per_book = max(1, total_k // num_books)
#     remainder = total_k % num_books
#
#     used = set()
#     picked = []
#
#     for i, title in enumerate(titles):
#         try:
#             idx = _data[_data["title"] == title].index[0]
#         except IndexError:
#             continue
#
#         cand = _candidates_for(idx)
#         if not cand:
#             continue
#
#         cos = _cosine_scores(idx, cand)
#         gen = _genre_scores(idx, cand)
#         aut = _author_scores(idx, cand)
#
#         m = min(len(cos), len(gen), len(aut))
#         if m == 0:
#             continue
#
#         scores = 0.5 * cos[:m] + 0.3 * gen[:m] + 0.2 * aut[:m]
#         take = per_book + (1 if i < remainder else 0)
#
#         ranked = heapq.nlargest(take * 2, zip(cand[:m], scores), key=lambda x: x[1])  # 여유
#         c = 0
#         for j, _ in ranked:
#             if j not in used:
#                 used.add(j)
#                 picked.append(j)
#                 c += 1
#                 if c >= take:
#                     break
#
#     # 결과 생성 (직렬화 안전 캐스팅)
#     result = []
#     for ridx in picked:
#         row = _data.iloc[ridx]
#
#         try:
#             _id = int(row["id"])
#         except Exception:
#             _id = row["id"]
#
#         _book_date = row["publication_date"]
#         try:
#             _book_date = _book_date.isoformat()
#         except Exception:
#             _book_date = str(_book_date)
#
#         item = {
#             "id": _id,
#             "title": row["title"],
#             "writer": row["writer"],
#             "publisher": row["publisher"],
#             "description": row["description"],
#             "book_date": _book_date,
#             "img": row["img"],
#         }
#         result.append(item)
#
#     # is_school 플래그
#     if user_name:
#         school_id = get_user_school_id(user_name)
#         try:
#             school_id = int(school_id) if school_id is not None else None
#         except Exception:
#             school_id = None
#
#         if school_id is not None and "school_id" in _data.columns:
#             sid_series = pd.to_numeric(_data["school_id"], errors="coerce").astype("Int64")
#             for item in result:
#                 ridx = _data.index[_data["title"] == item["title"]][0]
#                 row_sid = sid_series.iloc[ridx]
#                 item["is_school"] = (int(row_sid) == school_id) if pd.notna(row_sid) else False
#         else:
#             for item in result:
#                 item["is_school"] = False
#
#     return result


#3차 수정

# Reco_System/recommendation_engine.py
# ------------------------------------------------------------
# - description 컬럼만 임베딩
# - 캐시 파일: 레포 루트의 book_embeddings_rds.npy
# - 캐시가 있으면 np.load(mmap_mode="r")로 즉시 로드
# - 없으면 encode → np.save 로 저장 후 사용
# - (안전) 캐시 행수 != 데이터 행수면 다시 계산해 저장
# - 기존 구조/함수 시그니처 유지, os만 사용(pathlib X)
# ------------------------------------------------------------

import os
import threading
import random
import numpy as np
import pandas as pd
import heapq
from collections import defaultdict
from sentence_transformers import SentenceTransformer

from .data_loader import (
    load_and_preprocess_data,
    extract_genres,
    extract_authors,
    get_user_school_id,
)

# -------- 전역 캐시/상태 --------
_model = None
_data = None
_genre_list = None
_author_list = None
_EMB = None                # description 임베딩 (numpy array / memmap)
_GENRE_INV = None          # 장르 토큰 -> 인덱스 집합
_READY = False             # 풀모드(코사인) 준비 완료 플래그

# 레포 루트 절대경로: .../Bookshelf-AI
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMBEDDING_PATH = os.path.join(BASE_DIR, "embeddings.npy")  # 캐시 경로 고정

# ---------------- 내부 유틸 ----------------
def _build_genre_inv():
    inv = defaultdict(set)
    for i, toks in enumerate(_genre_list):
        for t in toks:
            inv[t].add(i)
    return inv

def _ensure_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens")

def _ensure_embeddings():
    """
    description 임베딩을 캐시에서 불러오거나, 없으면 생성 후 저장.
    캐시 행수와 데이터 행수가 다르면 다시 계산해 저장.
    """
    global _EMB
    _ensure_model()

    # 캐시가 존재하면 우선 로드
    if os.path.exists(EMBEDDING_PATH):
        _EMB = np.load(EMBEDDING_PATH, mmap_mode="r")
        # 데이터 행수와 맞지 않으면 재계산
        if _EMB.shape[0] != len(_data):
            descs = _data["description"].fillna("").astype(str).tolist()
            _EMB = _model.encode(
                descs,
                normalize_embeddings=True,
                batch_size=128,
                show_progress_bar=True,
                convert_to_numpy=True,
            ).astype("float32")
            np.save(EMBEDDING_PATH, _EMB)
    else:
        # 캐시가 없으면 새로 계산 후 저장
        descs = _data["description"].fillna("").astype(str).tolist()
        _EMB = _model.encode(
            descs,
            normalize_embeddings=True,
            batch_size=128,
            show_progress_bar=True,
            convert_to_numpy=True,
        ).astype("float32")
        np.save(EMBEDDING_PATH, _EMB)

    # 최종적으로 mmap으로 다시 열어도 좋지만, 이미 메모리에 있으면 그대로 써도 됨
    # _EMB = np.load(EMBEDDING_PATH, mmap_mode="r")

def _warmup():
    """무거운 초기화: (모델 로드 + 임베딩 준비 + 역인덱스 보강)"""
    global _GENRE_INV, _READY
    try:
        _ensure_embeddings()
        if _GENRE_INV is None:
            _GENRE_INV = _build_genre_inv()
        _READY = True
    except Exception:
        _READY = False
        raise

def init_if_needed():
    """가벼운 부분은 동기 초기화, 무거운 건 백그라운드 워밍업"""
    global _data, _genre_list, _author_list, _GENRE_INV
    if _data is None:
        _data = load_and_preprocess_data()          # DB -> DataFrame
        _data = _data.reset_index(drop=True)        # 0..N-1 보장(라벨/위치 혼동 방지)
        _genre_list = extract_genres(_data)         # 장르 토큰 리스트
        _author_list = extract_authors(_data)       # 작가 토큰 리스트
        _GENRE_INV = _build_genre_inv()             # O(N)
    if not _READY:
        # threading.Thread(target=_warmup, daemon=True).start()
        _warmup()

# ---------------- 스코어링 ----------------
def _candidates_for(idx: int):
    """장르 역인덱스 합집합으로 후보 생성"""
    cand = set()
    for t in _genre_list[idx]:
        cand |= _GENRE_INV.get(t, set())
    cand.discard(idx)
    return list(cand)

def _cosine_scores(idx, cand):
    if not _READY or _EMB is None:
        return np.zeros(len(cand), dtype=float)
    v = _EMB[idx]       # (d,)
    M = _EMB[cand]      # (k, d)
    return M @ v        # normalize=True → dot == cosine

def _genre_scores(idx, cand):
    s1 = set(_genre_list[idx])
    out = []
    for j in cand:
        s2 = set(_genre_list[j])
        u = len(s1 | s2)
        out.append((len(s1 & s2) / u) if u else 0.0)
    return np.array(out)

def _author_scores(idx, cand):
    s1 = set(_author_list[idx])
    out = []
    for j in cand:
        s2 = set(_author_list[j])
        u = len(s1 | s2)
        out.append((len(s1 & s2) / u) if u else 0.0)
    return np.array(out)

def _to_py(o):
    if isinstance(o, np.generic):
        return o.item()
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, pd.Timestamp):
        return o.isoformat()
    return o

# ---------------- 외부 API ----------------
def recommend_page_books(titles, user_name, total_k=20):
    """
    - init_if_needed()로 라이트모드(장르/작가) 즉시 사용
    - 백그라운드 워밍업 완료되면 코사인 포함(품질↑)
    - description 임베딩 캐시는 book_embeddings_rds.npy 하나만 사용
    """
    init_if_needed()

    if not titles:
        return []

    max_input = 20
    if len(titles) > max_input:
        titles = random.sample(titles, 10)

    num_books = len(titles)
    per_book = max(1, total_k // num_books)
    remainder = total_k % num_books

    used = set()
    for title in titles:
        pos = np.where(_data["title"].values == title)[0]
        if len(pos):
            used.add(int(pos[0]))

    picked = []

    for i, title in enumerate(titles):
        # 위치 인덱스 사용(라벨 혼동 방지)
        pos = np.where(_data["title"].values == title)[0]
        if len(pos) == 0:
            continue
        idx = int(pos[0])

        cand = _candidates_for(idx)
        if not cand:
            continue

        cos = _cosine_scores(idx, cand)
        gen = _genre_scores(idx, cand)
        aut = _author_scores(idx, cand)

        m = min(len(cos), len(gen), len(aut))
        if m == 0:
            continue

        scores = 0.5 * cos[:m] + 0.3 * gen[:m] + 0.2 * aut[:m]
        take = per_book + (1 if i < remainder else 0)

        ranked = heapq.nlargest(take * 2, zip(cand[:m], scores), key=lambda x: x[1])
        c = 0
        for j, _ in ranked:
            if j not in used:
                used.add(j)
                picked.append(j)
                c += 1
                if c >= take:
                    break

    result = []
    for ridx in picked:
        row = _data.iloc[ridx]

        try:
            _id = int(row["id"])
        except Exception:
            _id = row["id"]

        _book_date = row.get("publication_date")
        try:
            _book_date = _book_date.isoformat()
        except Exception:
            _book_date = str(_book_date)

        item = {
            "id": _id,
            "title": row["title"],
            "writer": row["writer"],
            "publisher": row["publisher"],
            "description": row["description"],
            "book_date": _book_date,
            "img": row["img"],
        }
        result.append(item)

    # is_school 플래그
    if user_name:
        school_id = get_user_school_id(user_name)
        try:
            school_id = int(school_id) if school_id is not None else None
        except Exception:
            school_id = None

        if school_id is not None and "school_id" in _data.columns:
            sid_series = pd.to_numeric(_data["school_id"], errors="coerce").astype("Int64")
            for item in result:
                pos = np.where(_data["title"].values == item["title"])[0]
                if len(pos):
                    ridx = int(pos[0])
                    row_sid = sid_series.iloc[ridx]
                    item["is_school"] = (int(row_sid) == school_id) if pd.notna(row_sid) else False
                else:
                    item["is_school"] = False
        else:
            for item in result:
                item["is_school"] = False

    return result
