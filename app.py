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

# --- OFFICIAL JI COLOR THEME CSS ---
st.markdown("""
<style>
    /* 1. MAIN BACKGROUND */
    .stApp {
        background-color: #FFFFFF;
    }
    
    /* 2. HEADER TYPOGRAPHY (Deep Black) */
    h1 {
        color: #111111 !important;
        font-weight: 700 !important;
        padding-bottom: 10px;
        /* Subtle Gradient Border at bottom of header */
        border-bottom: 2px solid;
        border-image: linear-gradient(135deg, #1E8F4E 0%, #2E9BCB 100%) 1;
    }
    
    p, .stMarkdown {
        color: #4A4A4A; /* Charcoal Gray for secondary text */
    }

    /* 3. MODERN CARD BUTTONS (Secondary -> Primary Hover) */
    div.stButton > button {
        width: 100%;
        height: 70px;
        background-color: #FFFFFF;      /* White Base */
        color: #111111;                 /* Black Text */
        border: 2px solid #2E9BCB;      /* Crescent Blue Border */
        border-radius: 12px;
        font-size: 18px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(46, 155, 203, 0.1); /* Subtle Blue Shadow */
    }
    
    /* HOVER STATE: Turns into Primary (Islamic Green) */
    div.stButton > button:hover {
        background-color: #1E8F4E;      /* Islamic Green BG */
        color: #FFFFFF;                 /* White Text */
        border-color: #1E8F4E;
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(30, 143, 78, 0.25); /* Green Glow */
    }
    
    /* 4. INFO BOX STYLING */
    .stAlert {
        background-color: #F0F7F4; /* Very light green bg */
        border-left: 4px solid #1E8F4E; /* Islamic Green Accent */
        color: #111111;
    }
    
    /* Logo styling */
    img { border-radius: 8px; }
    
</style>
""", unsafe_allow_html=True)

# --- MAIN INTERFACE ---

# 1. Logo Section
if os.path.exists("logo.png"):
    col_logo1, col_logo2, col_logo3 = st.columns([1,1,1])
    with col_logo2:
        st.image("logo.png", use_container_width=True)

st.title("Jamaat-e-Islami Islamabad")
st.markdown("**Digital Knowledge Base & Election Management System**")
st.write("") # Spacer

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

# 3. Navigation Grid
st.subheader("Select a Module")
col1, col2 = st.columns(2)

# --- CARD 1: PUBLIC CHAT ---
with col1:
    if os.path.exists("chat_icon.png"):
        st.image("chat_icon.png", width=90)
    else:
        st.image("https://cdn-icons-png.flaticon.com/512/8943/8943377.png", width=90)
        
    if st.button("Open Public Chat", key="btn_chat", use_container_width=True):
        st.switch_page("pages/1_Chat.py")

# --- CARD 2: ADMIN PANEL ---
with col2:
    if os.path.exists("admin_icon.png"):
        st.image("admin_icon.png", width=90)
    else:
        st.image("https://cdn-icons-png.flaticon.com/512/2942/2942813.png", width=90)
        
    if st.button("Open Admin Panel", key="btn_admin", use_container_width=True):
        st.switch_page("pages/2_Admin.py")

st.markdown("---")
st.caption("© 2025 Jamaat-e-Islami Islamabad | Developed for Digital Wing")