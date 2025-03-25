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
import pandas as pd

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Fixed Directory for Attachments
ATTACHMENTS_DIR = "attachments"
os.makedirs(ATTACHMENTS_DIR, exist_ok=True)

def extract_from_xlsx(filepath):
    """Extracts text content from all sheets in an Excel file."""
    try:
        xls = pd.ExcelFile(filepath)
        extracted_text = ""

        for sheet_name in xls.sheet_names:
            df = xls.parse(sheet_name)
            extracted_text += f"Sheet: {sheet_name}\n"
            extracted_text += df.to_string(index=False, header=True) + "\n\n"

        return extracted_text.strip()
    except Exception as e:
        return f"Error processing Excel file: {str(e)}"

def extract_from_csv(filepath):
    """Extracts text from a CSV file."""
    try:
        df = pd.read_csv(filepath)
        return df.to_string(index=False, header=True)
    except Exception as e:
        return f"Error processing CSV file: {str(e)}"

def extract_from_image(filepath):
    """Extracts text from an image using OCR."""
    try:
        image = Image.open(filepath)
        text = pytesseract.image_to_string(image).strip()
        return text
    except Exception as e:
        return f"Error processing image: {str(e)}"

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

# Function to extract .msg email content and attachments
def extract_from_msg(filepath):
    """Extracts email content and saves attachments to a fixed directory."""
    msg = extract_msg.Message(filepath)
    msg_message = f"Subject: {msg.subject}\nFrom: {msg.sender}\nTo: {msg.to}\nBody:\n{msg.body}"

    attachments = {}
    for att in msg.attachments:
        att_filename = att.longFilename
        att_data = att.data

        # Save attachment in fixed directory
        attachment_path = os.path.join(ATTACHMENTS_DIR, att_filename)
        with open(attachment_path, "wb") as f:
            f.write(att_data)

        # Process attachment using respective extractor
        att_text, _ = extract_text_and_attachments(attachment_path)
        attachments[att_filename] = att_text

    return msg_message, attachments

# Function to extract .eml email content and attachments
def extract_from_eml(filepath):
    """Extracts email content and saves attachments to a fixed directory."""
    with open(filepath, "rb") as f:
        msg = BytesParser(policy=policy.default).parse(f)

    email_text = f"Subject: {msg['subject']}\nFrom: {msg['from']}\nTo: {msg['to']}\n\n"
    if msg.get_body(preferencelist=("plain")):
        email_text += msg.get_body(preferencelist=("plain")).get_content()

    attachments = {}
    for part in msg.iter_attachments():
        filename = part.get_filename()
        payload = part.get_payload(decode=True)

        if filename and payload:
            # Save attachment in fixed directory
            attachment_path = os.path.join(ATTACHMENTS_DIR, filename)
            with open(attachment_path, "wb") as f:
                f.write(payload)

            # Process attachment using respective extractor
            att_text, _ = extract_text_and_attachments(attachment_path)
            attachments[filename] = att_text

    return email_text, attachments

def extract_from_txt(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

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
    elif ext == "png" or ext == "jpg" or ext == "jpeg":
        return extract_from_image(filepath), {}
    elif ext == "xlsx":
        return extract_from_xlsx(filepath), {}
    elif ext == "csv":
        return extract_from_csv(filepath), {}
    elif ext == "txt":
        return extract_from_txt(filepath), {}
    else:
        return "Unsupported file type", {}

def process_file(filepath):
    text, attachment_texts = extract_text_and_attachments(filepath)
    content = text
    for att_name, att_text in attachment_texts.items():
        content += str(att_text) 
    return content

