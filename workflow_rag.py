import os
import asyncio
import json
from typing import Union

from utils import load_env, get_cohere_api_key
from llama_index.core.workflow import Workflow, step, Context, StartEvent, StopEvent, Event
from llama_index.core import StorageContext, load_index_from_storage, Settings
from llama_index.llms.cohere import Cohere
from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.core.llms import ChatMessage
from llama_index.utils.workflow import draw_all_possible_flows

# הגדרות בסיסיות
load_env()
Settings.llm = Cohere(api_key=get_cohere_api_key(), model="command-r-08-2024")
Settings.embed_model = CohereEmbedding(api_key=get_cohere_api_key(), model_name="embed-multilingual-v3.0")

# הגדרת אירועים
class RAGEvent(Event):
    query: str

class ExtractionEvent(Event):
    query: str

class RetrievedEvent(Event):
    nodes: list
    query: str

class ProjectKnowledgeWorkflow(Workflow):

    @step
    async def route(self, ctx: Context, ev: StartEvent) -> Union[RAGEvent, ExtractionEvent, StopEvent]:
        query = ev.get("query")
        if not query: return StopEvent(result="אנא הזן שאלה.")

        print(f"🚦 מנתב שאילתה: '{query}'")
        structured_keywords = ["רשימה", "כל ההחלטות", "אזהרות", "כללים", "הנחיות", "מה השתנה", "list", "rules"]
        
        if any(kw in query.lower() for kw in structured_keywords):
            return ExtractionEvent(query=query)
        else:
            return RAGEvent(query=query)

    @step
    async def query_extraction(self, ctx: Context, ev: ExtractionEvent) -> StopEvent:
        print("📊 נתיב: Structured Extraction (JSON)")
        try:
            with open("extracted_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            prompt = f"נתונים: {json.dumps(data['items'], indent=2, ensure_ascii=False)}\nשאלה: {ev.query}"
            messages = [
                ChatMessage(role="system", content="ענה על סמך ה-JSON המסופק."),
                ChatMessage(role="user", content=prompt)
            ]
            response = await Settings.llm.achat(messages)
            return StopEvent(result=str(response))
        except FileNotFoundError:
            return StopEvent(result="קובץ ה-JSON לא נמצא.")

    @step
    async def retrieve(self, ctx: Context, ev: RAGEvent) -> Union[RetrievedEvent, StopEvent]:
        print("🔍 נתיב: Semantic RAG (Vector Search)")
        storage_context = StorageContext.from_defaults(persist_dir="./storage")
        index = load_index_from_storage(storage_context)
        retriever = index.as_retriever(similarity_top_k=3)
        nodes = retriever.retrieve(ev.query)
        if not nodes: return StopEvent(result="לא נמצא מידע.")
        return RetrievedEvent(nodes=nodes, query=ev.query)

    @step
    async def synthesize(self, ctx: Context, ev: RetrievedEvent) -> StopEvent:
        context_str = "\n\n".join([n.get_content() for n in ev.nodes])
        prompt = f"הקשר: {context_str}\nשאלה: {ev.query}"
        messages = [
            ChatMessage(role="system", content="ענה על סמך ההקשר בלבד."),
            ChatMessage(role="user", content=prompt)
        ]
        response = await Settings.llm.achat(messages)
        return StopEvent(result=str(response))

async def main():
    wf = ProjectKnowledgeWorkflow(timeout=60)
    
  
    try:
        from llama_index.utils.workflow import draw_all_possible_flows
        draw_all_possible_flows(wf, filename="workflow_viz_final.html")
        print("🎨 תרשים ה-Workflow נוצר בהצלחה!")
    except Exception as e:
        print(f"⚠️ לא ניתן היה לצייר את התרשים: {e}")
    
  
    print("\n--- בדיקה: שליפה מובנית ---")
    res = await wf.run(query="תן לי רשימה של כל האזהרות")
    print(f"תשובה: {res}")

if __name__ == "__main__":
    asyncio.run(main())