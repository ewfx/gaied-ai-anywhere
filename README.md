# 🚀 Project Name

## 📌 Table of Contents
- [Introduction](#introduction)
- [Demo](#demo)
- [Inspiration](#inspiration)
- [What It Does](#what-it-does)
- [How We Built It](#how-we-built-it)
- [Challenges We Faced](#challenges-we-faced)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Team](#team)

---

## 🎯 Introduction

The Agentic AI Orchestrator is designed to automate the triage and routing of emails and documents, leveraging AI-powered extraction, classification, and processing. The system streamlines workflows by analyzing unstructured data from multiple formats and providing structured insights for better decision-making.

🔍 Problem Statement

Manual email and document processing is time-consuming, error-prone, and inefficient, especially in industries like banking, finance, and customer support. Organizations receive thousands of emails daily with attachments in different formats, requiring human intervention for:

🔹 Understanding the content (loan requests, transaction authorizations, fee payments, etc.)

🔹 Extracting important data from PDFs, Word documents, Excel sheets, and images

🔹 Classifying requests and routing them to the appropriate department

This solution eliminates manual effort by using AI-driven automation to process, extract, and categorize emails and their attachments efficiently.

## 🎥 Demo
🔗 [Live Demo](#) (if applicable)  
📹 [Video Demo](#) (if applicable)  
🖼️ Screenshots:

![Screenshot 1](https://github.com/ewfx/gaied-ai-anywhere/blob/main/artifacts/demo/snapshot.png)

## 💡 Inspiration

The inspiration for this project came from the inefficiencies and challenges faced in email and document triage within industries like banking, finance, and customer support. Organizations receive a high volume of emails daily, often with complex attachments in various formats. Manually processing these emails is:

📌 Time-Consuming – Employees must manually review, extract, and classify emails and documents.

⚠️ Error-Prone – Critical details can be misclassified or overlooked, leading to operational inefficiencies.

💰 Resource-Intensive – Requires dedicated personnel, increasing costs and slowing down decision-making.

📂 Unstructured Data Complexity – Documents come in different formats (.eml, .msg, .pdf, .csv, .xlsx, images) requiring different extraction methods.

🔄 Duplicate Processing Issues – Emails and attachments may be redundant, leading to repeated processing efforts.

🔍 Lack of Intelligent Search & Routing – Difficulties in quickly retrieving and forwarding relevant data to the right departments.

This project solves these challenges by using AI-powered automation to extract, classify, and route emails and documents efficiently.

## ⚙️ What It Does

📩 Universal Email & Document Extraction: Handles .eml, .msg, .pdf, .docx, .doc, .xlsx, .csv, .png, .jpg, .txt files.

📝 Smart Data Extraction: Parses content using OCR (for images/PDFs).

📂 Agentic-AI Based Classification: Categorizes emails and documents into predefined types.

⚡ FastAPI Backend: Provides a scalable API to process files in real-time.

🎨 Next-Gen Streamlit UI: A modern, sleek, and intuitive frontend for easy interaction.

## 🛠️ How We Built It

This project leverages modern technologies and frameworks to ensure efficiency, scalability, and usability:

Backend & API

🔹 FastAPI – High-performance web framework for API development.

🔹 Pydantic – Data validation and parsing for API requests.

Frontend (UI)

🔹 Streamlit – Interactive web-based UI for document triage.

🔹 Custom CSS – Enhancing the UI with modern, next-gen styling.

Document Processing & Extraction

🔹 extract-msg – Parses .msg email files.

🔹 email.parser – Extracts content from .eml files.

🔹 PyMuPDF (fitz) – Reads and extracts text from PDFs.

🔹 python-docx – Extracts text from Word documents.

🔹 pandas – Handles .csv and .xlsx file processing.

🔹 Pillow & pytesseract – OCR for extracting text from images.

🔹 LangChain & LangGraph – Used for AI-driven classification and automation.

🔹 LangChain-Docling – Efficient document handling and analysis.

## 🚧 Challenges We Faced

1️⃣ Handling Multiple Document Formats

Extracting content from .msg and .eml files required custom parsing.

OCR-based text extraction for images and scanned PDFs was slow.

Solution: Used extract-msg, pymupdf, and pytesseract to handle different formats efficiently.

2️⃣ Duplicate Detection

Faced challenges in deciding whether to store duplicates in a database.

Solution: Used an AI agent to handle duplicate detection dynamically without relying on DB storage.

3️⃣ Scalability & Performance

Large files and multiple requests slowed down processing.

Solution: Optimized API calls, enabled streaming, and used batch processing for efficient document handling.

## 🏃 How to Run
1. Clone the repository  
   ```sh
   git clone https://github.com/ewfx/gaied-ai-anywhere.git
   ```
2. Install dependencies  
   ```sh
   pip install -r requirements.txt (for Python)
   Even after isntalling the above you might have to install pytesseract as below on Windows,
      1) tesseract from https://github.com/UB-Mannheim/tesseract/wiki
      2) locate its path during installation. "C:\Program Files\Tesseract-OCR\" was the default path for me (it might vary with yours so please keep a note of it)
      3) Add the .exe to this "pytesseract.pytesseract.tesseract_cmd" variable in code\src\utils\util.py (as of now it is populated with my default path)
   ```
3. Run the project  
   ```sh
   On one terminal navigate to code\src and run - uvicorn faiss_api:app --host 0.0.0.0 --port 8000 --reload
   On other terminal navigate to code\src and run - streamlit run app.py
   ```

## 🏗️ Tech Stack
- 🔹 Frontend: Streamlit
- 🔹 Backend: FastAPI
- 🔹 Database: didn't require a database
- 🔹 Other: pytesseract, langchain, langgraph

## 👥 Team
- Yegyanathan - [GitHub](https://github.com/Yegy001)
- **Uday** - [GitHub](https://github.com/UdayDheerajNulu)
