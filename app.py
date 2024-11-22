from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import evaluate
from routers import pre_test
from routers import mock_qa
from routers import Summarize
from routers import roadmap

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