from pydantic import BaseModel, Field
from typing import List, Optional

class MockQARequest(BaseModel):
    content: str = "แนะนำที่เที่ยวกรุงเทพหน่อย"