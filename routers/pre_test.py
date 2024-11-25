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
    max_question = 5
    response_topic = body.topics
    topic_titles = [topic.title for topic in response_topic]
    topic_amount = len(topic_titles)
    amount_per_topic = round(max_question / topic_amount)
    diff_titles = [diff.level for diff in response_topic]
    current_amount = 0
    n = 0
    max_retries = 3
    final_questions = []
    final_json = []
    if topic_titles:
        for t in topic_titles:
            if topic_amount - n != 1:
                if amount_per_topic == 1:
                    messages = [
                        {
                            "role": "system",
                            "content": "You are a adviser designed to make test question in Beginner, Intermediate and Expert difficulty about the topics that user say they know about to test their knowledge."
                        },
                        {
                            "role": "user",
                            "content": "User want to be {}. Make **exactly only** ".format(body.occupation.title) + str(amount_per_topic) + " question which are design to be choices question but without the choices, answer and no number index that are about " + str(t) + " in a " + str(diff_titles[n]) + """ difficulty. In array format such as [\"question1\"] no need for confirmation message"""
                        }
                    ]
                else:
                    messages = [
                        {
                            "role": "system",
                            "content": "You are a adviser designed to make test question in Beginner, Intermediate and Expert difficulty about the topics that user say they know about to test their knowledge."
                        },
                        {
                            "role": "user",
                            "content": "User want to be {}. Make **exactly only** ".format(body.occupation.title) + str(amount_per_topic) + " question which are design to be choices question but without the choices, answer and no number index that are about " + str(t) + " in a " + str(diff_titles[n]) + """ difficulty. In array format such as [\"question1\", \"question2\", ...] no need for confirmation message"""
                        }
                    ]

            elif topic_amount - n == 1:
                current_topic_amount = max_question - current_amount
                if current_topic_amount == 1:
                    messages = [
                    {
                        "role": "system",
                        "content": "You are a adviser designed to make test question in Beginner, Intermediate and Expert difficulty about the topics that user say they know about to test their knowledge."
                    },
                    {
                        "role": "user",
                        "content": "User want to be {}. Make **exactly only** ".format(body.occupation.title) + str(current_topic_amount) + " question which are design to be choices question but without the choices, answer and no number index that are about " + str(t) + " in a " + str(diff_titles[n]) + """ difficulty. In array format such as [\"question1\"] no need for confirmation message"""
                    }
                ]
                else:
                    messages = [
                        {
                            "role": "system",
                            "content": "You are a adviser designed to make test question in Beginner, Intermediate and Expert difficulty about the topics that user say they know about to test their knowledge."
                        },
                        {
                            "role": "user",
                            "content": "User want to be {}. Make **exactly only** ".format(body.occupation.title) + str(current_topic_amount) + " question which are design to be choices question but without the choices, answer and no number index that are about " + str(t) + " in a " + str(diff_titles[n]) + """ difficulty. In array format such as [\"question1\", \"question2\", ...] no need for confirmation message"""
                        }
                    ]

            n = n + 1
            retries = 0
            while retries < max_retries:
                try:
 
                    response = llm_request.send_request(messages)

                    if response:
                        content = response["choices"][0]["message"]["content"]
                        questions = ast.literal_eval(content)
                        for single_question in questions:
                            final_questions.append(single_question)
                            current_amount += 1
                        break
                except (json.JSONDecodeError, ValueError, SyntaxError) as e:
                    retries += 1
                    print(f"Error on topic {t}, retrying {retries}/{max_retries}...")
            if retries == max_retries:
                print(f"Failed to generate questions for topic {t} after {max_retries} retries.")

    elif body.occupation.title and not topic_titles:
        messages = [
            {
                "role": "system",
                "content": "You are a adviser designed to make test question in Beginner, Intermediate and Expert difficulty about the topics that user say they know about to test their knowledge."
            },
            {
                "role": "user",
                "content": """User want to be {}.Make list of 5 questions which are design to be choices question but without the choices, answer and no number index that are about the fundamental of what user want to be. in array format such as ["question1", "question2", "question3", ...] no need for confirmation message""".format(body.occupation.title)
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
        for q in range(0,5):
                current_question = final_questions[q]
                messages_choice = [
                        {
                            "role": "system",
                            "content": "You are a programming professional designed to make a choice and answer for the question user provide by output as JSON response."
                        },
                        {
                            "role": "user",
                            "content": "Make 4 choices and show the correct choice at the end of the question no need to explain for each of this question " + str(current_question) + """ in only this JSON object {"question":Question,"choices":{"a":choice A,"b":choice B,"c":choice C,"d":choice D},"answer":correct_choice (Use only lowercase a,b,c,d)}. Please provide the JSON with proper formatting and include the closing brace `}`."""
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