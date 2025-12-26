import streamlit as st
import pandas as pd
import sqlite3
from db import get_data, run_query, DB_NAME

st.set_page_config(layout="wide")
st.header("🔐 Admin Control Panel")

password = st.sidebar.text_input("Password", type="password")

if password == "Wajeeh@1408":  # CHANGE THIS PASSWORD
    
    tab1, tab2, tab3 = st.tabs(["📚 Knowledge Base", "👥 Candidates", "💬 Chat Logs"])

    # --- TAB 1: KNOWLEDGE BASE (Edit Vision, etc) ---
    with tab1:
        st.subheader("Manage Website Content")
        st.info("Edit your Vision, Welcome Message, and Contact Info here.")
        
        df_kb = get_data("SELECT * FROM knowledge_base")
        edited_kb = st.data_editor(df_kb, num_rows="dynamic", key="kb_edit", use_container_width=True)

        if st.button("💾 Save Content Changes"):
            conn = sqlite3.connect(DB_NAME)
            run_query("DELETE FROM knowledge_base") # Clear old
            # Save new (excluding ID column to let DB regen it)
            if "id" in edited_kb.columns:
                edited_kb = edited_kb.drop(columns=["id"])
            edited_kb.to_sql("knowledge_base", conn, if_exists="append", index=False)
            conn.close()
            st.success("Updated!")
            st.rerun()

    # --- TAB 2: CANDIDATES ---
    with tab2:
        st.subheader("Manage Candidates")
        df_cand = get_data("SELECT * FROM candidates")
        edited_cand = st.data_editor(df_cand, num_rows="dynamic", key="cand_edit", use_container_width=True)

        if st.button("💾 Save Candidate List"):
            conn = sqlite3.connect(DB_NAME)
            run_query("DELETE FROM candidates")
            if "id" in edited_cand.columns:
                edited_cand = edited_cand.drop(columns=["id"])
            edited_cand.to_sql("candidates", conn, if_exists="append", index=False)
            conn.close()
            st.success("Updated!")
            st.rerun()

    # --- TAB 3: LOGS ---
    with tab3:
        st.subheader("Live Chats")
        st.dataframe(get_data("SELECT * FROM messages ORDER BY timestamp DESC LIMIT 50"), use_container_width=True)

else:
    st.warning("Please enter admin password.")