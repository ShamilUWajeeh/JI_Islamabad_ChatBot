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

def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Load Animation
lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_bo8vqwyw.json")

# Custom CSS for "Modern Cards" Look
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    h1 { color: #009933 !important; font-weight: 700 !important; }
    
    /* Button Styling */
    div.stButton > button {
        width: 100%;
        height: 60px; /* Adjusted height */
        background-color: white;
        color: #31333F;
        border: 2px solid #009933;
        border-radius: 12px;
        font-size: 18px; /* Adjusted font size */
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    div.stButton > button:hover {
        background-color: #009933;
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        border-color: #009933;
    }
    
    img { border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# --- MAIN INTERFACE ---

# 1. Logo
if os.path.exists("logo.png"):
    col_logo1, col_logo2, col_logo3 = st.columns([1,1,1])
    with col_logo2:
        st.image("logo.png", use_container_width=True)

st.title("Jamaat-e-Islami Islamabad")
st.markdown("**Digital Knowledge Base & Election Management System**")
st.markdown("---")

# 2. Hero Section
col_anim, col_text = st.columns([1, 1.5])

with col_anim:
    if lottie_coding:
        st_lottie(lottie_coding, height=200, key="unique_animation_key")
    else:
        st.image("https://cdn-icons-png.flaticon.com/512/10605/10605943.png", width=150)

with col_text:
    st.info("""
    **Assalam-o-Alaikum!**
    
    Welcome to the official digital portal. 
    Select a dashboard below to manage elections or assist voters.
    """)

st.write("") 

# 3. Navigation Grid (CLEAN BUTTONS)
st.subheader("Select a Module")
col1, col2 = st.columns(2)

# --- CARD 1: PUBLIC CHAT ---
with col1:
    if os.path.exists("chat_icon.png"):
        st.image("chat_icon.png", width=100)
    else:
        st.image("https://cdn-icons-png.flaticon.com/512/8943/8943377.png", width=100)
        
    # REMOVED EMOJI HERE 👇
    if st.button("Open Public Chat", key="btn_chat", use_container_width=True):
        st.switch_page("pages/1_Chat.py")

# --- CARD 2: ADMIN PANEL ---
with col2:
    if os.path.exists("admin_icon.png"):
        st.image("admin_icon.png", width=100)
    else:
        st.image("https://cdn-icons-png.flaticon.com/512/2942/2942813.png", width=100)
        
    # REMOVED EMOJI HERE 👇
    if st.button("Open Admin Panel", key="btn_admin", use_container_width=True):
        st.switch_page("pages/2_Admin.py")

st.markdown("---")
st.caption("© 2025 Jamaat-e-Islami Islamabad | Developed for Digital Wing")