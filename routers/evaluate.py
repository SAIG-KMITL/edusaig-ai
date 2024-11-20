from fastapi import APIRouter, status
from internal.LLMRequest import LLMRequest
from models.evaluate import EvaluateTestRequest
import utils.response as res
import os

router = APIRouter()


url = os.getenv("SAIG_LLM_URL")
model_name = "meta-llama/Meta-Llama-3.1-8B-Instruct"
llm_request = LLMRequest(url=url, model=model_name)

@router.post("/qa", status_code=status.HTTP_200_OK)
async def qa(body: EvaluateTestRequest):
    messages = [
        {
            "role": "system",
            "content": "You are a programming professional designed to evaluate user answer and give short advise not longer than 250 words on where user might be wrong and how to improve."
        },
        {
            "role": "user",
            "content": """The question is {} and the correct answer is {} but user answer is {}. Give the user advise on why it's wrong and what should they improve?""".format(body.question, body.correct_choice, body.user_ans)
        }
    ]
    
    response = llm_request.send_request(messages)
    
    if response:
        return res.success_response_status(
            status=status.HTTP_200_OK,
            message="Generate comment successful",
            data=response
        )
    else:
        return res.error_response_status(
            status=status.HTTP_400_BAD_REQUEST,
            message="Failed to get a valid response from LLM."
        )