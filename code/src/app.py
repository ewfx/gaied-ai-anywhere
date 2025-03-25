import streamlit as st
import requests
import os

# API URLs
FAISS_ADD_URL = "http://127.0.0.1:8000/add_document/"
FAISS_SEARCH_URL = "http://127.0.0.1:8000/search/"

st.title("📄 FAISS Document Search & Upload")

# Upload Section
st.subheader("📤 Upload a Document for Processing")
uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt"])

if uploaded_file:
    # Save file temporarily
    file_path = os.path.join("uploads", uploaded_file.name)
    os.makedirs("uploads", exist_ok=True)
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success(f"Uploaded {uploaded_file.name} ✅")

    # Send file for processing
    response = requests.post("http://127.0.0.1:8000/process_document/", json={"file_path": file_path})
    st.info(response.json().get("message", "Processing error."))

# Search Section
st.subheader("🔎 Search Documents")

query = st.text_input("Enter your search query:")
top_k = st.slider("Number of results:", 1, 10, 3)

if st.button("Search"):
    if query:
        response = requests.post(FAISS_SEARCH_URL, json={"query": query, "top_k": top_k})
        results = response.json().get("results", [])

        if results:
            st.subheader("Search Results:")
            for res in results:
                st.write(f"📄 **{res['doc_id']}** (Score: {res['distance']:.4f})")
                st.write(res["text"])
                st.write("---")
        else:
            st.write("❌ No relevant documents found.")
    else:
        st.warning("Please enter a query.")

st.write("🔥 Powered by FAISS & FastAPI")
