import streamlit as st
import time
from chatbot_engine import ask_gemini_stream

# --- PAGE CONFIG ---
st.set_page_config(page_title="JI AI Assistant", page_icon="💬")

# --- CSS STYLING ---
st.markdown("""
<style>
    .chat-message {
        padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex;
    }
    .chat-message.user {
        background-color: #f0f2f6; border: 1px solid #e0e0e0;
    }
    .chat-message.bot {
        background-color: #e8f5e9; border: 1px solid #c8e6c9;
    }
    .chat-message .avatar {
        width: 40px; height: 40px; border-radius: 50%; object-fit: cover; margin-right: 1rem;
    }
    .chat-message .message {
        width: 100%; font-size: 16px; line-height: 1.5;
    }
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR SETTINGS ---
with st.sidebar:
    st.image("logo.png", width=100) if "logo.png" in [f.name for f in Path(".").iterdir()] else st.write("🤖")
    st.title("Settings")
    
    # We keep this for user preference, even if the bot is smart enough to detect language
    language = st.radio("Response Language:", ["Auto-Detect", "Urdu", "English"])
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("🔒 **Admin Access**")
    if st.button("Go to Admin Panel"):
        st.switch_page("pages/2_Admin_Panel.py")

# --- INITIALIZE CHAT HISTORY ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Assalam-o-Alaikum! I am the JI Islamabad AI Assistant. How can I help you today?"}
    ]

# --- DISPLAY CHAT HISTORY ---
st.title("💬 JI Islamabad Digital Assistant")

for message in st.session_state.messages:
    role_class = "user" if message["role"] == "user" else "bot"
    avatar = "👤" if message["role"] == "user" else "🤖"
    
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# --- CHAT INPUT & LOGIC ---
if prompt := st.chat_input("Ask about UCs, Wards, or Organization..."):
    # 1. Add User Message to History
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # 2. Generate Assistant Response
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Append language instruction if specific language is chosen
        final_prompt = prompt
        if language == "Urdu":
            final_prompt += " (Please answer in Urdu)"
        elif language == "English":
            final_prompt += " (Please answer in English)"

        # --- THE FIX IS HERE: CALLING THE FUNCTION CORRECTLY ---
        try:
            # We now only pass the prompt. The engine handles the API key and context.
            stream_generator = ask_gemini_stream(final_prompt)
            
            for chunk in stream_generator:
                full_response += chunk
                message_placeholder.markdown(full_response + "▌")
                
            message_placeholder.markdown(full_response)
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
            full_response = "I encountered a connection error. Please try again."

    # 3. Save Assistant Message to History
    st.session_state.messages.append({"role": "assistant", "content": full_response})