from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import evaluate
from routers import pre_test
from routers import mock_qa 
from routers import asr
from routers import roadmap
from routers import Summarize

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

app.include_router(
    roadmap.router, 
    tags=["roadmap"]
)

app.include_router(
    pre_test.router,
    tags=["pre-test"]
)

app.include_router(
    evaluate.router,
    tags=["evaluate-test"]
)

app.include_router(
    Summarize.router,
    tags=["Summarize"]
)