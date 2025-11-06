import pandas as pd
from sqlalchemy import create_engine, text
from .config import DB_URL

engine = create_engine(DB_URL)

def load_books_from_db():
    query = text("""
        SELECT 
            b.book_name AS title,
            b.book_author AS writer,
            b.publisher,
            a.affiliation_name AS school,
            bd.registration_number AS id_number,
            bd.call_number AS call_num,
            b.publication_date AS pubdata,
            b.book_type AS catgory,
            b.book_introduction AS description
        FROM book b
        LEFT JOIN book_detail bd ON bd.book = b.id
        LEFT JOIN affiliation a ON bd.affiliation = a.id;
    """)
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df
