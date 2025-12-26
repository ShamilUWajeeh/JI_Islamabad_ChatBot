import streamlit as st
import requests
from streamlit_lottie import st_lottie
from db import init_db
import os

# --- PAGE SETUP ---
st.set_page_config(
    page_title="JI Islamabad Portal",
    page_icon="☪️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Ensure DB is ready
init_db()

# --- ASSETS & STYLING ---

# 1. Load Lottie Animation (Helper Function)
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load a "Community/Team" animation (You can change this URL)
lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_bo8vqwyw.json")

# 2. Custom CSS for "Modern Cards" Look
st.markdown("""
<style>
    /* Main Background adjustments */
    .stApp {
        background-color: #ffffff;
    }
    
    /* Header Styling */
    h1 {
        color: #009933 !important; /* JI Green */
        font-weight: 700 !important;
    }
    
    /* Custom Card Styling for Buttons */
    div.stButton > button {
        width: 100%;
        height: 80px;
        background-color: white;
        color: #31333F;
        border: 2px solid #009933;
        border-radius: 12px;
        font-size: 20px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Hover Effect */
    div.stButton > button:hover {
        background-color: #009933;
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        border-color: #009933;
    }
    
    /* Logo Styling */
    .logo-img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 150px;
    }
</style>
""", unsafe_allow_html=True)

# --- MAIN INTERFACE ---

# 1. Logo Section (Optional: Checks if file exists)
if os.path.exists("logo.png"):
    st.image("logo.png", width=120)

st.title("Jamaat-e-Islami Islamabad")
st.markdown("**Digital Knowledge Base & Election Management System**")

st.markdown("---")

# 2. Hero Section (Animation + Intro)
col_anim, col_text = st.columns([1, 1.5])

with col_anim:
    if lottie_coding:
        st_lottie(lottie_coding, height=200, key="coding")
    else:
        st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=150)

with col_text:
    st.info("""
    **Assalam-o-Alaikum!**
    
    Welcome to the official digital portal. 
    Select a dashboard below to manage elections or assist voters.
    """)

st.write("") # Spacer

# 3. Modern Navigation Cards
col1, col2 = st.columns(2)

with col1:
    # We use a button that triggers a switch
    if st.button("🤖 Public Chatbot"):
        st.switch_page("pages/1_Chat.py")

with col2:
    if st.button("🔐 Admin Panel"):
        st.switch_page("pages/2_Admin.py")

st.markdown("---")
st.caption("© 2025 Jamaat-e-Islami Islamabad | Developed for Digital Wing")