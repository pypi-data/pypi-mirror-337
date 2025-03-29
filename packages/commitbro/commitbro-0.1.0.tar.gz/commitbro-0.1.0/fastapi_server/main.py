"""
main.py
---------
FastAPI backend for receiving commit history data and triggering training.
This is your remote training API.
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Commit(BaseModel):
    hash: str
    message: str
    body: str

class TrainingData(BaseModel):
    commits: List[Commit]

@app.post("/train")
async def train_model(data: TrainingData):
    # Log the received commits for debugging.
    print(f"[*] Received {len(data.commits)} commits for training.")
    if data.commits:
        print(f"[*] First commit:\nMessage: {data.commits[0].message}\nHash: {data.commits[0].hash}")
    
    # Here, you would normally trigger your training pipeline.
    return {
        "status": "training_started",
        "model": "user-custom-model-v1",
        "received_commits": len(data.commits)
    }

# To run this FastAPI app locally, use:
# uvicorn main:app --reload
