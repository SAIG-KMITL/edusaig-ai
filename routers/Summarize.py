from fastapi import APIRouter, status
from internal.SumService import Summarization
from models.SumModels import SumRequest
import utils.response as res
import os

from dotenv import load_dotenv
load_dotenv()

router = APIRouter()

print("chck")

url = os.getenv("SAIG_LLM_URL")
model_name = "meta-llama/Meta-Llama-3.1-8B-Instruct"
llm_request = Summarization(url=url, model=model_name)

@router.post("/sum", status_code=status.HTTP_200_OK)
async def sum(body: SumRequest):

    
    response = llm_request.SumText(body.content)["choices"][0]["message"]["content"]
    output = {"summary":response}
    
    if response:
        return res.success_response_status(
            status=status.HTTP_200_OK,
            payload = output
        )
    else:
        return res.error_response_status(
            status=status.HTTP_400_BAD_REQUEST,
            message="Failed to get a valid response from LLM."
        )