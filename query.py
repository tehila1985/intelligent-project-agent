import os
from dotenv import load_dotenv, find_dotenv

from llama_index.core import StorageContext, load_index_from_storage, Settings
from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.llms.cohere import Cohere
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core.response_synthesizers import get_response_synthesizer
from llama_index.core.query_engine import RetrieverQueryEngine

def main():
    load_dotenv(find_dotenv())

    # 1. הגדרת המודלים ב-Settings
    Settings.embed_model = CohereEmbedding(
        api_key=os.environ["COHERE_API_KEY"],
        model_name="embed-multilingual-v3.0",
        input_type="search_query" 
    )
    
    # עדכון המודל לגרסה העדכנית של 2026
    Settings.llm = Cohere(
        api_key=os.environ["COHERE_API_KEY"],
        model="command-r-plus-08-2024" 
    )

    # 2. טעינת האינדקס מהאחסון המקומי
    print("טוען את מסד הנתונים מתיקיית storage...")
    storage_context = StorageContext.from_defaults(persist_dir="./storage")
    index = load_index_from_storage(storage_context)

    # 3. הגדרת ה-Retriever (שלב ה-Retrieve במטלה)
    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=3, # נשלוף 3 קטעים רלוונטיים
    )

    # 4. עיבוד תוצאות (שלב ה-Postprocessing במטלה)
    node_postprocessor = SimilarityPostprocessor(
        similarity_cutoff=0.2 # מסנן תוצאות שלא מספיק קשורות
    )

    # 5. יצירת התשובה (שלב ה-Synthesizing במטלה)
    response_synthesizer = get_response_synthesizer(
        response_mode="compact" # שיטה יעילה לאיחוד מידע
    )

    # 6. חיבור המנוע הסופי
    query_engine = RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=response_synthesizer,
        node_postprocessors=[node_postprocessor]
    )

    # --- הרצת שאילתה לבדיקה ---
    question = "באיזה מסד נתונים הוחלט להשתמש ולמה?"
    print(f"\nשואל את המערכת: '{question}'")
    
    response = query_engine.query(question)
    
    print("\n--- התשובה שהתקבלה ---")
    print(response)
    print("-----------------------\n")

if __name__ == "__main__":
    main()