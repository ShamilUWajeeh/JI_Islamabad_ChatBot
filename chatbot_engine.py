import streamlit as st
import os
import time
import random
from google import genai
from google.genai import types

# --- CONFIGURATION ---
DATA_FILE = "data.txt" 
PRIMARY_MODEL = "gemini-2.5-pro"      

# CHANGE THIS LINE:
BACKUP_MODEL = "gemini-1.5-flash-001"   

# --- LOAD API KEY ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except (FileNotFoundError, KeyError):
    # Fallback for local testing if secrets.toml is missing
    api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("❌ API Key missing! Add it to .streamlit/secrets.toml")
    st.stop()

client = genai.Client(api_key=api_key)

# --- CACHED DATA LOADING ---
@st.cache_data(show_spinner=False)
def load_data():
    """Reads the text file once and keeps it in memory."""
    if not os.path.exists(DATA_FILE):
        return None
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return f.read()

def ask_gemini_stream(user_question):
    """
    Sends the question to Gemini with Auto-Retry and Fallback logic.
    """
    context_text = load_data()
    
    if not context_text:
        yield "⚠️ Error: Data file not found. Please check Admin Panel."
        return

    # The System Instruction tells the bot how to behave
    system_instruction = f"""
    You are the Official AI Assistant for Jamaat-e-Islami (JI) Islamabad.
    Your knowledge comes STRICTLY from the provided context below.
    
    CONTEXT DATA:
    {context_text}
    
    RULES:
    1. Answer ONLY based on the context above.
    2. If the answer is not in the text, say: "I cannot find this information in my records."
    3. Keep answers concise, polite, and professional.
    4. You can answer in English or Urdu depending on the user's question.
    """

    # --- RETRY LOGIC ---
    max_retries = 3
    current_model = PRIMARY_MODEL
    
    for attempt in range(max_retries + 1): # +1 for the backup attempt
        try:
            # Send request
            response = client.models.generate_content_stream(
                model=current_model,
                contents=user_question,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.3
                )
            )
            
            # Stream the response
            for chunk in response:
                if chunk.text:
                    yield chunk.text
            
            # If we finished successfully, stop the loop
            return

        except Exception as e:
            error_msg = str(e)
            
            # If it's a 503 (Overloaded) or 429 (Rate Limit) error
            if "503" in error_msg or "429" in error_msg:
                if attempt < max_retries - 1:
                    # Wait a bit and try again (Exponential backoff)
                    wait_time = 2 ** attempt  # 1s, 2s, 4s...
                    time.sleep(wait_time + random.uniform(0, 1))
                    continue
                
                elif current_model == PRIMARY_MODEL:
                    # If Primary failed multiple times, switch to Backup
                    current_model = BACKUP_MODEL
                    yield f"\n\n*[System: {PRIMARY_MODEL} is busy. Switching to {BACKUP_MODEL}...]*\n\n"
                    time.sleep(1)
                    continue
            
            # If it's a real error (or we ran out of retries)
            yield f"❌ Connection Error: {error_msg}"
            return