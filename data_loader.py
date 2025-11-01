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

# DB에서 book + book_detail + affiliation JOIN
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
                a.affiliation_name AS school
            FROM book b
            LEFT JOIN book_detail bd ON bd.book = b.id
            LEFT JOIN affiliation a ON bd.affiliation = a.id
        """)
        data = pd.read_sql(query, conn)

    # 결측값 처리
    data['title'] = data['title'].fillna('')
    data['writer'] = data['writer'].fillna('')
    data['publisher'] = data['publisher'].fillna('')
    data['publication_date'] = data['publication_date'].fillna('')
    data['description'] = data['description'].fillna('')
    data['catgory'] = data['catgory'].fillna('')
    data['img'] = data['img'].fillna('')
    data['school'] = data['school'].fillna('')
    data['id_number'] = data['id_number'].fillna('')
    data['call_num'] = data['call_num'].fillna('')

    # 책 소개에서 특수문자 제거
    data['description'] = data['description'].str.replace('[^가-힣a-zA-Z0-9 .,!?]', '', regex=True)

    # 이미지 기준 중복 제거
    data = data.drop_duplicates(subset=['img']).reset_index(drop=True)

    return data


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


# 대여한 책 제목
def load_rented_book_titles():
    with engine.connect() as conn:
        query = text("""
            SELECT DISTINCT 
                b.book_name AS title
            FROM book_rental_record br
            JOIN book_detail bd ON br.book_detail = bd.id
            JOIN book b ON bd.book = b.id;
        """)
        df_titles = pd.read_sql(query, conn)
    return df_titles['title'].to_list()