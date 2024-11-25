from fastapi import APIRouter, status
from internal.LLMRequest import LLMRequest
from models.pre_test import PreTestRequest
import utils.response as res
import os
import json
import ast
from dotenv import load_dotenv
load_dotenv()

router = APIRouter(
    tags=["pre-test"],
)

url = os.getenv("SAIG_LLM_URL")
model_name = "meta-llama/Meta-Llama-3.1-8B-Instruct"
llm_request = LLMRequest(url=url, model=model_name)

@router.post("/generate-pretest/", status_code=status.HTTP_200_OK)
async def qa(body: PreTestRequest):
    response_topic = body.topics
    topic_titles = [topic.title for topic in response_topic]
    diff_titles = [diff.level for diff in response_topic]
    n = 0
    final_questions = []
    final_json = []
    if topic_titles:
        for t in topic_titles:
            messages = [
                {
                    "role": "system",
                    "content": "You are a adviser designed to make test question in Beginner, Intermediate and Expert difficulty about the topics that user say they know about to test their knowledge."
                },
                {
                    "role": "user",
                    "content": "User want to be {}.Make list of 10 questions which are design to be choices question but without the choices, answer and no number index that are about ".format(body.occupation.title) + str(t) + "in a" + str(diff_titles[n]) + """difficulty. in array format such as ["question1", "question2", "question3", ...] no need for confirmation message"""
                }
            ]
 
            response = llm_request.send_request(messages)
            
            n = n + 1
            if response:
                try:
                    content = response["choices"][0]["message"]["content"]
                    questions = ast.literal_eval(content)
                    for single_question in questions:
                        final_questions.append(single_question)
                except (json.JSONDecodeError, ValueError, SyntaxError) as e:
                    response = llm_request.send_request(messages)
            else:
                return res.error_response_status(
                    status=status.HTTP_400_BAD_REQUEST,
                    message="Failed to get a valid response from LLM."
                )
    elif body.occupation.title and not topic_titles:
        messages = [
            {
                "role": "system",
                "content": "You are a adviser designed to make test question in Beginner, Intermediate and Expert difficulty about the topics that user say they know about to test their knowledge."
            },
            {
                "role": "user",
                "content": """User want to be {}.Make list of 10 questions which are design to be choices question but without the choices, answer and no number index that are about the fundamental of what user want to be. in array format such as ["question1", "question2", "question3", ...] no need for confirmation message""".format(body.occupation.title)
            }
        ]

        response = llm_request.send_request(messages)
        
        n = n + 1
        if response:
            try:
                content = response["choices"][0]["message"]["content"]
                questions = ast.literal_eval(content)
                for single_question in questions:
                    final_questions.append(single_question)
            except (json.JSONDecodeError, ValueError, SyntaxError) as e:
                response = llm_request.send_request(messages)
        else:
            return res.error_response_status(
                status=status.HTTP_400_BAD_REQUEST,
                message="Failed to get a valid response from LLM."
            )
    else:
        return res.error_response_status(
                status=status.HTTP_400_BAD_REQUEST,
                message="Failed to get a valid topic or occupation."
            )
    if final_questions:
        for q in final_questions:
                messages_choice = [
                        {
                            "role": "system",
                            "content": "You are a programming professional designed to make a choice and answer for the question user provide by output as JSON response."
                        },
                        {
                            "role": "user",
                            "content": "Make 4 choices and show the correct choice at the end of the question no need to explain for each of this question " + str(q) + """ in only this JSON object {"question":Question,"choices":{"a":choice A,"b":choice B,"c":choice C,"d":choice D},"answer":correct_choice (Use only lowercase a,b,c,d)}. Please provide the JSON with proper formatting and include the closing brace `}`."""
                        }
                ]

                response_ans = llm_request.send_request(messages_choice)

                if response_ans:
                    try:
                        content_ans = response_ans["choices"][0]["message"]["content"]
                        json_data = json.loads(content_ans)
                        final_json.append(json_data)
                    except (json.JSONDecodeError, ValueError, SyntaxError, KeyError) as e:
                        print(f"Error parsing JSON")
                        print("Raw response:", response_ans)
                        response_ans = llm_request.send_request(messages_choice)
                else:
                    return res.error_response_status(
                    status=status.HTTP_400_BAD_REQUEST,
                    message="Failed to get a valid response from LLM."
                )
        return res.success_response_status(
                status=status.HTTP_200_OK,
                payload=final_json
            )