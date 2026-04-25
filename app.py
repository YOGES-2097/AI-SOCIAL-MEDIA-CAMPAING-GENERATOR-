import streamlit as st
import sqlite3
from database import init_db, get_db_connection
from pipeline.graph_agent import run_campaign_agent
from pipeline.vector_store import seed_database
from dotenv import load_dotenv

# --- Initialization ---
load_dotenv()
init_db()       # Ensure the SQLite database exists
seed_database() # Ensure the AI Memory (ChromaDB) exists

st.set_page_config(page_title="AI Media", layout="wide", initial_sidebar_state="expanded")

# --- Session State ---
if "user_id" not in st.session_state:
    st.session_state.user_id = None
    st.session_state.username = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ==========================================
# PAGE 1: LOGIN & REGISTRATION
# ==========================================
def login_page():
    st.title("Welcome to AI Campaigns ")
    tab1, tab2 = st.tabs(["Login", "Create Account"])
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Login"):
                conn = get_db_connection()
                user = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password)).fetchone()
                conn.close()
                
                if user:
                    st.session_state.user_id = user["user_id"]
                    st.session_state.username = user["username"]
                    st.rerun()
                else:
                    st.error("Incorrect username or password.")
                    
    with tab2:
        with st.form("register_form"):
            new_user = st.text_input("Choose Username")
            new_pass = st.text_input("Choose Password", type="password")
            if st.form_submit_button("Register"):
                try:
                    conn = get_db_connection()
                    conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (new_user, new_pass))
                    conn.commit()
                    conn.close()
                    st.success("Account created! Switch to the Login tab to enter.")
                except sqlite3.IntegrityError:
                    st.error("Username already exists. Please choose another.")

# ==========================================
# PAGE 2: THE MAIN CHAT INTERFACE
# ==========================================
def main_page():
    # --- Sidebar ---
    with st.sidebar:
        st.markdown(f"### 🟢 {st.session_state.username}")
        
        if st.button("New Chat", use_container_width=True, type="primary"):
            st.session_state.chat_history = []
            st.rerun()
            
        if st.button("Logout", use_container_width=True):
            st.session_state.user_id = None
            st.session_state.username = None
            st.session_state.chat_history = []
            st.rerun()
            
        st.divider()
        st.header("Work History")
        
        # Direct Database Call for History
        conn = get_db_connection()
        history_data = conn.execute("SELECT * FROM campaign_history WHERE user_id = ? ORDER BY created_at DESC", (st.session_state.user_id,)).fetchall()
        conn.close()
        
        if not history_data:
            st.info("No campaigns generated yet.")
        
        for i, item in enumerate(history_data):
            button_label = f"{item['target_platform']} - {item['campaign_topic'][:20]}..."
            if st.button(button_label, key=f"hist_btn_{i}", use_container_width=True):
                st.session_state.chat_history = [
                    {"role": "user", "content": item['campaign_topic']},
                    {"role": "assistant", "content": item['generated_content']}
                ]
                st.rerun()

    # --- Main Chat Area ---
    st.title("AI Media Campaign Generator")
    
    if len(st.session_state.chat_history) == 0:
        st.info("Welcome! Click the 'Settings & Media' button below to attach an image, then describe your campaign to get started.")
        
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # --- Input Area ---
    with st.popover(" Select platform & Attach Media"):
        platform = st.selectbox("Target Platform", ["Instagram", "YouTube", "LinkedIn", "Twitter (X)", "Facebook"])
        uploaded_file = st.file_uploader("Upload Poster (Optional)", type=["png", "jpg", "jpeg"])

    if user_prompt := st.chat_input("Describe your campaign here..."):
        st.session_state.chat_history.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)
            
        with st.chat_message("assistant"):
            with st.spinner("Analyzing and writing..."):
                image_bytes = uploaded_file.getvalue() if uploaded_file else None
                
                try:
                    # DIRECT CALL to LangGraph Agent! No API needed.
                    final_content = run_campaign_agent(user_prompt, platform, image_bytes)
                    
                    st.markdown(final_content)
                    st.session_state.chat_history.append({"role": "assistant", "content": final_content})
                    
                    # Save to local SQLite database
                    conn = get_db_connection()
                    conn.execute("""
                        INSERT INTO campaign_history (user_id, campaign_topic, generated_content, target_platform) 
                        VALUES (?, ?, ?, ?)
                    """, (st.session_state.user_id, user_prompt, final_content, platform))
                    conn.commit()
                    conn.close()
                    
                    st.rerun()
                except Exception as e:
                    st.error(f"Generation Error: {str(e)}")

# --- Router ---
if st.session_state.user_id is None:
    login_page()
else:
    main_page()