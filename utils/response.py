from fastapi.responses import JSONResponse
from fastapi import HTTPException, status

def success_response_status(status: status, question_json: str):
    res = JSONResponse(
        status_code=status,
        content=question_json
    ) 
    return res

def error_response_status(status: status, message: str):
    return HTTPException(
        status_code=status,
        detail={"message": message}
    )