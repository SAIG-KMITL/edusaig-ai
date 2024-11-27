from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime

class Teacher(BaseModel):
  id: str
  username: str
  fullname: str
  role: str
  password: str
  email: str
  points: int
  createdAt: datetime
  updatedAt: datetime
  profileKey: Optional[str] = None

class Category(BaseModel):
  id: str
  title: str
  description: str
  slug: str
  createdAt: datetime
  updatedAt: datetime

class Course(BaseModel):
  id: str
  title: str
  description: str
  thumbnailKey: str
  teacherId: str
  duration: int
  level: str
  price: float
  status: str
  createdAt: datetime
  updatedAt: datetime
  teacher: Teacher
  category: Category

class RoadMapGeneratorRequest(BaseModel):
  user_data: Dict[str, Any]
  courses: List[Course]

  class Config:
      json_schema_extra = {
          "example": {
              "user_data": {
                  "userID": "U2672",
                  "name": "User_293",
                  "age": 39,
                  "university": "Yale",
                  "department": "Game Development",
                  "interest": [
                      "Robotics",
                      "Cloud Computing",
                      "Data Science"
                  ],
                  "preTestScore": 93,
                  "preTestDescription": "Strong in algorithm design, programming fundamentals. Needs improvement in architectural patterns, performance optimization."
              },
              "courses": [
                  {
                      "id": "fa51a450-f8b0-42a3-93f4-cc780b1cc5d8",
                      "title": "Introduction to Programming",
                      "description": "This course is an introduction to programming",
                      "thumbnailKey": "https://www.example.com/thumbnail.jpg",
                      "teacherId": "teacherId-123",
                      "duration": 60,
                      "level": "beginner",
                      "price": 100,
                      "status": "published",
                      "createdAt": "2024-11-13T09:20:12.477Z",
                      "updatedAt": "2024-11-13T09:20:12.477Z",
                      "teacher": {
                          "id": "36ade201-cb69-41eb-a36d-266f3b31139d",
                          "username": "johndoe",
                          "fullname": "John Doe",
                          "role": "teacher",
                          "password": "$argon2id$v=19$m=65536,t=3,p=4$GOKD6bEQshgetAUK006XTQ$fUDic1gaH+iJa7CUZAQBj7Q5UDRvc39CwITWkbwW0kA",
                          "email": "johndoe@gmail.com",
                          "points": 0,
                          "createdAt": "2024-11-13T16:14:55.623Z",
                          "updatedAt": "2024-11-13T16:14:55.623Z",
                          "profileKey": None
                      },
                      "category": {
                          "id": "122ec4ae-5e82-481a-9711-ec974224ac7b",
                          "title": "javascript",
                          "description": "high level programming language",
                          "slug": "course",
                          "createdAt": "2024-11-13T09:19:56.058Z",
                          "updatedAt": "2024-11-13T09:19:56.058Z"
                      }
                  }
              ]
          }
      }