from pydantic import BaseModel, Field
from typing import List, Optional

class ASRRequest(BaseModel):
    url: str = "https://youtu.be/D5uvVt08vEY?si=FBPXxXdeuQpbBOB_"
    language: str = "en"