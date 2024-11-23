from pydantic import BaseModel
from typing import List, Dict

class MockQARequest(BaseModel):
    chapter_summary: str = "เรียน Python ได้ที่ Edusaig"
    chat_history: List[Dict[str, str]] = [
        {'user': "สวัสดีค่ะ"},
        {'agent': "สวัสดีค่ะ"},
        {'user': "เรียน Python ที่ไหนดี"}
    ]