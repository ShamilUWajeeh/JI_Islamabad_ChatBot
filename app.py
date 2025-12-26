import streamlit as st
from db import init_db

# Ensure DB exists on startup
init_db()

st.set_page_config(page_title="JI Islamabad Bot", page_icon="☪️")

st.title("Jamaat-e-Islami Islamabad ☪️")
st.subheader("Digital Knowledge Base & Election System")

st.info("Please select a module from the sidebar.")

st.markdown("""
### Available Modules:
- **🤖 Chat Interface:** For voters and public queries.
- **🔐 Admin Panel:** For the team to update Candidates & Content.
""")