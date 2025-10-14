# from fastapi import HTTPException

# from fastapi import FastAPI, Query
# from pydantic import BaseModel

# #1. 로그인 2. 회원가입 3. 글 CRUD 4. 댓글 CRUD 5. 좋아요 6. pagecount
# #클래스 종류: 유저, 글 ,댓글

# app = FastAPI()	

# class Item(BaseModel):
# 	name : str
# 	description : str
# 	price : float
# 	tax : float | None = None

# class User(BaseModel):
# 	name : str
# 	id : str
# 	password : str

# class Post(BaseModel):
# 	post_id : int
# 	title : str
# 	content : str
# 	image_url : str
# 	like_count : int
# 	read_count : int

# class Comment(BaseModel):
# 	content : int
# 	user_id : str
# 	post_id : str

# @app.get("/")
# async def root():
# 	return {"message": "Hello World"}

# #API Method 4개 : GET(URL), POST(Header), PUT, DELETE

# @app.post("/login")
# async def login(id: User = Query(), password: str = Query()):
# 	if User.id() == id and password == User.password():
# 		return {"massage": "로그인 성공"}
# 	return HTTPException(status_code=401, detail="로그인 실패")


# @app.post("/signup")
# async def signup(user: User):
# 	User.create(**user.dict())
# 	return {"message": "회원가입 성공"}

# #메인화면
# @app.get("/board")
# async def all_get_board():
# 	return Post

# #상세 글보기
# @app.get("/board/{Post_id}")
# async def get_board(post_id: int):
# 	return {"post_id": Post.objects.get(id=post_id).id}

# #글생성
# @app.post("/board")
# async def post_board(post: Post):
# 	Post.objects.create(**post.dict())
# 	return {"message": post.post_id}

# #글 업데이트
# @app.patch("/board/{post_id}")
# async def patch_board(post_id: int, post: Post):
# 	last_post = Post.objects.get(id=post_id)
# 	post_title  = post.title.replace()
# 	post.content = post.content.replace()
# 	post.image_url = post.image_url.replace()
# 	return last_post

# #글 삭제
# @app.delete("/board/{post_id}")
# async def delete_board(post_id: int):
# 	Post.delete_by_id(post_id)
# 	return {"message": "삭제 완료"}

# #댓글 생성
# @app.post("/comment")
# async def post_commment():
# 	Post.objects.create(**Comment.dict())
# 	return {"message": Comment.post_id}

# #댓글 읽기
# @app.get("/comment/{id}")
# async def post_commment():

# #댓글 업데이트
# @app.patch("/comment/{id}")
# async def post_commment():

# # #댓글 삭제
# @app.delete("/comment/{id}")
# async def post_commment():

# #좋아요
# @app.post("/recommend")
# async def post_recommend(post_id: int):
# 	post = Post.get_by_id(post_id)
# 	post.like_count = post.like_count + 1
# 	return post

# #조회수
# @app.post("/readboard")
# async def read_board(post_id: int):
# 	post = Post.get_by_id(post_id)
# 	post.read_count = post.read_count + 1
# 	return post
#---------------------------------------------------------------
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel

# app = FastAPI()

# # 모델 정의
# class User(BaseModel):
#     name: str
#     id: str
#     password: str

# class Post(BaseModel):
#     post_id: str
#     title: str
#     content: str
#     image_url: str
#     like_count: int
#     read_count: int

# class Comment(BaseModel):
#     content: str
#     user_id: str
#     post_id: str


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

# @app.post("/login")
# async def login(user: User):
#     # 여기서는 단순히 구조만 보여주면 됨
#     return {"message": f"로그인 시도: {user.id}"}

# @app.post("/signup")
# async def signup(user: User):
#     return {"message": f"회원가입: {user.id}"}

# @app.get("/board")
# async def all_get_board():
#     return [{"post_id": "1", "title": "테스트", "content": "내용", 
#              "image_url": "url", "like_count": 0, "read_count": 0}]

# @app.get("/board/{post_id}")
# async def get_board(post_id: int):
#     return {"post_id": post_id, "title": "상세글"}

# @app.post("/board")
# async def post_board(post: Post):
#     return {"message": f"글 생성: {post.post_id}"}

# @app.patch("/board/{post_id}")
# async def patch_board(post_id: int, post: Post):
#     return {"message": f"글 {post_id} 수정됨"}

# @app.delete("/board/{post_id}")
# async def delete_board(post_id: int):
#     return {"message": f"글 {post_id} 삭제됨"}

# @app.post("/recommend")
# async def post_recommend(post_id: int):
#     return {"message": f"글 {post_id} 좋아요 +1"}

# @app.post("/readboard")
# async def read_board(post_id: int):
#     return {"message": f"글 {post_id} 조회수 +1"}
#------------------------------------------------------------------
# from fastapi import FastAPI
# from pydantic import BaseModel
# from typing import List

# app = FastAPI()

# # 책 데이터 구조 정의
# class Book(BaseModel):
#     title: str
#     author: str
#     description: str
#     image_url: str

