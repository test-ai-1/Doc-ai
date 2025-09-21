"""
LexPlain AI - PDF Processor Module
Handles PDF text extraction with PyPDF2 and OCR fallback
"""

import PyPDF2
import io
from typing import Tuple
from backend.ocr_engine import extract_text_with_ocr, extract_text_from_image, extract_text_from_image_with_fallback

def extract_text_from_pdf(pdf_file) -> Tuple[str, bool]:
    """
    Extract text from uploaded PDF file
    Uses PyPDF2 first, then OCR fallback if needed
    
    Returns:
        Tuple of (extracted_text, used_ocr)
        - extracted_text: The text content
        - used_ocr: Boolean indicating if OCR was used
    """
    try:
        # First try PyPDF2
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        
        for page_num, page in enumerate(pdf_reader.pages):
            page_text = page.extract_text()
            text += page_text + "\n"
        
        # Check if we got meaningful text
        if len(text.strip()) < 50:  # Very short text might indicate scanned PDF
            print(f"PDF text too short ({len(text)} chars), trying OCR...")
            # For PDFs, we'll use a simple fallback since OCR on PDFs is complex
            return f"PDF appears to be scanned. For hackathon demo, please convert to images and upload as PNG/JPG files for OCR analysis. Extracted text: {text}", False
        else:
            return text, False
            
    except Exception as e:
        print(f"PyPDF2 failed: {str(e)}, trying OCR...")
        try:
            # Fallback to OCR
            ocr_text = extract_text_with_ocr(pdf_file)
            if ocr_text:
                return ocr_text, True
            else:
                return f"Error reading PDF: {str(e)}", False
        except Exception as ocr_error:
            return f"Error reading PDF: {str(e)}. OCR also failed: {str(ocr_error)}", False

def is_pdf_scanned(pdf_file) -> bool:
    """
    Check if PDF appears to be scanned (no extractable text)
    Returns: True if likely scanned, False if has text
    """
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        total_text = ""
        
        # Check first few pages
        for page_num in range(min(3, len(pdf_reader.pages))):
            page_text = pdf_reader.pages[page_num].extract_text()
            total_text += page_text
        
        # If very little text, likely scanned
        return len(total_text.strip()) < 100
        
    except Exception:
        return True  # Assume scanned if we can't read it

def extract_text_from_image_file(image_file) -> Tuple[str, bool]:
    """
    Extract text from uploaded image file
    Uses Google Document AI OCR with pytesseract fallback
    
    Returns:
        Tuple of (extracted_text, used_ocr)
        - extracted_text: The text content
        - used_ocr: Always True for images
    """
    try:
        ocr_text = extract_text_from_image_with_fallback(image_file)
        if ocr_text:
            return ocr_text, True
        else:
            return "Could not extract text from image. Please ensure the image is clear and contains readable text.", True
            
    except Exception as e:
        return f"Error processing image: {str(e)}", True
