# Spark AI Media Campaign Generator 🚀

Spark AI is a full-stack marketing tool built with Streamlit and LangGraph. It analyzes user text and uploaded images to generate highly engaging, brand-aligned social media campaigns.

## 🌟 Key Features
* **Multimodal Vision:** Uses Google Gemini to analyze uploaded product posters and extract key marketing details.
* **RAG Brand Memory:** Utilizes ChromaDB to permanently store and strictly enforce company brand guidelines (tone, pricing rules, etc.) during generation.
* **Local History:** Fully integrated SQLite database to save, manage, and instantly reload past campaigns.
* **Agentic Workflow:** Powered by LangGraph to orchestrate memory retrieval, image analysis, and text generation in a seamless pipeline.

## 🛠️ Tech Stack
* **Frontend:** Streamlit
* **AI Orchestration:** LangGraph, LangChain
* **Models:** Gemini 2.5 Flash, HuggingFace Embeddings (`all-MiniLM-L6-v2`)
* **Databases:** ChromaDB (Vector Store), SQLite (Relational)

## 🚀 How to Run Locally
1. Clone this repository.
2. Install the requirements: `pip install -r requirements.txt`
3. Add your `GOOGLE_API_KEY` and `HF_TOKEN` to a `.env` file.
4. Run the app: `streamlit run app.py`