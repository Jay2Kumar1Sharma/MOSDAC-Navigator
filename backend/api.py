import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from .knowledge_base import KnowledgeBase
from .llm_handler import LLMHandler
from .config import API_HOST, API_PORT

app = FastAPI(title="MOSDAC AI Help Bot API")

try:
    kb = KnowledgeBase()
    llm = LLMHandler()
except FileNotFoundError as e:
    print(f"FATAL ERROR: {e}")
    kb = None
    llm = None

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str

@app.post("/query", response_model=QueryResponse)
def handle_query(request: QueryRequest):
    if not kb or not llm:
        return {"answer": "Error: Backend services are not initialized. Please check the server logs."}
    
    context_docs = kb.query(request.query)
    answer = llm.get_response(request.query, context_docs)
    return {"answer": answer}

if __name__ == "__main__":
    uvicorn.run(app, host=API_HOST, port=API_PORT)