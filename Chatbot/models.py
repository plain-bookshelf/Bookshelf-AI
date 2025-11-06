from pydantic import BaseModel

class Chat(BaseModel):
    user_said: str
    user_id: str