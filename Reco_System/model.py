from pydantic import BaseModel

class BookUserName(BaseModel):
    user_name: str