from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import json
from workflow_rag import ProjectKnowledgeWorkflow

app = FastAPI()

# תיקון שגיאת התחברות (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

@app.post("/ask")
async def ask_question(request: QueryRequest):
    print(f"📩 קיבלתי שאלה: {request.query}")
    try:
        wf = ProjectKnowledgeWorkflow(timeout=60)
        response = await wf.run(query=request.query)
        clean_res = str(response).replace("assistant:", "").strip()
        return {"response": clean_res}
    except Exception as e:
        print(f"❌ שגיאה בשרת: {e}")
        return {"response": f"שגיאה פנימית בשרת: {str(e)}"}

@app.get("/", response_class=HTMLResponse)
async def get_index():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"קובץ index.html לא נמצא בתיקייה: {e}"

if __name__ == "__main__":
    import uvicorn
    # הרצה על פורט 8000
    uvicorn.run(app, host="127.0.0.1", port=8000)