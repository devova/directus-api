from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(config=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from directus.collections.test1 import TestCollection  # noqa
