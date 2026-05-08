import streamlit as st
import chromadb
import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

# 1. Setup the Embedding Model
# We use a free, local HuggingFace model
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 2. Define where the database will be saved on your hard drive
DB_DIR = os.path.join(os.path.dirname(__file__), "..", "chroma_db")

@st.cache_resource
def get_vector_store():
    """Connects to the Chroma database."""
    # Clears any ghost connections to prevent the tenant error
    chromadb.api.client.SharedSystemClient.clear_system_cache()
    
    return Chroma(persist_directory=DB_DIR, embedding_function=embeddings, collection_name="brand_guidelines")

def seed_database():
    """Adds your company's secret brand rules to the AI's permanent memory."""
    db = get_vector_store()
    
    # Check if we already have data to avoid duplicates
    if db._collection.count() > 0:
        print("Database already has memory!")
        return
        
    print(" Seeding ChromaDB with Brand Guidelines...")
    
    # Here are the strict rules the AI MUST follow
    guidelines = [
        "Brand Voice Rule: We are highly energetic but strictly professional. Never use slang words like 'bro', 'lit', or 'bet'.",
        "Pricing Rule: Never mention exact prices or dollar amounts in social media posts. Always direct users to 'Click the link in bio to see our plans'.",
        
    ]
    
    docs = [Document(page_content=text) for text in guidelines]
    db.add_documents(docs)
    print(" Memory successfully created!")

def retrieve_guidelines(query: str, k: int = 2) -> str:
    """Searches the database for the 2 most relevant rules based on the user's prompt."""
    db = get_vector_store()
    results = db.similarity_search(query, k=k)
    
    if not results:
        return "No specific brand guidelines found."
        
    # Combine the retrieved rules into a single string
    context = "\n".join([doc.page_content for doc in results])
    return context

