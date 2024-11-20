from pydantic import BaseModel, Field
from typing import List, Optional

class EvaluateTestRequest(BaseModel):
    question: str = "What is the purpose of the 'print' function in Python?"
    correct_choice: str = "To print output to the screen"
    user_ans: str = "To define variables"