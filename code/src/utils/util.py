import os
import extract_msg
import olefile
import fitz  # pymupdf
from docx import Document
from email import policy
from email.parser import BytesParser
from langchain_docling import DoclingLoader
import pytesseract
from PIL import Image
import io
from langchain_community.document_loaders import UnstructuredPDFLoader

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_pdf(filepath):
    loader = UnstructuredPDFLoader(filepath, mode="elements")
    docs = loader.load()
    return "\n".join(doc.page_content for doc in docs)

def extract_from_pdf(filepath):
    doc = fitz.open(filepath)
    full_text = ""

    for page in doc:
        page_text = page.get_text("text").strip()
        extracted_text = page_text if page_text else ""

        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            img_bytes = base_image["image"]
            img_pil = Image.open(io.BytesIO(img_bytes))
            
            ocr_text = pytesseract.image_to_string(img_pil).strip()
            extracted_text += f"\n[Image {img_index + 1} OCR]:\n{ocr_text}" if ocr_text else ""

        full_text += extracted_text + "\n\n"
    
    return full_text.strip()

def extract_from_docx(filepath):
    doc = Document(filepath)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_from_doc(filepath):
    if olefile.isOleFile(filepath):
        loader = DoclingLoader(filepath)
        return "\n".join(doc.page_content for doc in loader.load())
    return "Unsupported .doc format"

def extract_from_msg(filepath):
    msg = extract_msg.Message(filepath)
    msg_message = f"Subject: {msg.subject}\nFrom: {msg.sender}\nTo: {msg.to}\nBody:\n{msg.body}"
    
    attachments = {att.longFilename: att.data for att in msg.attachments}
    return msg_message, attachments

def extract_from_eml(filepath):
    with open(filepath, "rb") as f:
        msg = BytesParser(policy=policy.default).parse(f)
    
    email_text = f"Subject: {msg['subject']}\nFrom: {msg['from']}\nTo: {msg['to']}\n\n"
    email_text += msg.get_body(preferencelist=("plain")).get_content() if msg.get_body() else ""
    
    attachments = {part.get_filename(): part.get_payload(decode=True) for part in msg.iter_attachments()}
    return email_text, attachments

def extract_text_and_attachments(filepath):
    ext = filepath.lower().split(".")[-1]
    
    if ext == "pdf":
        return extract_from_pdf(filepath), {}
    elif ext == "docx":
        return extract_from_docx(filepath), {}
    elif ext == "doc":
        return extract_from_doc(filepath), {}
    elif ext == "msg":
        return extract_from_msg(filepath)
    elif ext == "eml":
        return extract_from_eml(filepath)
    else:
        return "Unsupported file type", {}

def process_file(filepath):
    print(f"Processing: {filepath}")
    text, attachment_texts = extract_text_and_attachments(filepath)
    print("Extracted Text:", text)
    content = text
    for att_name, att_text in attachment_texts.items():
        content += att_text
        print(f"Extracted Text from {att_name}:", att_text)
    
    return content

def image_with_docloader(filepath):
    loader = DoclingLoader(filepath)
    documents = loader.load()
    return "\n".join(doc.page_content for doc in documents)
