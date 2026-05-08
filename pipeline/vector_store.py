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
        # --- Voice & Tone Rules ---
        "Brand Voice Rule: Always maintain an authoritative but approachable tone. Never use overly casual internet slang, abbreviations, or aggressive sales language.",
        "Empathy Rule: When discussing customer pain points, use empathetic language. Focus on how the product or service empowers the user rather than just listing technical features.",
        "Emoji Rule: Use emojis sparingly and only when appropriate for the platform. Never use more than three emojis per post.",
        
        # --- Compliance & Financial Rules ---
        "Pricing Rule: Never state exact prices, discounts, or dollar amounts in social media posts unless explicitly instructed. Always direct the user to 'Visit our website for pricing tiers'.",
        "ROI Rule: Never guarantee specific financial returns, conversion rates, or guaranteed success. Use phrases like 'helps optimize' or 'designed to improve'.",
        
        # --- Engagement & Conversion Rules ---
        "Call-To-Action Rule: Always conclude promotional posts with a clear Call-To-Action (CTA) instructing the user to 'Click the link in the comments' or 'Link in bio'.",
        "Competitor Rule: Never explicitly name competitor brands or speak negatively about other companies in the industry. Focus exclusively on our own unique value propositions.",
        
        # --- Platform-Specific Formatting Rules ---
        "LinkedIn Guidelines: For LinkedIn content, structure the post with a strong hook in the first line. Break up text into short, readable sentences with line breaks. Use industry-standard terminology.",
        "X (Twitter) Guidelines: For X (Twitter), keep the core message concise. Be punchy, direct, and use no more than two highly relevant hashtags.",
        "Instagram Guidelines: For Instagram, focus heavily on the aesthetic or visual value of the product being shown. Place all hashtags at the absolute bottom of the caption."
        
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

