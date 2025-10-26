import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from data_loader import load_and_preprocess_data, extract_genres, extract_authors

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
def build_candidates(threshold=0.5):
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


def recommend_books(title, top_k=20):
    idx = data[data['title'] == title].index[0]
    candidate_indices = candidates_dict[idx]

    if not candidate_indices:
        return []

    scores = (
            0.5 * cosine_sim(title) +
            0.3 * genre_sim(title) +
            0.2 * author_sim(title)
    )
    ranked = sorted(zip(candidate_indices, scores), key=lambda x: x[1], reverse=True)[:top_k]
    return [{"title": data.iloc[i]['title']} for i, _ in ranked]
