from fastapi.responses import JSONResponse
from fastapi import HTTPException, status

def success_response_status(status: status, advise: str):
    res = JSONResponse(
        status_code=status,
        content=advise
    ) 
    return res

def error_response_status(status: status, message: str):
    return HTTPException(
        status_code=status,
        detail={"message": message}
    )