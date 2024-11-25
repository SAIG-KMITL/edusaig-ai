from pydantic import BaseModel, Field
from typing import List, Optional

class ASRRequest(BaseModel):
    url: str = "https://res.cloudinary.com/dzdnk2a88/video/upload/v1732371616/hcwqyiiybi0pwfpykvho.mp4"
    language: str = "en"