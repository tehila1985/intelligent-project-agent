import os
from dotenv import load_dotenv, find_dotenv

def load_env():
    _ = load_dotenv(find_dotenv())

def get_api_key(provider):
    load_env()
    return os.getenv(f"{provider}_API_KEY")

def get_cohere_api_key():
    load_env()
    return os.getenv("COHERE_API_KEY")