# # 추천 책 리스트 (샘플 데이터)
# recommended_books = [
#     Book(
#         title="데미안",
#         author="헤르만 헤세",
#         description="자아를 찾아가는 소년의 성장 이야기. 고전이지만 청소년뿐만 아니라 모든 세대가 읽을 수 있는 책.",
#         image_url="https://image.aladin.co.kr/product/17/14/cover500/8970122199_1.jpg"
#     ),
#     Book(
#         title="어린 왕자",
#         author="앙투안 드 생텍쥐페리",
#         description="순수한 시선으로 바라본 세상과 사랑의 의미. 짧지만 여운이 오래 남는 이야기.",
#         image_url="https://image.aladin.co.kr/product/3/82/cover500/8983921559_1.jpg"
#     ),
#     Book(
#         title="1984",
#         author="조지 오웰",
#         description="전체주의와 감시 사회에 대한 날카로운 비판. 현대 사회를 성찰하게 만드는 명작.",
#         image_url="https://image.aladin.co.kr/product/2/60/cover500/8982814474_1.jpg"
#     ),
#     Book(
#         title="종의 기원",
#         author="찰스 다윈",
#         description="진화론의 기초가 된 고전. 과학적 사고와 비판적 시각을 기르는 데 도움을 줌.",
#         image_url="https://image.aladin.co.kr/product/11/87/cover500/8935652339_1.jpg"
#     ),
#     Book(
#         title="죽음의 수용소에서",
#         author="빅터 프랭클",
#         description="아우슈비츠 생존자의 시선으로 본 삶의 의미. 극한 상황 속에서도 인간이 희망을 붙드는 힘을 보여줌.",
#         image_url="https://image.aladin.co.kr/product/22/63/cover500/8937834799_1.jpg"
#     )
# ]

# # 추천 API 엔드포인트
# @app.get("/recommend", response_model=List[Book])
# def get_recommendations():
#     return recommended_books
#------------------------------------------------------------------
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

model = SentenceTransformer("all-MiniLM-L6-v2")
data = pd.read_csv("tmdb_5000_movies.csv")
data['overview'] = data['overview'].fillna('')

genre_list = []
replace_list = ['[','{','"',':',']','}',',','1','2','3','4','5','6','7','8','9','0']

for g_raw in data['genres']:
    g = g_raw
    for r in replace_list:
        g = g.replace(r, '')
    genre_list.append(g)

re_ge = []
for g in genre_list:
    items = [item for item in g.replace('name','').replace('id','').split(' ') if item]
    re_ge.append(items)

def jac(list1, list2):
    s1, s2 = set(list1), set(list2)
    union_size = len(s1.union(s2))
    if union_size == 0:
        return 0.0
    return len(s1.intersection(s2)) / union_size

jac_list = []
for i in range(len(re_ge)):
    row = [jac(re_ge[i], re_ge[j]) for j in range(len(re_ge))]
    jac_list.append(row)

jac_list = np.array(jac_list)

threshold = 0.2
candidates_dict = {}
for i in range(len(jac_list)):
    candidates = [j for j, sim in enumerate(jac_list[i]) if sim >= threshold and j != i]
    candidates_dict[i] = candidates

def Cosine(title):
    doc_input = data[data['title'] == title]['overview'].iloc[0]
    idx = data[data['title'] == title].index[0]

    valid_indices = [i for i in candidates_dict[idx] if i in data.index]
    doc_candidates = data['overview'].loc[valid_indices].tolist()

    emb_input = model.encode([doc_input])
    emb_candidates = model.encode(doc_candidates)

    similarities = cosine_similarity(emb_input, emb_candidates)[0]
    return similarities

def main_jac(title):
    idx = data[data['title'] == title].index[0]
    candidates = candidates_dict[idx]
    movie_gen = re_ge[idx]
    return np.array([jac(movie_gen, re_ge[i]) for i in candidates])

replace_list2 = ['[','{','"',':',']','}','1','2','3','4','5','6','7','8','9','0']

filtered_co = []
for raw in data['production_companies']:
    c = raw
    for r in replace_list2:
        c = c.replace(r,'')
    items = [item.strip() for item in c.replace('name','').replace('id','').split(',') if item.strip()]
    filtered_co.append(items)

def comapnies_jac(title):
    idx = data[data['title'] == title].index[0]
    movie_co = filtered_co[idx]

    can_co = [filtered_co[i] for i in candidates_dict[idx]]
    return np.array([jac(movie_co, c) for c in can_co])

def recommendation(title):
    Final_Score = 0.6 * Cosine(title) + 0.3 * main_jac(title) + 0.1 * comapnies_jac(title)
    idx_scores = list(zip(candidates_dict[data[data['title']==title].index[0]], Final_Score))
    idx_scores = sorted(idx_scores, key=lambda x: x[1], reverse=True)
    top_idx = idx_scores[:20]

    rec_movies = [data['title'][i[0]] for i in top_idx]
    return rec_movies

app = FastAPI()


class MovieInfo(BaseModel):
    title: str
def recommend_movies(movie: MovieInfo) -> List[dict]:
    """
    movie.title 기준으로 추천 영화 리스트 반환
    """
    rec_list = recommendation(movie.title)
    return [{"title": t} for t in rec_list]
@app.post("/recommend_movies")
async def get_recommendations(movie: MovieInfo):
    results = recommend_movies(movie)
    return {"input_movie": movie, "recommendations": results}
