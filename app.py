from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import mock_qa 
from routers import asr

app = FastAPI(openapi_prefix="/ai")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(
    mock_qa.router,
    tags=["mock_qa"]
)

app.include_router(asr.router)