import streamlit as st
import requests
import os
import json

# API URL
PROCESS_URL = "http://127.0.0.1:8000/process_document/"

# Next-Gen Modern UI Colors
PRIMARY_COLOR = "#6C63FF"  # Vibrant Purple
SECONDARY_COLOR = "#00D4FF"  # Neon Blue
BACKGROUND_COLOR = "#0D0D0D"  # Dark Background
TEXT_COLOR = "#F8F8F8"  # Light Text
CARD_BG_COLOR = "#1E1E2E"  # Dark Card Background
ACCENT_COLOR = "#FF007F"  # Hot Pink Accent

# Set up page styling
st.set_page_config(page_title="Gen AI Orchestrator", layout="wide")

# Apply custom futuristic UI styling
st.markdown(f"""
    <style>
        body {{
            background-color: {BACKGROUND_COLOR};
            color: {TEXT_COLOR};
            font-family: 'Inter', sans-serif;
        }}
        .stApp {{
            background-color: {BACKGROUND_COLOR};
        }}
        .stButton>button {{
            background: linear-gradient(135deg, {PRIMARY_COLOR}, {ACCENT_COLOR});
            color: white;
            font-size: 16px;
            font-weight: bold;
            border-radius: 12px;
            padding: 12px 24px;
            transition: all 0.3s ease-in-out;
            border: none;
        }}
        .stButton>button:hover {{
            background: linear-gradient(135deg, {ACCENT_COLOR}, {SECONDARY_COLOR});
            transform: scale(1.05);
        }}
        .stMarkdown h1 {{
            text-align: center;
            font-size: 36px;
            font-weight: 700;
            color: {SECONDARY_COLOR};
            text-shadow: 2px 2px 10px rgba(0, 212, 255, 0.7);
        }}
        .stMarkdown h3 {{
            text-align: center;
            font-size: 20px;
            font-weight: 500;
            color: {TEXT_COLOR};
        }}
        .highlight-box {{
            background: linear-gradient(135deg, {CARD_BG_COLOR}, {BACKGROUND_COLOR});
            border: 1px solid {ACCENT_COLOR};
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0px 4px 15px rgba(255, 0, 127, 0.3);
            color: {TEXT_COLOR};
            font-size: 18px;
            text-align: center;
        }}
    </style>
""", unsafe_allow_html=True)

# Stylish Header
st.markdown(f"""
    <h1>🚀 Gen AI Orchestrator for Email & Document Triage</h1>
    <h3>by Team <span style='color:{SECONDARY_COLOR}; font-weight: 600;'>Ai-Anywhere</span></h3>
""", unsafe_allow_html=True)

st.markdown("---")

# Upload Section
st.markdown(f"""
    <div class='highlight-box'>
        📤 <b>Upload a Document for Processing</b>
    </div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Choose a file", type=["eml", "msg", "pdf", "docx", "csv", "xlsx", "png", "jpg", "jpeg"])

if uploaded_file:
    # Save file to fixed directory
    file_path = os.path.join("uploads", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success(f"✅ {uploaded_file.name} uploaded successfully!")

    # Send file for processing
    response = requests.post(PROCESS_URL, json={"file_path": file_path})
    result = response.json()
    
    # Display JSON Output in a Styled Box
    st.markdown(f"""
        <div class='highlight-box'>
            📜 <b>Extracted Information</b>
        </div>
    """, unsafe_allow_html=True)
    st.json(result, expanded=True)

# Footer
st.markdown(f"""
    <br><hr>
    <p style="text-align: center; font-size: 14px; color: {TEXT_COLOR};">
        Built with ❤️ using Streamlit | Powered by Next-Gen UI
    </p>
""", unsafe_allow_html=True)
