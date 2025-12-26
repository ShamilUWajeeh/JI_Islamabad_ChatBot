import streamlit as st
import requests
from streamlit_lottie import st_lottie
from db import init_db
import os
import base64

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

# Helper to load local image for HTML embedding
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

# --- CSS STYLING ---
st.markdown("""
<style>
    /* 1. ANIMATIONS */
    @keyframes float-logo {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
        100% { transform: translateY(0px); }
    }
    
    /* 2. MAIN LAYOUT COLORS */
    .stApp {
        background-color: #FFFFFF;
    }
    
    /* 3. CUSTOM HEADER (Logo + Big Text) */
    .main-header-container {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 20px;
        padding-bottom: 20px;
        border-bottom: 2px solid;
        border-image: linear-gradient(135deg, #1E8F4E 0%, #2E9BCB 100%) 1;
    }
    
    .header-logo {
        width: 80px; /* Adjust logo size */
        margin-right: 20px;
        animation: float-logo 3s ease-in-out infinite; /* Floating Animation */
    }
    
    .header-text {
        font-family: 'sans-serif';
        color: #111111;
        font-weight: 800;
        font-size: 3.5rem; /* EXTRA LARGE TEXT */
        line-height: 1.1;
        margin: 0;
    }
    
    /* Mobile Responsiveness for Header */
    @media (max-width: 600px) {
        .header-text { font-size: 2.2rem; }
        .header-logo { width: 60px; }
    }

    /* 4. BUTTON CARDS */
    div.stButton > button {
        width: 100%;
        height: 80px;
        background-color: #FFFFFF;
        color: #111111;
        border: 2px solid #2E9BCB; /* Crescent Blue Border */
        border-radius: 12px;
        font-size: 20px;
        font-weight: 700;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(46, 155, 203, 0.1);
    }
    
    /* Button Hover Effect */
    div.stButton > button:hover {
        background-color: #1E8F4E; /* Islamic Green */
        color: #FFFFFF;
        border-color: #1E8F4E;
        transform: translateY(-3px);
        box-shadow: 0 8px 15px rgba(30, 143, 78, 0.25);
    }

    /* 5. TEXT & ALERTS */
    .stAlert {
        background-color: #F0F7F4;
        border-left: 5px solid #1E8F4E;
        color: #111111;
    }
    
    p { font-size: 1.1rem; color: #4A4A4A; }
    
</style>
""", unsafe_allow_html=True)

# --- MAIN INTERFACE ---

# 1. Custom Animated Header (Logo + Big Text)
# We use HTML to force them side-by-side with animation
logo_b64 = get_base64_image("logo.png")
logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="header-logo">' if logo_b64 else ''

st.markdown(f"""
    <div class="main-header-container">
        {logo_html}
        <h1 class="header-text">Jamaat-e-Islami<br>Islamabad</h1>
    </div>
""", unsafe_allow_html=True)


# 2. Hero Section (Animation + Intro)
col_anim, col_text = st.columns([1, 1.5])

with col_anim:
    if lottie_coding:
        st_lottie(lottie_coding, height=220, key="unique_animation_key")
    else:
        st.image("https://cdn-icons-png.flaticon.com/512/10605/10605943.png", width=150)

with col_text:
    st.info("""
    **Assalam-o-Alaikum!**
    
    Welcome to the official digital portal. 
    Select a dashboard below to manage elections or assist voters.
    """)

st.write("") # Spacer

# 3. Navigation Grid (Clean Buttons)
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