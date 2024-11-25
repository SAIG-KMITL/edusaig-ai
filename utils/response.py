from fastapi.responses import JSONResponse
from fastapi import HTTPException, status


def success_response_status(status: status, payload: dict):
    res = JSONResponse(
        status_code=status,
        content=payload
    ) 
    return res

def error_response_status(status: status, message: str):
    return HTTPException(
        status_code=status,
        detail={"message": message}
    )