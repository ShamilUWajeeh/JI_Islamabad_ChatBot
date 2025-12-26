import streamlit as st
from db import init_db

# 1. Initialize the Database immediately when the app starts
init_db()

# 2. Configure the page settings
st.set_page_config(
    page_title="JI Islamabad Bot", 
    page_icon="☪️",
    initial_sidebar_state="expanded" # Keeps the sidebar open by default
)

# 3. Main Header and Title
st.title("Jamaat-e-Islami Islamabad ☪️")
st.subheader("Digital Knowledge Base & Election System")

# 4. Navigation Section
st.markdown("---")
st.info("👇 **Select a Dashboard:**")

# Create two columns for big buttons
col1, col2 = st.columns(2)

with col1:
    # Points to "pages/1_Chat.py" (Renamed file)
    st.page_link("pages/1_Chat.py", label="Open Chatbot", icon="🤖")

with col2:
    # Points to "pages/2_Admin.py" (Renamed file)
    st.page_link("pages/2_Admin.py", label="Admin Panel", icon="🔐")