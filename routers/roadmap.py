from fastapi import APIRouter, status
from models.roadmap import RoadMapGeneratorRequest
import utils.response as res
from internal.roadmap_agent import generate_roadmap

router = APIRouter()

@router.post("/generate-roadmap", status_code=status.HTTP_200_OK)
async def roadmap_generator(body: RoadMapGeneratorRequest):
  # Required fields for validation
  required_user_fields = ["userID", "name", "interest"]
  required_course_fields = ["id", "title", "description", "level", "duration", "status"]

  # Validate user_data
  if not body.user_data or not all(key in body.user_data for key in required_user_fields):
      return res.error_response_status(
          status=status.HTTP_400_BAD_REQUEST,
          message=f"Invalid or incomplete user data. Required fields: {', '.join(required_user_fields)}"
      )

  # Validate courses
  if not body.courses:
      return res.error_response_status(
          status=status.HTTP_400_BAD_REQUEST,
          message="Courses list cannot be empty."
      )

  # Validate each course
  for course in body.courses:
      # Convert Pydantic model to dict for field checking
      course_dict = course.model_dump()
      missing_fields = [field for field in required_course_fields if field not in course_dict]
      
      if missing_fields:
          return res.error_response_status(
              status=status.HTTP_400_BAD_REQUEST,
              message=f"Course {course.id} is missing required fields: {', '.join(missing_fields)}"
          )
      
      # Validate duration is a positive integer
      if not isinstance(course.duration, int) or course.duration <= 0:
          return res.error_response_status(
              status=status.HTTP_400_BAD_REQUEST,
              message=f"Course {course.id} has invalid duration. Duration must be a positive integer."
          )

  try:
      response = generate_roadmap(body.user_data, body.courses)

      if response:
          return res.success_response_status(
              status=status.HTTP_200_OK,
              payload=response
          )
      else:
          return res.error_response_status(
              status=status.HTTP_400_BAD_REQUEST,
              message="Failed to generate roadmap."
          )
  except Exception as e:
      return res.error_response_status(
          status=status.HTTP_500_INTERNAL_SERVER_ERROR,
          message=f"An error occurred: {str(e)}"
      )