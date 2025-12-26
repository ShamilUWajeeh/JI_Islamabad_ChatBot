import streamlit as st
from db import run_query, get_data
from datetime import datetime
import base64
import os

# --- CUSTOM ANIMATED HEADER ---
# 1. CSS for the header animation & layout
st.markdown("""
<style>
    @keyframes pulse-header {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.02); opacity: 0.95; }
        100% { transform: scale(1); opacity: 1; }
    }
    .chat-header-container {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 15px;
        /* Subtle JI Gradient Background */
        background: linear-gradient(135deg, rgba(30, 143, 78, 0.08) 0%, rgba(46, 155, 203, 0.08) 100%);
        border-radius: 12px;
        margin-bottom: 25px;
        border: 1px solid rgba(30, 143, 78, 0.2);
        /* THE CONTINUOUS ANIMATION */
        animation: pulse-header 4s ease-in-out infinite;
    }
    .chat-header-logo {
        width: 50px;
        height: auto;
        margin-right: 15px;
    }
    .chat-header-text {
        font-family: sans-serif;
        font-size: 26px;
        font-weight: 700;
        color: #111111;
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)

# 2. Helper function to load local image for HTML
def get_img_tag(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            data = f.read()
        encoded = base64.b64encode(data).decode()
        return f'<img src="data:image/png;base64,{encoded}" class="chat-header-logo">'
    else:
        # Fallback logo if local file isn't found
        return '<img src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png" class="chat-header-logo">'

# 3. Display the combined, animated header
st.markdown(f"""
    <div class="chat-header-container">
        {get_img_tag("logo.png")}
        <h1 class="chat-header-text">Jamaat-e-Islami Islamabad</h1>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 1. LOGIN SCREEN
# ==========================================
if "user_phone" not in st.session_state:
    with st.form("login"):
        st.write("Please enter your details to start:")
        name = st.text_input("Name")
        phone = st.text_input("Phone Number")
        
        if st.form_submit_button("Start Chat", use_container_width=True):
            if phone:
                # Save User to DB
                run_query("INSERT OR IGNORE INTO contacts (phone_number, name, last_active) VALUES (?,?,?)", 
                          (phone, name, datetime.now()))
                
                # Save Session State
                st.session_state['user_phone'] = phone
                st.session_state['user_name'] = name
                st.rerun()

# ==========================================
# 2. CHAT INTERFACE
# ==========================================
else:
    # --- DYNAMIC WELCOME MESSAGE ---
    # Fetch from Knowledge Base
    welcome_df = get_data("SELECT content FROM knowledge_base WHERE topic = 'Welcome'")
    
    if not welcome_df.empty:
        st.info(welcome_df.iloc[0]['content'])
    else:
        st.info(f"Assalam-o-Alaikum, {st.session_state['user_name']}! How can I help you today?")
    # -------------------------------

    # Initialize chat history if empty
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # --- DISPLAY HISTORY ---
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # --- CHAT INPUT & LOGIC ---
    if prompt := st.chat_input("Ask about candidates or JI vision..."):
        
        # 1. Display & Save USER Message
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        run_query("INSERT INTO messages (phone_number, sender, content, timestamp) VALUES (?,?,?,?)",
                  (st.session_state['user_phone'], "user", prompt, datetime.now()))

        # 2. Determine BOT Response
        response = ""
        
        # A. Check if asking for Candidates (e.g., "UC-10")
        if "UC" in prompt.upper():
            # Extract number (simple logic: grab 2 chars after 'UC')
            try:
                uc_search = prompt.upper().split("UC")[-1].strip()[:2]
                # Remove dashes if any
                uc_search = uc_search.replace("-", "").strip()
                
                df = get_data(f"SELECT * FROM candidates WHERE uc_number LIKE '%{uc_search}%'")
                
                if not df.empty:
                    response = f"**Found candidates for UC-{uc_search}:**\n\n"
                    for i, row in df.iterrows():
                        response += f"- 👤 **{row['candidate_name']}** ({row['role']})\n  📞 {row['phone']}\n\n"
                else:
                    response = f"I could not find data for UC-{uc_search} yet. Please check the number."
            except:
                response = "Please specify the UC number clearly (e.g., 'Who is in UC-10?')."
        
        # B. Check Knowledge Base (General Questions)
        else:
            # Simple keyword search in Topic OR Content
            df_kb = get_data(f"SELECT * FROM knowledge_base WHERE content LIKE '%{prompt}%' OR topic LIKE '%{prompt}%'")
            
            if not df_kb.empty:
                response = df_kb.iloc[0]['content']
            else:
                # Fallback response
                response = "I couldn't find an answer in the database. Please contact the main office at G-6 Markaz."

        # 3. Display & Save BOT Response
        with st.chat_message("assistant"):
            st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        run_query("INSERT INTO messages (phone_number, sender, content, timestamp) VALUES (?,?,?,?)",
                  (st.session_state['user_phone'], "bot", response, datetime.now()))