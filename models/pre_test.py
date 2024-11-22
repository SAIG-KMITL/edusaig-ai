from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional

class User(BaseModel):
    id: str = "8d4887aa-28e7-4d0e-844c-28a8ccead003"
    email: str = "johndoe@gmail.com"
    points: int = 200
    role: str = "student"
    createdAt: datetime = datetime(2024, 11, 20, 14, 5, 10, 6000)
    updatedAt: datetime = datetime(2024, 11, 20, 14, 5, 10, 6000)
    fullname: str = "John Doe"

class Occupation(BaseModel):
    id: str = "oc-001"
    title: str = "Computer Engineer"
    description: str = "Computer Engineering combines hardware and software design to create and optimize computing systems."
    createdAt: datetime = datetime(2024, 11, 20, 15, 1, 56, 406000)
    updatedAt: datetime = datetime(2024, 11, 20, 15, 1, 56, 406000)

class Topic(BaseModel):
    id: str = "string"
    title: str = "string"
    description: str = "string"
    level: str = "string"
    createdAt: datetime = datetime(2024, 11, 20, 15, 1, 56, 406000)
    updatedAt: datetime = datetime(2024, 11, 20, 15, 1, 56, 406000)

class PreTestRequest(BaseModel):
    id: str = "1"
    user: User = User()
    topics: List[Topic] = [
        Topic(
            id="py-001",
            title="Python Programming",
            description="An introductory topic on Python programming, covering basic syntax, data structures, and simple algorithms.",
            level="beginner",
            createdAt=datetime(2024, 11, 20, 15, 1, 56, 406000),
            updatedAt=datetime(2024, 11, 20, 15, 1, 56, 406000),
        ),
        Topic(
            id="hw-001",
            title="Computer Hardware Basics",
            description="A foundational topic focusing on the essential components of computer hardware, such as CPUs, memory, and storage devices.",
            level="beginner",
            createdAt=datetime(2024, 11, 20, 15, 1, 56, 406000),
            updatedAt=datetime(2024, 11, 20, 15, 1, 56, 406000),
        )
    ]
    occupation: Occupation = Occupation()
    createdAt: datetime = datetime(2024, 11, 20, 15, 1, 56, 406000)
    updatedAt: datetime = datetime(2024, 11, 20, 15, 1, 56, 406000)