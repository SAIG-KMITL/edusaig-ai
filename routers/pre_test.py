from fastapi import APIRouter, status
from internal.LLMRequest import LLMRequest
from models.pre_test import PreTestRequest
import utils.response as res
import os
import json
import ast
from dotenv import load_dotenv
load_dotenv()

n = 1
router = APIRouter(
    tags=["pre-test"],
)

url = os.getenv("SAIG_LLM_URL")
model_name = "meta-llama/Meta-Llama-3.1-8B-Instruct"
llm_request = LLMRequest(url=url, model=model_name)

@router.post("/generate-pretest/", status_code=status.HTTP_200_OK)
async def qa(body: PreTestRequest):
    messages = [
        {
            "role": "system",
            "content": "You are a programming professional designed that can make test question in Beginner, Intermediate and Expert difficulty about the subject that the user ask."
        },
        {
            "role": "user",
            "content": """Make list of 20 questions which are design to be choices question but without the choices, answer and no number index that are about this request in a {} difficulty {} . in array format such as ["question1", "question2", "question3", ...] no need for confirmation message""".format(body.user_interested_topic, body.difficulty)
        }
    ]
    
    response = llm_request.send_request(messages)
    
    response_data = response
    
    content = response_data["choices"][0]["message"]["content"]
    
    questions = ast.literal_eval(content)

    if response:
        final_json = []
        for q in questions:
            messages_choice = [
                    {
                        "role": "system",
                        "content": "You are a programming professional designed to make a choice and answer for the question user provide by output as JSON response."
                    },
                    {
                        "role": "user",
                        "content": "Make 4 choices and show the correct choice at the end of the question no need to explain for each of this question " + q + """ in only this JSON object {"question":Question,"choices":{"a":choice A,"b":choice B,"c":choice C,"d":choice D},"answer":correct_choice (Use only lowercase a,b,c,d)}. Please provide the JSON with proper formatting and include the closing brace `}`."""
                    }
            ]
            response_ans = llm_request.send_request(messages_choice)

            content_ans = response_ans["choices"][0]["message"]["content"]

            json_data = json.loads(content_ans)

            if response_ans:
                final_json.append(json_data)
            else:
                return res.error_response_status(
                status=status.HTTP_400_BAD_REQUEST,
                message="Failed to get a valid response from LLM."
            )
        return res.success_response_status(
            status=status.HTTP_200_OK,
            message="Generate comment successful",
            questions_json=final_json
        )
    
    else:
        return res.error_response_status(
            status=status.HTTP_400_BAD_REQUEST,
            message="Failed to get a valid response from LLM."
        )