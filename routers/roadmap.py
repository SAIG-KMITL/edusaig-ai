from fastapi import APIRouter, status
from models.roadmap import RoadMapGeneratorRequest
import utils.response as res
from internal.roadmap_agent import generate_roadmap

router = APIRouter()

@router.post("/roadmap_generator", status_code=status.HTTP_200_OK)
async def roadmap_generator(body: RoadMapGeneratorRequest):
   # Validate user_data
   if not body.user_data or not all(key in body.user_data for key in ["userID", "name", "interest"]):
        return res.error_response_status(
             status=status.HTTP_400_BAD_REQUEST,
             message="Invalid or incomplete user data."
        )
   
   # Validate courses
   if not body.courses or not all(key in course for course in body.courses 
                                for key in ["courseID", "courseName", "courseLevel"]):
        return res.error_response_status(
             status=status.HTTP_400_BAD_REQUEST,
             message="Invalid or incomplete courses data."
        )
   
   try:
        response = generate_roadmap(body.user_data, body.courses)
   
        if response:
             return res.success_response_status(
                  status=status.HTTP_200_OK,
                  message="Roadmap generated successfully",
                  data=response
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