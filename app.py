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
    
    /* Side Image Styling */
    .side-image img {
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        max-height: 500px;
        object-fit: cover;
    }

    /* Icon Styling - Centers the icons in their columns */
    div[data-testid="stImage"] {
        display: flex;
        justify_content: center;
        align-items: center;
    }
    
    /* Icon Hover Effect */
    div[data-testid="stImage"] img {
        transition: transform 0.3s ease;
    }
    div[data-testid="stImage"] img:hover {
        transform: scale(1.1);
    }

    /* Buttons */
    .stButton button {
        height: 50px;
        font-size: 18px;
        border-radius: 25px; /* Rounded pill shape */
        font-weight: 600;
        width: 100%;
        margin-top: 10px;
        border: 2px solid transparent;
        transition: all 0.3s;
    }
    
    /* Primary Button (Chat) */
    div[data-testid="column"]:nth-of-type(1) .stButton button {
        background-color: #008000;
        color: white;
    }
    div[data-testid="column"]:nth-of-type(1) .stButton button:hover {
        background-color: white;
        color: #008000;
        border-color: #008000;
        box-shadow: 0 4px 10px rgba(0,128,0,0.2);
    }

    /* Secondary Button (Admin) */
    div[data-testid="column"]:nth-of-type(2) .stButton button {
        background-color: #f0f2f6;
        color: #333;
    }
    div[data-testid="column"]:nth-of-type(2) .stButton button:hover {
        background-color: #e0e0e0;
        border-color: #999;
    }
    
    /* Text Styling */
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        color: #333;
        line-height: 1.1;
        margin-bottom: 5px;
    }
    .subtitle {
        font-size: 1.5rem;
        font-weight: 500;
        color: #008000;
        margin-bottom: 20px;
    }
    .description {
        font-size: 1.2rem;
        color: #555;
        line-height: 1.6;
        margin-bottom: 30px;
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

# --- LEFT: SIDE IMAGE ---
with col_left:
    st.markdown('<div class="side-image">', unsafe_allow_html=True)
    if os.path.exists("side.png"):
        st.image("side.png", use_container_width=True)
    elif os.path.exists("side.jpg"):
        st.image("side.jpg", use_container_width=True)
    else:
        # Fallback if image is missing
        st.info("ℹ️ Add 'side.png' to display an image here.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- RIGHT: CONTENT & ICONS ---
with col_right:
    # 1. Header Text
    st.markdown('<div class="main-title">JI Islamabad<br>Digital Wing</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Official AI Smart Assistant</div>', unsafe_allow_html=True)
    
    # 2. Description
    st.markdown("""
    <div class="description">
        <b>Assalam-o-Alaikum!</b><br>
        This AI hub is designed to empower you with instant access to:
        <ul style="margin-top: 5px;">
            <li>🗳️ <b>Election Data:</b> Detailed Constituencies & Wards.</li>
            <li>📜 <b>Party Info:</b> Manifesto, Leadership & History.</li>
            <li>🏢 <b>Connect:</b> Office locations & Contact info.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---") # Divider line

    # 3. ACTION CARDS (Icons + Buttons)
    btn_col1, btn_col2 = st.columns(2)
    
    # -- Chat Section --
    with btn_col1:
        if os.path.exists("chat_icon.png"):
            st.image("chat_icon.png", width=80)  # Adjust width as needed
        else:
            st.write("💬") # Fallback emoji
            
        if st.button("Start Chatting"):
            st.switch_page("pages/1_Chat.py")
            
    # -- Admin Section --
    with btn_col2:
        if os.path.exists("admin_icon.png"):
            st.image("admin_icon.png", width=80) # Adjust width as needed
        else:
            st.write("⚙️") # Fallback emoji
            
        if st.button("Admin Panel"):
            st.switch_page("pages/2_Admin_Panel.py")

# --- 4. FOOTER ---
st.markdown(
    """
    <div class="footer">
        © 2025 Jamaat-e-Islami Islamabad | Digital Wing | Powered by Gemini 2.0 Flash
    </div>
    """,
    unsafe_allow_html=True
)