import io
from pydantic import BaseModel

class emotionRequest(BaseModel):
    content: str