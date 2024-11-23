from fastapi import APIRouter, status
from internal.LLMRequest import LLMRequest
from internal.qa_processor import QAProcessor
from models.mock_qa import MockQARequest
import utils.response as res
import os
from dotenv import load_dotenv

router = APIRouter()

load_dotenv()
url = os.getenv("SAIG_LLM_URL")
model_name = "meta-llama/Meta-Llama-3.1-8B-Instruct"
llm_request = LLMRequest(url=url, model=model_name)

@router.post("/qa", status_code=status.HTTP_200_OK)
async def qa(body: MockQARequest):
    """
    QA endpoint to process chapter summary and chat history, and return an AI-generated response.
    """
    try:
        # Initialize the PromptProcessor
        processor = QAProcessor()

        # Generate the prompt
        prompt = processor.generate_qa_prompt(
            chapter_summary=body.chapter_summary,
            chat_history=body.chat_history
        )

        # Prepare messages for the LLM
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]

        # Send the prompt to the LLM
        response = llm_request.send_request(messages)

        # Extract the answer from the response
        if response and "choices" in response and len(response["choices"]) > 0:
            # Return the content of the assistant's message (plain string)
            output = {"answer":response["choices"][0]["message"]["content"]}
            return res.success_response_status(
                status=status.HTTP_200_OK,
                payload = output
            )
        else:
            return res.error_response_status(
                status=status.HTTP_400_BAD_REQUEST,
                message="Failed to get a valid response from LLM."
            )

    except Exception as e:
        return res.error_response_status(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"An error occurred: {str(e)}"
        )
