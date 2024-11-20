from pydantic import BaseModel, Field
from typing import List, Optional

class EvaluateTestRequest(BaseModel):
    question: str = "What is the purpose of the 'print' function in Python?"
    correct_answer: str = "To print output to the screen"
    user_answer: str = "To define variables"