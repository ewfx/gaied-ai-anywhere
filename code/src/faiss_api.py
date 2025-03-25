from fastapi import FastAPI, HTTPException
import faiss
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from pydantic import BaseModel
import os
import requests
#from docling.loaders import DoclingLoader
from utils.util import process_file

# Initialize FastAPI
app = FastAPI()

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")
dimension = 384  # MiniLM model output size

# Initialize FAISS index
index = faiss.IndexFlatL2(dimension)

# Metadata storage
metadata_store = []

# Document extractor
#extractor = DoclingLoader()

# Load existing index and metadata if available
# Load existing index and metadata if available
if os.path.exists("faiss_index.idx"):
    index = faiss.read_index("faiss_index.idx")
    metadata_store = pd.read_csv("metadata.csv").to_dict(orient="records")
    print("✅ Loaded existing FAISS index.")
else:
    print("⚠️ No existing FAISS index found. Starting fresh.")

# Models
class Document(BaseModel):
    doc_id: str
    text: str

class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

class FilePathRequest(BaseModel):
    file_path: str

@app.post("/process_document/")
async def process_document(file_req: FilePathRequest):
    """Processes an uploaded file and stores text in FAISS"""
    file_path = file_req.file_path

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found.")

    text = process_file(file_path)
    doc_id = os.path.basename(file_path)
    # Store in FAISS
    embedding = model.encode([text]).astype(np.float32)
    index.add(embedding)
    metadata_store.append({"doc_id": doc_id, "text": text})

    # Save FAISS index
    faiss.write_index(index, "faiss_index.idx")
    pd.DataFrame(metadata_store).to_csv("metadata.csv", index=False)

    return {"message": f"Processed and stored {doc_id} successfully!"}

@app.post("/add_document/")
async def add_document(doc: Document):
    """Store document embedding in FAISS"""
    embedding = model.encode([doc.text]).astype(np.float32)
    index.add(embedding)
    metadata_store.append({"doc_id": doc.doc_id, "text": doc.text})

    # Save FAISS index
    faiss.write_index(index, "faiss_index.idx")
    pd.DataFrame(metadata_store).to_csv("metadata.csv", index=False)

    return {"message": f"Document {doc.doc_id} added successfully!"}

@app.post("/search/")
async def search(query: QueryRequest):
    """Search FAISS for similar documents"""
    if index.ntotal == 0:
        raise HTTPException(status_code=400, detail="No documents in FAISS index.")

    query_embedding = model.encode([query.query]).astype(np.float32)
    D, I = index.search(query_embedding, k=query.top_k)

    results = [{"doc_id": metadata_store[i]["doc_id"], "text": metadata_store[i]["text"], "distance": float(D[0][j])}
               for j, i in enumerate(I[0]) if i != -1]

    return {"query": query.query, "results": results}

@app.get("/")
def root():
    return {"message": "FAISS Text Search API is running!"}
