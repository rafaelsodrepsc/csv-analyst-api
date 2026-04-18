from fastapi import FastAPI
from routers import datasets
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent.parent / ".env")

app = FastAPI()

app.include_router(datasets.router)