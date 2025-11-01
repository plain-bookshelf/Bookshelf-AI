from pydantic import BaseModel

class BookInfo(BaseModel):
    title: str