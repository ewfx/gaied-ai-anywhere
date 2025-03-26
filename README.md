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
A brief overview of your project and its purpose. Mention which problem statement are your attempting to solve. Keep it concise and engaging.

## 🎥 Demo
🔗 [Live Demo](#) (if applicable)  
📹 [Video Demo](#) (if applicable)  
🖼️ Screenshots:

![Screenshot 1](link-to-image)

## 💡 Inspiration
What inspired you to create this project? Describe the problem you're solving.

## ⚙️ What It Does
Explain the key features and functionalities of your project.

## 🛠️ How We Built It
Briefly outline the technologies, frameworks, and tools used in development.

## 🚧 Challenges We Faced
Describe the major technical or non-technical challenges your team encountered.

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
