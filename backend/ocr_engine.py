"""
LexPlain AI - OCR Engine Module
Handles Google Document AI OCR for scanned PDFs and images
"""

import os
import io
from typing import Optional
from google.cloud import documentai
from dotenv import load_dotenv
import pytesseract
from PIL import Image

# Load environment variables
load_dotenv()

def extract_text_with_ocr(pdf_file) -> Optional[str]:
    """
    Extract text from PDF using Google Document AI OCR
    Handles scanned PDFs and images
    
    Returns:
        Extracted text or None if failed
    """
    try:
        # Get credentials path from environment
        credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        if not credentials_path:
            print("GOOGLE_APPLICATION_CREDENTIALS not set, skipping OCR")
            return None
        
        # Initialize Document AI client
        client = documentai.DocumentProcessorServiceClient()
        
        # For hackathon, use pre-trained OCR processor
        # In production, you'd use your specific processor ID
        project_id = "your-project-id"  # Replace with actual project ID
        location = "us-central1"
        processor_id = "pretrained-ocr"  # Pre-trained OCR processor
        
        processor_name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"
        
        # Read PDF file
        pdf_content = pdf_file.read()
        pdf_file.seek(0)  # Reset file pointer
        
        # Create document
        raw_document = documentai.RawDocument(
            content=pdf_content,
            mime_type="application/pdf"
        )
        
        # Process document
        request = documentai.ProcessRequest(
            name=processor_name,
            raw_document=raw_document
        )
        
        result = client.process_document(request=request)
        document = result.document
        
        # Extract text
        text = document.text
        
        if text and len(text.strip()) > 0:
            print(f"OCR extracted {len(text)} characters")
            return text
        else:
            print("OCR returned empty text")
            return None
            
    except Exception as e:
        print(f"OCR failed: {str(e)}")
        # For hackathon demo, return a placeholder
        return "OCR processing failed - this appears to be a scanned document. Please ensure you have valid Google Cloud credentials set up for Document AI OCR processing."

def extract_text_from_image(image_file) -> Optional[str]:
    """
    Extract text from image file using Google Document AI OCR
    Handles PNG, JPG, JPEG images
    
    Returns:
        Extracted text or None if failed
    """
    try:
        # Get credentials path from environment
        credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        if not credentials_path:
            print("GOOGLE_APPLICATION_CREDENTIALS not set, skipping OCR")
            return None
        
        # Initialize Document AI client
        client = documentai.DocumentProcessorServiceClient()
        
        # For hackathon, use pre-trained OCR processor
        project_id = "your-project-id"  # Replace with actual project ID
        location = "us-central1"
        processor_id = "pretrained-ocr"  # Pre-trained OCR processor
        
        processor_name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"
        
        # Read image file
        image_content = image_file.read()
        image_file.seek(0)  # Reset file pointer
        
        # Determine MIME type based on file extension
        file_extension = image_file.name.lower().split('.')[-1]
        mime_type_map = {
            'png': 'image/png',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg'
        }
        mime_type = mime_type_map.get(file_extension, 'image/jpeg')
        
        # Create document
        raw_document = documentai.RawDocument(
            content=image_content,
            mime_type=mime_type
        )
        
        # Process document
        request = documentai.ProcessRequest(
            name=processor_name,
            raw_document=raw_document
        )
        
        result = client.process_document(request=request)
        document = result.document
        
        # Extract text
        text = document.text
        
        if text and len(text.strip()) > 0:
            print(f"OCR extracted {len(text)} characters from image")
            return text
        else:
            print("OCR returned empty text from image")
            return None
            
    except Exception as e:
        print(f"Image OCR failed: {str(e)}")
        # For hackathon demo, return a placeholder
        return "Image OCR processing failed. Please ensure you have valid Google Cloud credentials set up for Document AI OCR processing."

def extract_text_with_pytesseract(image_file) -> Optional[str]:
    """
    Fallback OCR using pytesseract (works without Google Cloud)
    For hackathon demo purposes
    
    Returns:
        Extracted text or None if failed
    """
    try:
        # Reset file pointer
        image_file.seek(0)
        
        # Open image with PIL
        image = Image.open(image_file)
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Extract text using pytesseract
        text = pytesseract.image_to_string(image)
        
        if text and len(text.strip()) > 0:
            print(f"Pytesseract extracted {len(text)} characters from image")
            return text.strip()
        else:
            print("Pytesseract returned empty text from image")
            return None
            
    except Exception as e:
        print(f"Pytesseract OCR failed: {str(e)}")
        return None

def extract_text_from_image_with_fallback(image_file) -> Optional[str]:
    """
    Extract text from image with Google Document AI, fallback to pytesseract
    Perfect for hackathon demos
    
    Returns:
        Extracted text or None if both methods fail
    """
    # First try Google Document AI
    try:
        credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        if credentials_path and os.path.exists(credentials_path):
            result = extract_text_from_image(image_file)
            if result and "processing failed" not in result.lower():
                return result
    except Exception as e:
        print(f"Google Document AI failed: {str(e)}")
    
    # Fallback to pytesseract
    print("Falling back to pytesseract OCR...")
    pytesseract_result = extract_text_with_pytesseract(image_file)
    
    if pytesseract_result:
        return pytesseract_result
    else:
        return "OCR processing failed. For hackathon demo, please ensure you have either Google Cloud credentials set up or pytesseract installed. The image may also be too blurry or contain no readable text."
