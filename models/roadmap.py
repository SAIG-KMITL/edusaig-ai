from pydantic import BaseModel
from typing import Dict, Any, List
from datetime import datetime

class RoadMapGeneratorRequest(BaseModel):
  user_data: Dict[str, Any]
  courses: List[Dict[str, Any]]

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
                      "courseID": "CS917",
                      "courseName": "Blockchain Development",
                      "courseDescription": "Develop professional-grade skills with industry-standard tools and practices.",
                      "courseLevel": "Advanced",
                      "duration": "4 weeks",
                      "lastUpdated": "2024-05-01"
                  }
              ]
          }
      }

# from pydantic import BaseModel, Field
# from typing import List
# from pydantic import BaseModel

# class UserData(BaseModel):
#   userID: str
#   name: str
#   age: int
#   university: str
#   department: str
#   interest: List[str]
#   preTestScore: int
#   preTestDescription: str

# class Course(BaseModel):
#   courseID: str
#   courseName: str
#   courseDescription: str
#   courseLevel: str
#   duration: str
#   lastUpdated: str

# class RoadMapGeneratorRequest(BaseModel):
#   user_data: UserData
#   courses: List[Course]