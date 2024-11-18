from pydantic import BaseModel, Field
from typing import List, Optional

class SumRequest(BaseModel):
    content: str = "แนะนำที่เที่ยวกรุงเทพหน่อย"