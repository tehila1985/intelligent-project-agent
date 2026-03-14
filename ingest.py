import os
from dotenv import load_dotenv, find_dotenv
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.embeddings.cohere import CohereEmbedding

def main():
    load_dotenv(find_dotenv())

    # הגדרת מודל ההטמעה עם הממדים הנכונים (1024)
    embed_model = CohereEmbedding(
        api_key=os.environ["COHERE_API_KEY"],
        model_name="embed-multilingual-v3.0",
        input_type="search_document"
    )
    Settings.embed_model = embed_model
    Settings.node_parser = MarkdownNodeParser()

    print("סורק קבצי md מתיקיית data...")
    # טעינת המסמכים
    documents = SimpleDirectoryReader(input_dir="data", recursive=True).load_data()

    print(f"נמצאו {len(documents)} מסמכים. מייצר אינדקס וקטורי...")
    index = VectorStoreIndex.from_documents(documents)

    # שמירה מקומית
    index.storage_context.persist(persist_dir="./storage")
    print("✅ האינדקס נשמר בהצלחה בתיקיית storage!")

if __name__ == "__main__":
    main()