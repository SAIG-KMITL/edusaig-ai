from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
    Summarize.router,
    tags=["Summarize"]
)