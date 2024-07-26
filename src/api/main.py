import os
from pathlib import Path
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from orchestrator import Task, create

load_dotenv()

app = FastAPI()


origins = [
    o.strip()
    for o in Path(Path(__file__).parent / "origins.txt").read_text().splitlines()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/api/article")
async def create_article(task: Task):
    return StreamingResponse(
        create(task.research, task.products, task.assignment),
        media_type="application/x-ndjson",
    )
