from fastapi import APIRouter, status
from internal.LLMRequest import LLMRequest
from models.mock_qa import MockQARequest
import utils.response as res
import os

router = APIRouter(
    prefix="/mock-qa",
    tags=["mock-qa"],
)

url = os.getenv("SAIG_LLM_URL")
model_name = "meta-llama/Meta-Llama-3.1-8B-Instruct"
llm_request = LLMRequest(url=url, model=model_name)

@router.post("/qa", status_code=status.HTTP_200_OK)
async def qa(body: MockQARequest):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": body.content},
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