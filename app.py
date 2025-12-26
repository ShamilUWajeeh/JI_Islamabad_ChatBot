import streamlit as st
from db import init_db

# Ensure DB exists
init_db()

# 1. Configure the page to keep the sidebar expanded by default
st.set_page_config(
    page_title="JI Islamabad Bot", 
    page_icon="☪️",
    initial_sidebar_state="expanded"  # <--- THIS FORCES THE SIDEBAR OPEN
)

st.title("Jamaat-e-Islami Islamabad ☪️")
st.subheader("Digital Knowledge Base & Election System")

st.markdown("---")
st.info("👇 **Select a Dashboard:**")

# 2. Add Big Clickable Buttons (No arrow needed!)
col1, col2 = st.columns(2)

with col1:
    st.page_link("pages/1_🤖_Chat.py", label="🤖 Open Chatbot", icon="💬")

with col2:
    st.page_link("pages/2_🔐_Admin.py", label="🔐 Admin Panel", icon="⚙️")