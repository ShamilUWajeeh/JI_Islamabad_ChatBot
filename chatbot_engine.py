import os
import toml
from google import genai
from google.genai import types

# --- CONFIGURATION ---
# Ensure this matches your actual file name
DATA_FILE = "data.txt" 

# Use the model available to your account
MODEL_ID = "gemini-2.5-pro" 

def get_client(api_key):
    return genai.Client(api_key=api_key)

# 🟢 THIS WAS MISSING
def load_data():
    if not os.path.exists(DATA_FILE):
        return None
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

def ask_gemini_stream(api_key, user_query, target_language="English"):
    # 1. Load Data
    context_data = load_data()
    
    if not context_data:
        yield "⚠️ Error: Data file not found. Please check Admin Panel."
        return

    client = get_client(api_key)

    # 2. Define Rules
    system_instruction = f"""
    You are the Official AI Assistant for Jamaat-e-Islami (Islamabad).
    
    YOUR KNOWLEDGE BASE:
    1. Election Constituencies (UCs, Wards, Census Blocks).
    2. Organization Details.
    
    STRICT LANGUAGE SETTING:
    The user has chosen: **{target_language}**.
    
    RULES:
    1. If English: Answer in English. Transliterate Urdu names (e.g., "Gokina" not "گوکینہ").
    2. If Urdu: Answer in Urdu (Nastaliq style).
    3. Be accurate with Ward numbers and Census blocks.
    """

    try:
        # 3. Generate Stream
        response = client.models.generate_content_stream(
            model=MODEL_ID,
            contents=[
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(text=f"OFFICIAL RECORDS:\n{context_data}"),
                        types.Part.from_text(text=f"USER QUERY:\n{user_query}")
                    ]
                )
            ],
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.1,
                max_output_tokens=2048
            )
        )
        
        # 4. Yield Chunks
        for chunk in response:
            if chunk.text:
                yield chunk.text

    except Exception as e:
        yield f"❌ Connection Error: {str(e)}"