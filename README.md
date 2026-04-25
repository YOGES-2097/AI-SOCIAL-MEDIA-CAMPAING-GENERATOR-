## Abstract
The **AI Media Campaign Generator** is a full-stack, AI-powered application designed to automate the creation of platform-specific social media marketing campaigns. Leveraging an agentic workflow orchestrated by LangGraph, the system analyzes user-provided context and multimodal inputs (images/posters) using Google's Gemini 2.5 Flash model. To ensure strict adherence to corporate brand guidelines, a Retrieval-Augmented Generation (RAG) architecture is implemented utilizing ChromaDB as a vector store. The application is packaged as a modular monolith using Streamlit and SQLite, enabling a seamless, serverless deployment to the Streamlit Community Cloud.

---

## 1. Introduction & "Why This Project?"

### The Problem
In modern digital marketing, creating rapid, high-quality content across multiple platforms (Instagram, LinkedIn, X, Facebook) is essential. However, marketing teams face several bottlenecks:
1. **Brand Inconsistency:** Standard Large Language Models (LLMs) often hallucinate or deviate from specific company guidelines (e.g., using prohibited slang or exposing confidential pricing).
2. **Multimodal Disconnect:** Marketers often have a visual asset (a poster or product image) but struggle to quickly draft engaging copy that perfectly matches the visual context.
3. **Workflow Fragmentation:** Generating a post usually requires bouncing between a database, an image processing tool, and an AI chat interface.

### The Spark AI Solution (Why this project?)
This project was built to solve these exact bottlenecks by creating an **Autonomous Marketing Agent**. Instead of just wrapping an API in a UI, Spark AI uses **LangGraph** to create a thinking pipeline. It intercepts the user's request, searches its own "memory" (ChromaDB) for brand rules, physically "looks" at uploaded images to understand context, and synthesizes all this data into a ready-to-publish campaign. It acts not just as a text generator, but as a brand-safe marketing assistant.

---

## 2. Approaching Method (System Architecture)

The system utilizes an **Agentic Workflow** built on LangGraph, ensuring that tasks are executed in a deterministic, reliable sequence rather than relying on a single, massive LLM prompt.

### 🧠 The LangGraph Pipeline
1. **State Initialization:** The user inputs a prompt, selects a platform, and optionally uploads a poster.
2. **Node 1: Fetch Memory (RAG):** The system takes the user's prompt and queries a local **ChromaDB** vector database using HuggingFace embeddings (`all-MiniLM-L6-v2`). It retrieves the most relevant corporate brand rules (e.g., "Never mention exact prices").
3. **Node 2: Vision Processing:** If an image is uploaded, it is compressed using **Pillow** to save API tokens, converted to base64, and sent to **Gemini 2.5 Flash** for multimodal analysis. The AI extracts text, mood, and target demographic data from the image.
4. **Node 3: Content Generation:** A LangChain prompt template combines the user's initial prompt, the retrieved brand rules, and the visual description, instructing the LLM to generate the final campaign optimized for the chosen social media platform.
5. **Database Storage:** The final output is saved to a local **SQLite** database, allowing users to browse their generation history seamlessly.

---

## 3. Project Structure

The repository is structured as a **Modular Monolith**, separating the UI from the AI logic and database management.

```text
SOCIAL_MEDIA_CAMPAIGN/
│
├── app.py                # Main Streamlit UI, Auth Router, and Session State
├── database.py           # SQLite3 initialization, User Auth, and History tables
├── requirements.txt      # Production dependencies
├── .env                  # Environment variables (Ignored in Git)
├── .gitignore            # Git ignore rules
│
├── ai_media.db           # Local SQLite Database (Generated dynamically)
├── chroma_db/            # Local Vector Store for Brand Rules (Generated dynamically)
│
└── pipeline/             # AI Core Logic & LangGraph Agents
    ├── chains.py         # LangChain prompt templates and LLM invocation
    ├── graph_agent.py    # LangGraph state machine definition
    ├── image.py          # Pillow compression & Gemini Vision integration
    └── vector_store.py   # HuggingFace embeddings & ChromaDB operations
```
4. Required Libraries (Tech Stack)
The project relies on a modern AI and web framework stack. See requirements.txt for exact versions.

Frontend & Web Server: * streamlit: Powers the interactive web interface and application state.

AI Orchestration & Agents: * langgraph: Manages the stateful workflow of the AI agent.

langchain: Provides the prompt templating and LLM chaining tools.

Large Language Models (LLMs): * langchain-google-genai: Connects to Google's Gemini 2.5 Flash for text and vision.

Memory & Retrieval Augmented Generation (RAG):

langchain-chroma: The vector database used for storing brand guidelines.

langchain-huggingface: Generates vector embeddings using local models.

sentence-transformers: Required backend for HuggingFace embeddings.

Relational Database: SQLite3

ai_media.db: Local SQLite Database (Generated dynamically)

Data Processing:

Pillow: Used for local image compression to optimize API payload limits.

python-dotenv: Manages secure environment variables locally.

Here is a highly elaborated, professional README.md that is structured to serve both as a complete GitHub repository guide and a comprehensive project report for your internship submission.

You can copy and paste this entire block directly into your README.md file on GitHub!



5. Setup & Local Installation
To run this application locally on your machine, follow these steps:

Prerequisites
Python 3.10 or higher.

A Google Gemini API Key.

A Hugging Face Access Token.

Installation Steps
Clone the repository:https://github.com/YOGES-2097/AI-SOCIAL-MEDIA-CAMPAING-GENERATOR-.git

Create a virtual environment:
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

Install the required libraries: pip install -r requirements.txt

Set up Environment Variables:
Create a .env file in the root directory and add your API keys:

Code snippet
GOOGLE_API_KEY="your_google_api_key_here"
HF_TOKEN="your_huggingface_token_here"

# LangSmith Tracing for Analytics
LANGCHAIN_TRACING="true"
LANGCHAIN_ENDPOINT="[https://api.smith.langchain.com](https://api.smith.langchain.com)"
LANGCHAIN_API_KEY="your_langsmith_key_here"
LANGCHAIN_PROJECT="Production_Name"

Run the Application: streamlit run app.py

6. Future Enhancements
OAuth Social Integration: Implementing APIs to allow one-click publishing directly to LinkedIn and X (Twitter) from the Streamlit UI.

Text-to-Image Generation: Integrating Stable Diffusion to auto-generate poster images if the user does not supply visual context.

Advanced Analytics: Expanding LangSmith tracing to provide a user-facing dashboard for token usage and campaign success rates.
