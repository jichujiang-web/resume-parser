# app/utils.py
"""
Utility functions for extracting text and contact info from PDFs and DOCX files,
and for cleaning model output.
"""

import re
import pdfplumber
from docx import Document
import json


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from a PDF using pdfplumber and clean it.

    Args:
        file_path (str): Path to the PDF file.

    Returns:
        str: Cleaned text extracted from the PDF.
    """
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    # Clean extracted text
    return clean_model_output(text)


def extract_text_from_docx(file_path: str) -> str:
    """
    Extract text from a DOCX file and clean it.

    Args:
        file_path (str): Path to the DOCX file.

    Returns:
        str: Cleaned text extracted from the DOCX file.
    """
    doc = Document(file_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"

    # Clean extracted text
    return clean_model_output(text)


def extract_contact_info(text: str) -> dict:
    """
    Extract contact information such as email and phone number from text using regex.

    Args:
        text (str): Input text to search for contact info.

    Returns:
        dict: Dictionary containing 'name', 'email', and 'phone' keys.
    """
    email_regex = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    phone_regex = r"\+?\d[\d\s\-\(\)]{7,}\d"

    email_match = re.search(email_regex, text)
    phone_match = re.search(phone_regex, text)

    return {
        "name": None,  # Optional: extract with LLM or heuristics
        "email": email_match.group(0) if email_match else None,
        "phone": phone_match.group(0) if phone_match else None
    }


def clean_model_output(output_text: str):
    """
    Clean raw text or model output:
    - Remove excessive newlines
    - Remove empty markdown code blocks
    - Try to extract JSON content

    Args:
        output_text (str): Text to clean.

    Returns:
        str or dict: Cleaned text or extracted JSON object.
    """
    # Remove multiple consecutive newlines
    output_text = re.sub(r'\n\s*\n+', '\n', output_text)

    # Remove empty markdown code blocks (``` ... ```)
    output_text = re.sub(r'```[\s]*```', '', output_text)

    # Try to extract JSON
    json_match = re.search(r'\{.*\}', output_text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass

    # Fallback: return cleaned string
    return output_text.strip()
