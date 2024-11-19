from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import pre_test

app = FastAPI(openapi_prefix="/ai")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(
    pre_test.router,
    tags=["pre-test"]
)