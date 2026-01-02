import streamlit as st
import os

# --- PASSWORD PROTECTION ---
ADMIN_PASSWORD = "123"  # Change this to your desired password

st.set_page_config(page_title="Admin Panel", page_icon="⚙️")

st.title("⚙️ Admin Dashboard")

# Check Password
password = st.text_input("Enter Admin Password", type="password")

if password != ADMIN_PASSWORD:
    st.stop()  # Stop here if password is wrong

st.success("✅ Access Granted")

# --- DATA FILE CHECKER ---
st.subheader("📁 Data System Status")

DATA_FILE = "Cleaned_Master_List.txt"

if os.path.exists(DATA_FILE):
    st.success(f"File Found: `{DATA_FILE}`")
    
    # Read File Stats
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = f.read()
        
    col1, col2 = st.columns(2)
    col1.metric("Total Characters", len(data))
    col2.metric("Estimated Pages", len(data) // 3000)
    
    # Preview Data
    with st.expander("📄 View Raw Data Preview (First 2000 chars)"):
        st.text(data[:2000] + "...")
        
else:
    st.error(f"❌ Critical Error: `{DATA_FILE}` not found!")
    st.warning("Please run the cleaning script or place the file in the main folder.")

st.divider()

# --- API KEY CHECK ---
st.subheader("🔑 API Key Status")
try:
    api_key = st.secrets.get("GEMINI_API_KEY")
    if api_key:
        st.success(f"API Key is Set (Ends with ...{api_key[-4:]})")
    else:
        st.error("API Key is MISSING in secrets.toml")
except:
    st.error("Secrets file not found.")