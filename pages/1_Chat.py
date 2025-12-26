import streamlit as st
from db import run_query, get_data
from datetime import datetime

st.header("🤖 JI Islamabad Assistant")

# ==========================================
# 1. LOGIN SCREEN
# ==========================================
if "user_phone" not in st.session_state:
    with st.form("login"):
        st.write("Please enter your details to start:")
        name = st.text_input("Name")
        phone = st.text_input("Phone Number")
        
        if st.form_submit_button("Start"):
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
    st.subheader(f"Welcome, {st.session_state['user_name']}")

    # --- DYNAMIC WELCOME MESSAGE ---
    # Fetch from Knowledge Base
    welcome_df = get_data("SELECT content FROM knowledge_base WHERE topic = 'Welcome'")
    
    if not welcome_df.empty:
        st.info(welcome_df.iloc[0]['content'])
    else:
        st.info("Assalam-o-Alaikum! How can I help you today?")
    # -------------------------------

    # Initialize chat history if empty
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # --- DISPLAY HISTORY (Crucial Step) ---
    # This loop ensures previous messages stay on screen
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
                response = "I couldn't find an answer in the database. Please contact the main office at G-6 Markaz."

        # 3. Display & Save BOT Response
        with st.chat_message("assistant"):
            st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        run_query("INSERT INTO messages (phone_number, sender, content, timestamp) VALUES (?,?,?,?)",
                  (st.session_state['user_phone'], "bot", response, datetime.now()))