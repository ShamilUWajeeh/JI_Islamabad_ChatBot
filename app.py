import streamlit as st
import os

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="JI Islamabad Hub",
    page_icon="logo.png",
    layout="wide"
)

# --- 2. CUSTOM CSS ---
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Image Styling */
    .side-image img {
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        max-height: 500px;
        object-fit: cover;
    }

    /* Buttons */
    .stButton button {
        height: 60px;
        font-size: 18px;
        border-radius: 10px;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s;
    }
    
    /* Green Primary Button */
    .primary-btn button {
        background-color: #008000 !important;
        color: white !important;
        border: none;
    }
    .primary-btn button:hover {
        background-color: #006400 !important;
        transform: translateY(-2px);
    }

    /* Gray Secondary Button */
    .secondary-btn button {
        background-color: white !important;
        color: #333 !important;
        border: 2px solid #e0e0e0;
    }
    .secondary-btn button:hover {
        border-color: #333;
        background-color: #f9f9f9 !important;
        transform: translateY(-2px);
    }
    
    /* Text Styling */
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        color: #333;
        line-height: 1.1;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 1.5rem;
        font-weight: 500;
        color: #008000;
        margin-bottom: 25px;
    }
    .description {
        font-size: 1.2rem;
        color: #555;
        line-height: 1.6;
        margin-bottom: 35px;
    }
    
    /* Footer */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #f8f9fa;
        padding: 10px;
        text-align: center;
        font-size: 12px;
        color: #888;
        border-top: 1px solid #eee;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. MAIN LAYOUT ---
st.markdown("<br>", unsafe_allow_html=True)

col_left, col_spacer, col_right = st.columns([1, 0.1, 1.2])

# --- LEFT: DEDICATED SIDE IMAGE ---
with col_left:
    st.markdown('<div class="side-image">', unsafe_allow_html=True)
    
    # Priority Check: Look for side.png, then side.jpg
    if os.path.exists("side.png"):
        st.image("side_image.jpeg", use_container_width=True)
    elif os.path.exists("side_image.jpeg"):
        st.image("side_image.jpeg", use_container_width=True)
    else:
        st.warning("⚠️ Image not found. Please name your file 'side.png'")
        
    st.markdown('</div>', unsafe_allow_html=True)

# --- RIGHT: TEXT & ACTIONS ---
with col_right:
    # Title
    st.markdown('<div class="main-title">JI Islamabad<br>Digital Wing</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Official AI Smart Assistant</div>', unsafe_allow_html=True)
    
    # Description
    st.markdown("""
    <div class="description">
        <b>Assalam-o-Alaikum!</b><br>
        Welcome to the central information hub. This AI is trained to assist you with:
        <ul style="margin-top: 10px;">
            <li>🗳️ <b>Election Constituencies:</b> UCs, Wards, and Census Blocks.</li>
            <li>📜 <b>Party Information:</b> History, Manifesto, and Leadership.</li>
            <li>🏢 <b>Organization:</b> Offices and Contact Details.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Buttons
    btn_col1, btn_col2 = st.columns(2)
    
    with btn_col1:
        st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
        if st.button("Start Chatting 💬"):
            st.switch_page("pages/1_Chat.py")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with btn_col2:
        st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
        if st.button("Admin Panel 🔒"):
            st.switch_page("pages/2_Admin_Panel.py")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 4. FOOTER ---
st.markdown(
    """
    <div class="footer">
        © 2025 Jamaat-e-Islami Islamabad | Digital Wing | Powered by Gemini 2.0 Flash
    </div>
    """,
    unsafe_allow_html=True
)