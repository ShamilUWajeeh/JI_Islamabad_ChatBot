import streamlit as st
from db import run_query, get_data
from datetime import datetime

st.header("🤖 JI Islamabad Assistant")

# 1. Simple Login
if "user_phone" not in st.session_state:
    with st.form("login"):
        st.write("Please enter your details to start:")
        name = st.text_input("Name")
        phone = st.text_input("Phone Number")
        if st.form_submit_button("Start"):
            if phone:
                # Save User
                run_query("INSERT OR IGNORE INTO contacts (phone_number, name, last_active) VALUES (?,?,?)", 
                          (phone, name, datetime.now()))
                st.session_state['user_phone'] = phone
                st.session_state['user_name'] = name
                st.rerun()

# 2. Chat Interface
else:
    st.write(f"Logged in as: **{st.session_state['user_name']}**")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask about candidates or JI vision..."):
        
        # A. User Msg
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        run_query("INSERT INTO messages (phone_number, sender, content, timestamp) VALUES (?,?,?,?)",
                  (st.session_state['user_phone'], "user", prompt, datetime.now()))

        # B. Logic
        response = ""
        
        # Check Candidates
        if "UC" in prompt.upper():
            uc_search = prompt.split("UC")[-1].strip()[:2] # Grab number
            df = get_data(f"SELECT * FROM candidates WHERE uc_number LIKE '%{uc_search}%'")
            if not df.empty:
                response = "Found these candidates:\n"
                for i, row in df.iterrows():
                    response += f"- **{row['candidate_name']}** ({row['role']}) - 📞 {row['phone']}\n"
            else:
                response = "No data found for this UC yet."
        
        # Check Knowledge Base (Simple Keyword Search)
        else:
            df_kb = get_data(f"SELECT * FROM knowledge_base WHERE content LIKE '%{prompt}%' OR topic LIKE '%{prompt}%'")
            if not df_kb.empty:
                response = df_kb.iloc[0]['content']
            else:
                response = "I couldn't find an answer in the database. Please contact the main office."

        # C. Bot Msg
        with st.chat_message("assistant"):
            st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        run_query("INSERT INTO messages (phone_number, sender, content, timestamp) VALUES (?,?,?,?)",
                  (st.session_state['user_phone'], "bot", response, datetime.now()))