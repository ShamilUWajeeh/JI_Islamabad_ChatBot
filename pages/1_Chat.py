import streamlit as st
import time
import os
from chatbot_engine import ask_gemini_stream

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="JI Assistant",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CUSTOM CSS (Animation & Styling) ---
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding-top: 1rem; padding-bottom: 5rem;}
    
    /* ANIMATION: Pulse Effect for the Logo */
    @keyframes pulse {
        0% { transform: scale(1); filter: drop-shadow(0 0 0 rgba(0,128,0,0.4)); }
        50% { transform: scale(1.1); filter: drop-shadow(0 0 10px rgba(0,128,0,0.6)); }
        100% { transform: scale(1); filter: drop-shadow(0 0 0 rgba(0,128,0,0.4)); }
    }
    
    /* Apply animation to the specific logo image */
    [data-testid="stImage"] img[src*="logo.png"] {
        animation: pulse 2s infinite ease-in-out;
    }

    /* Chat Input Styling */
    .stChatInput {border-radius: 20px;}
    
    /* Urdu Font */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu:wght@400;700&display=swap');
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    col1, col2 = st.columns([1, 3])
    with col1:
        try: st.image("logo.png", width=70)
        except: st.write("📷")
    with col2:
        st.markdown("### JI Islamabad\n**Digital Wing**")
    
    st.divider()
    
    # Language Toggle
    st.markdown("#### 🌐 Language / زبان")
    language_choice = st.radio(
        "Language", ["English", "Urdu (اردو)"], 
        horizontal=True, label_visibility="collapsed"
    )

    st.markdown("---")
    if st.button("🗑️ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- 4. TOP HEADER SECTION ---
# This section puts the animated logo and title at the very top
top_col1, top_col2 = st.columns([1, 8])

with top_col1:
    # This image will be animated by the CSS above because it's named 'logo.png'
    try:
        st.image("logo.png", width=90)
    except:
        st.write("📷")

with top_col2:
    if language_choice == "English":
        st.markdown("## **Ask JI Islamabad**")
        st.caption("Official AI Bot for Jamaat-e-Islami Islamabad")
    else:
        st.markdown("## **انتخابی حلقہ جات اسسٹنٹ**", unsafe_allow_html=True)
        st.caption("جماعت اسلامی اسلام آباد کا آفیشل AI بوٹ")

# Optional Banner Image (If you have one)
if os.path.exists("banner.jpg"):
    st.image("banner.jpg", use_column_width=True)

st.divider()

# --- 5. API KEY CHECK ---
try: api_key = st.secrets.get("GEMINI_API_KEY")
except FileNotFoundError: api_key = None

if not api_key:
    st.warning("⚠️ Access Key Required")
    st.stop()

# --- 6. INITIALIZE STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 7. UI TEXT DICTIONARY ---
ui_text = {
    "English": {
        "greeting": "As-salamu Alaykum",
        "subtext": "How can I help you with JI Islamabad today?",
        "btn_uc": "📍 UC Areas",
        "btn_lead": "👤 Leadership",
        "btn_office": "📞 Offices",
        "btn_manif": "🗳️ Manifesto",
        "q_uc": "List all UCs and their areas.",
        "q_lead": "Who is the District Ameer?",
        "q_office": "Where is the main office?",
        "q_manif": "What is the key manifesto?",
        "input_placeholder": "Ask a question..."
    },
    "Urdu (اردو)": {
        "greeting": "السلام علیکم",
        "subtext": "جماعت اسلامی اسلام آباد کے حوالے سے میں آپ کی کیا مدد کر سکتا ہوں؟",
        "btn_uc": "📍 حلقہ جات",
        "btn_lead": "👤 قیادت",
        "btn_office": "📞 دفاتر",
        "btn_manif": "🗳️ منشور",
        "q_uc": "تمام یوسیز اور ان کے علاقوں کی فہرست دیں۔",
        "q_lead": "ضلعی امیر کون ہیں؟",
        "q_office": "مرکزی دفتر کہاں ہے؟",
        "q_manif": "جماعت کا اہم منشور کیا ہے؟",
        "input_placeholder": "اپنا سوال یہاں لکھیں..."
    }
}
current_text = ui_text[language_choice]

# --- 8. WELCOME SCREEN ---
if len(st.session_state.messages) == 0:
    st.markdown(f"<h3 style='text-align: center; color: #008000; font-family: Noto Nastaliq Urdu;'>{current_text['greeting']}</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: gray; font-family: Noto Nastaliq Urdu;'>{current_text['subtext']}</p>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    user_query = None
    
    if col1.button(current_text["btn_uc"], use_container_width=True): user_query = current_text["q_uc"]
    if col2.button(current_text["btn_lead"], use_container_width=True): user_query = current_text["q_lead"]
    if col3.button(current_text["btn_office"], use_container_width=True): user_query = current_text["q_office"]
    if col4.button(current_text["btn_manif"], use_container_width=True): user_query = current_text["q_manif"]
else:
    user_query = None

# --- 9. CHAT HISTORY ---
for message in st.session_state.messages:
    avatar = "logo.png" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# --- 10. HANDLE INPUT ---
if prompt := st.chat_input(current_text["input_placeholder"]) or user_query:
    if user_query: prompt = user_query

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="logo.png"):
        response_placeholder = st.empty()
        full_response = ""
        stream_generator = ask_gemini_stream(api_key, prompt, language_choice)
        
        for chunk in stream_generator:
            full_response += chunk
            response_placeholder.markdown(full_response + "▌")
            
        response_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    if user_query: st.rerun()