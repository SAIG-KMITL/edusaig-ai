from fastapi import APIRouter, status
from internal.LLMRequest import LLMRequest
from models.evaluate import EvaluateTestRequest
import utils.response as res
import os
from dotenv import load_dotenv
load_dotenv()

router = APIRouter(
    tags = ["evaluate-test"]
)


url = os.getenv("SAIG_LLM_URL")
model_name = "meta-llama/Meta-Llama-3.1-8B-Instruct"
llm_request = LLMRequest(url=url, model=model_name)

@router.post("/evaluate", status_code=status.HTTP_200_OK)
async def qa(body: EvaluateTestRequest):
    eva = ""
    questions = body.question
    correct = body.correct_answer
    ans = body.user_answer
    for i in range(1, len(questions)):
        cur = {
            "question": questions[i],
            "correct": correct[i],
            "answer": ans[i]
        }
        eva = eva + '\n' + str(cur)
    messages = [
        {
            "role": "system",
            "content": "You are a professional assistance and a professional programming tutor designed to evaluate user answer and give user whose are like student **in only one short polite advise paragraph not longer than 750 words** on where they might be wrong and how to improve."
        },
        {
            "role": "user",
            "content": "From this list of question that include the correct aswer and what user have answer. Give user an advise for each topic in a short paragraph on how they can improve their performance and what course topic should they focus on learning." + eva + """
            Output in this format:
            From the test result...(What user miss and how to improve)

            Recommend topic that you should review on
            -
            -
            -
            **No need for any confimation message. Just show the advise.**"""
        }
    ]
    
    response = llm_request.send_request(messages)

    content = response["choices"][0]["message"]["content"]
    
    if response:
        return res.success_response_status(
            status=status.HTTP_200_OK,
            payload=content
        )
    else:
        return res.error_response_status(
            status=status.HTTP_400_BAD_REQUEST,
            message="Failed to get a valid response from LLM."
        )