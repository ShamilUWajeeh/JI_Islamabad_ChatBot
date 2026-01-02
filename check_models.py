from google import genai
import os

# 🔴 Replace this with your actual key
api_key = "AIzaSyD1KfvHRmTAB0mocTZrdV5RX-NGI0XxUA4" 

try:
    print("🚀 Connecting with new google-genai library...")
    client = genai.Client(api_key=api_key)
    
    print("✅ Connection successful! Listing available models...")
    print("-" * 30)
    
    # New syntax to list models
    for m in client.models.list():
        # Only show generation models (filtering out others to keep it clean)
        if "generateContent" in m.supported_actions:
            print(f"- {m.name}")
            
    print("-" * 30)
    print("🎉 If you see the list above, your setup is perfect.")

except Exception as e:
    print(f"❌ Error: {e}")