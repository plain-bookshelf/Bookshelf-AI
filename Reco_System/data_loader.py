import os
import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL 연결 설정
db_user = os.getenv("DB_USER")
db_password = quote_plus(os.getenv("DB_PASSWORD"))
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

engine = create_engine(
    f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}",
    echo=False
)

# DB에서 book + book_detail + affiliation JOIN (+책 학교 소속)
def load_and_preprocess_data():
    with engine.connect() as conn:
        query = text("""
            SELECT
                b.id,
                b.book_name AS title,
                b.book_author AS writer,
                b.publisher,
                b.publication_date,
                b.book_introduction AS description,
                b.book_type AS catgory,
                b.book_image AS img,
                bd.registration_number AS id_number,
                bd.call_number AS call_num,
                a.id AS school_id,
                a.affiliation_name AS school
            FROM book b
            LEFT JOIN book_detail bd ON bd.book = b.id
            LEFT JOIN affiliation a ON bd.affiliation = a.id
        """)
        data = pd.read_sql(query, conn)

    # 결측값 처리
    for col in ["title", "writer", "publisher", "publication_date", "description",
                "catgory", "img", "school", "id_number", "call_num"]:
        data[col] = data[col].fillna('')

    # 책 소개에서 특수문자 제거
    data['description'] = data['description'].str.replace('[^가-힣a-zA-Z0-9 .,!?]', '', regex=True)

    # 이미지 기준 중복 제거
    data = data.drop_duplicates(subset=['img']).reset_index(drop=True)

    return data


def get_user_school_id(user_name: str) -> int | None:
    with engine.connect() as conn:
        row = conn.execute(text("""
            SELECT a.id AS user_school_id
            FROM member m
            LEFT JOIN affiliation a ON m.affiliation = a.id
            WHERE m.user_name = :user_name
            LIMIT 1
        """), {"user_name": user_name}).mappings().first()
    return row["user_school_id"] if row else None


# 대여한 책 제목
def load_rented_book_titles(user_name):
    with engine.connect() as conn:
        query = text("""
            SELECT DISTINCT 
                b.book_name AS title
            FROM book_rental_record br
            JOIN book_detail bd ON br.book_detail = bd.id
            JOIN book b ON bd.book = b.id
            JOIN member m ON br.member = m.id
            WHERE m.user_name = :user_name
        """)
        df_titles = pd.read_sql(query, conn, params={"user_name": user_name})
    return df_titles['title'].tolist()


# 카테고리 분리
def extract_genres(data):
    genre_list = []
    for cat in data['catgory']:
        seen = set()
        split_genres = sum([g.split('>') for g in cat.split('/')], [])
        genre_list.append([g for g in split_genres if not (g in seen or seen.add(g))])
    return genre_list


# 작가명 분리
def extract_authors(data):
    return [author.split() for author in data['writer'].to_list()]

