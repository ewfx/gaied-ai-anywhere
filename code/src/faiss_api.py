from fastapi import FastAPI, HTTPException
import faiss
import pandas as pd
import numpy as np
from pydantic import BaseModel
import os
import requests
from utils.util import process_file
from graph import agentic_email_triage
# Initialize FastAPI
app = FastAPI()
class FilePathRequest(BaseModel):
    file_path: str

@app.post("/process_document/")
async def process_document(file_req: FilePathRequest):
    """Processes an uploaded file and stores text in FAISS"""
    file_path = file_req.file_path

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found.")

    text = process_file(file_path)
    result = agentic_email_triage(text)

    return {"message": f"Processed successfully!", "result": result}

@app.get("/")
def root():
    return {"message": "FAISS Text Search API is running!"}
