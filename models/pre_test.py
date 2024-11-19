from pydantic import BaseModel, Field
from typing import List, Optional

class PreTestRequest(BaseModel):
    user_interested_topic: str = "I want to know about Python."
    difficulty: str = "Beginner"