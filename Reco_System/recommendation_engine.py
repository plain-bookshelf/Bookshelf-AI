import numpy as np
import pandas as pd
import random
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from .data_loader import load_and_preprocess_data, extract_genres, extract_authors, get_user_school_id


# 모델 및 데이터 초기화
model = SentenceTransformer("sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens")
data = load_and_preprocess_data()
genre_list = extract_genres(data)
author_list = extract_authors(data)


def jac(list1, list2):
    s1, s2 = set(list1), set(list2)
    union_size = len(s1.union(s2))
    return float(len(s1.intersection(s2)) / union_size) if union_size != 0 else 0.0


# 자카드 기반 후보 도서군 생성
def build_candidates(threshold=0.2):
    n = len(genre_list)
    jac_list = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            jac_list[i][j] = jac(genre_list[i], genre_list[j])

    candidates_dict = {
        i: [j for j, sim in enumerate(jac_list[i]) if sim >= threshold and i != j]
        for i in range(n)
    }
    return candidates_dict


candidates_dict = build_candidates()


def cosine_sim(title):
    idx = data[data['title'] == title].index[0]
    input_desc = data.at[idx, 'description']
    candidate_indices = candidates_dict[idx]
    candidate_descs = data['description'].iloc[candidate_indices].tolist()

    emb_input = model.encode([input_desc], normalize_embeddings=True)
    emb_candidates = model.encode(candidate_descs, normalize_embeddings=True)
    return cosine_similarity(emb_input, emb_candidates)[0]


def genre_sim(title):
    idx = data[data['title'] == title].index[0]
    input_genres = genre_list[idx]
    return np.array([jac(input_genres, genre_list[i]) for i in candidates_dict[idx]])


def author_sim(title):
    idx = data[data['title'] == title].index[0]
    input_authors = author_list[idx]
    return np.array([jac(input_authors, author_list[i]) for i in candidates_dict[idx]])


def _to_py(obj):
    if isinstance(obj, np.generic):
        return obj.item()
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, pd.Timestamp):
        return obj.isoformat()
    return obj


def recommend_page_books(titles, user_name, total_k=20):
    if not titles:
        return []

    # 빌린 책이 20 초과인 경우 랜덤으로 10권 뽑아서 titles 리스트로 반환
    max_input = 20
    if len(titles) > max_input:
        titles = random.sample(titles, 10)

    # 각 책당 추천할 개수 계산
    num_books = len(titles)
    per_book = total_k // num_books
    remainder = total_k % num_books  # 나머지는 앞에서부터 하나씩 더 줌

    all_recs = []
    used_indices = set()  # 중복 제거용

    for i, title in enumerate(titles):
        try:
            idx = data[data['title'] == title].index[0]
        except IndexError:
            continue

        candidate_indices = candidates_dict[idx]

        scores = (
            0.5 * cosine_sim(title) +
            0.3 * genre_sim(title) +
            0.2 * author_sim(title)
        )

        ranked = sorted(zip(candidate_indices, scores), key=lambda x: x[1], reverse=True)

        # 이 책이 가져갈 추천 개수
        num_recs = per_book + (1 if i < remainder else 0)

        count = 0
        for j, _ in ranked:
            if j not in used_indices:
                used_indices.add(j)
                all_recs.append(j)
                count += 1
            if count >= num_recs:
                break

    result = []
    for idx in all_recs:
        row = data.iloc[idx]

        # id
        try:
            _id = int(row["id"])
        except Exception:
            _id = row["id"]

        # school_id (NaN/None 대비)
        _school_id = row.get("school_id")
        try:
            _school_id = int(_school_id)
        except Exception:
            _school_id = None

        # 날짜는 문자열로
        _book_date = row["publication_date"]
        try:
            _book_date = _book_date.isoformat()  # Timestamp면
        except Exception:
            _book_date = str(_book_date)  # 그 외는 문자열화

        item = {
            "id": _id,
            "title": row["title"],
            "writer": row["writer"],
            "publisher": row["publisher"],
            "description": row["description"],
            "book_date": _book_date,
            "img": row["img"],
            "school_id": _school_id,  # 플래그 계산용
        }
        result.append(item)

    if user_name:
        school_id = get_user_school_id(user_name)
        if school_id is not None:
            try:
                school_id = int(school_id)
            except Exception:
                school_id = None
        if school_id is not None:
            for item in result:
                item["is_school"] = (item.get("school_id") == school_id)
        else:
            for item in result:
                item["is_school"] = False

    for item in result:
        item.pop("school_id", None)

    return result