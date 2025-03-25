import os
import shutil
import tempfile
import extract_msg
import email
import olefile
import fitz  # pymupdf
from docx import Document
from email import policy
from email.parser import BytesParser
from langchain_docling import DoclingLoader
import pytesseract
from PIL import Image
import io
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
from langchain_community.document_loaders import UnstructuredPDFLoader

def extract_text_from_pdf(filepath):
    loader = UnstructuredPDFLoader(filepath, mode="elements")
    docs = loader.load()
    
    print("\n".join(doc.page_content for doc in docs))


def save_attachment(payload, filename, output_dir):
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "wb") as f:
        f.write(payload)
    return filepath

def extract_from_pdf(filepath):
    doc = fitz.open(filepath)
    full_text = ""

    for page in doc:
        # Extract selectable text
        page_text = page.get_text("text").strip()
        extracted_text = page_text if page_text else ""

        # Extract images and apply OCR
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            img_bytes = base_image["image"]
            img_pil = Image.open(io.BytesIO(img_bytes))

            # Perform OCR
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
        return loader.load()
    return "Unsupported .doc format"

def extract_from_msg(filepath, output_dir):
    msg = extract_msg.Message(filepath)
    msg_message = f"Subject: {msg.subject}\nFrom: {msg.sender}\nTo: {msg.to}\nBody:\n{msg.body}"
    
    attachments = []
    for att in msg.attachments:
        attachment_path = save_attachment(att.data, att.longFilename, output_dir)
        attachments.append(attachment_path)
    
    return msg_message, attachments

def extract_from_eml(filepath, output_dir):
    with open(filepath, "rb") as f:
        msg = BytesParser(policy=policy.default).parse(f)
    
    email_text = f"Subject: {msg['subject']}\nFrom: {msg['from']}\nTo: {msg['to']}\n\n"
    email_text += msg.get_body(preferencelist=("plain")).get_content() if msg.get_body() else ""
    
    attachments = []
    for part in msg.iter_attachments():
        attachment_path = save_attachment(part.get_payload(decode=True), part.get_filename(), output_dir)
        attachments.append(attachment_path)
    
    return email_text, attachments

def extract_text_and_attachments(filepath, output_dir):
    ext = filepath.lower().split(".")[-1]
    main_text = ""
    attachment_texts = {}
    attachments = []
    
    if ext == "pdf":
        main_text = extract_from_pdf(filepath)
    elif ext == "docx":
        main_text = extract_from_docx(filepath)
    elif ext == "doc":
        main_text = extract_from_doc(filepath)
    elif ext == "msg":
        main_text, attachments = extract_from_msg(filepath, output_dir)
    elif ext == "eml":
        main_text, attachments = extract_from_eml(filepath, output_dir)
    else:
        main_text = "Unsupported file type"
    
    for att in attachments:
        att_text, _ = extract_text_and_attachments(att, output_dir)
        attachment_texts[att] = att_text
    
    return main_text, attachment_texts

def process_file(filepath, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    print(f"Processing: {filepath}")
    text, attachment_texts = extract_text_and_attachments(filepath, output_dir)
    print("Extracted Text:", text)  # Print first 500 chars for preview
    
    for att, att_text in attachment_texts.items():
        print(f"Extracted Text from {att}:", att_text)  # Preview each attachment text

def image_with_docloader(filepath,output_dir):
    loader = DoclingLoader(filepath)
    documents = loader.load()
    content_path = r"C:\Users\DELL\Downloads\MOMS APPLICATION ID_content.txt"
    content = ""
    with open(content_path, 'w', encoding='utf-8') as f:
        for doc in documents:
            f.write(doc.page_content + "\n\n")      
            content += doc.page_content + "\n\n"
    print(content)

if __name__ == "__main__":
    input_filepath = r"C:\Users\DELL\Downloads\MOMS APPLICATION ID.pdf"  # Replace with the actual file path
    output_directory = r"C:\Users\DELL\Downloads\extracted_files"  # Folder to save extracted attachments
    #process_file(input_filepath, output_directory)
    #image_with_docloader(input_filepath,output_directory)
    extract_text_from_pdf(input_filepath)
