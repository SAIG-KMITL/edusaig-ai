from pydantic import BaseModel
from typing import List, Dict

class MockQARequest(BaseModel):
    chapter_summary: str
    chat_history: List[Dict[str, str]]