"""
LexPlain AI - AI Engine Module
Contains all Gemini AI logic for document analysis, explanations, and simulations
"""

import google.generativeai as genai
import os
import json
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_KEY'))

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-pro')

def explain_clause(text: str) -> str:
    """
    Explain a legal clause in a warm, protective way
    Returns: Friendly explanation + risk + empowering question
    """
    try:
        prompt = f"""
        Explain this legal clause in the warmest, most protective way possible - like a wise friend who has your back. 
        Make it feel empowering, not scary. Use simple language and be encouraging.
        
        Clause: {text}
        
        Include:
        1. What it means in plain English
        2. Why it matters to them
        3. One empowering question they should ask before signing
        4. A tone that's supportive and protective
        """
        
        response = model.generate_content(prompt)
        return response.text
    
    except Exception as e:
        return f"Sorry, I'm having trouble analyzing this right now. Please try again. Error: {str(e)}"

def summarize_document(text: str) -> str:
    """
    Summarize the entire legal document in 3-5 simple sentences
    Returns: Plain-English summary focusing on obligations and risks
    """
    try:
        prompt = f"""
        Summarize this entire legal document in 3–5 simple, plain-English sentences. 
        Focus on: What is the user agreeing to? What are the biggest obligations or risks? 
        What should they absolutely not miss?
        
        Document text: {text[:4000]}
        
        Make it warm and protective - like a friend warning you about what you're signing.
        """
        
        response = model.generate_content(prompt)
        return response.text
    
    except Exception as e:
        return f"Sorry, I couldn't summarize this document. Please try again. Error: {str(e)}"

def simulate_what_if(scenario: str, full_text: str) -> str:
    """
    Simulate consequences of a scenario based on the legal document
    Returns: Realistic simulation with actionable advice
    """
    try:
        # Check for easter egg
        if "i'm scared" in scenario.lower() or "im scared" in scenario.lower():
            return """It's okay. You're not alone. Here's a free legal aid hotline: https://www.lawhelp.org . You've got this 💪"""
        
        prompt = f"""
        The user is asking: "{scenario}"
        
        Based on this legal document, simulate what would actually happen in this scenario.
        Be realistic but not scary. Explain it like you're their protective older sibling who knows the law.
        Be warm, supportive, and give them actionable advice.
        
        Document context: {full_text[:2000]}
        
        If they seem scared or worried, be extra gentle and encouraging.
        """
        
        response = model.generate_content(prompt)
        return response.text
    
    except Exception as e:
        return f"Sorry, I couldn't simulate that scenario. Please try again. Error: {str(e)}"

def generate_negotiation_email(clause: str) -> str:
    """
    Generate a polite, professional negotiation email
    Returns: Ready-to-send email with specific suggestions
    """
    try:
        prompt = f"""
        Create a polite, professional email the user can send to negotiate this clause.
        Make it sound confident but respectful. Include specific suggestions for improvement.
        
        Clause: {clause}
        
        Format as a ready-to-send email with:
        1. Professional greeting
        2. Acknowledgment of the clause
        3. Specific request for modification
        4. Reasonable justification
        5. Polite closing
        """
        
        response = model.generate_content(prompt)
        return response.text
    
    except Exception as e:
        return f"Sorry, I couldn't generate a negotiation email. Please try again. Error: {str(e)}"

def analyze_risks(document_text: str) -> List[Dict]:
    """
    Analyze document for risks and return structured risk data
    Returns: List of risk dictionaries with title, level, description, etc.
    """
    try:
        prompt = f"""
        Analyze this legal document and identify the TOP 3 most concerning or sneaky clauses that could hurt a regular person financially or legally. 
        For each risk, provide:
        1. A brief description in plain English
        2. A risk level (HIGH/MEDIUM/LOW)
        3. Why it's concerning
        4. A simple explanation like you're talking to a 15-year-old
        
        Document text: {document_text[:4000]}
        
        Format as JSON:
        {{
            "risks": [
                {{
                    "title": "Risk title",
                    "level": "HIGH/MEDIUM/LOW",
                    "description": "What this means",
                    "concern": "Why it's bad",
                    "simple_explanation": "Like talking to a teenager"
                }}
            ]
        }}
        """
        
        response = model.generate_content(prompt)
        
        try:
            # Try to parse JSON response
            risk_data = json.loads(response.text)
            return risk_data.get("risks", [])
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return [{
                "title": "Analysis Complete",
                "level": "MEDIUM",
                "description": "Document analysis completed",
                "concern": "Please review carefully",
                "simple_explanation": response.text
            }]
    
    except Exception as e:
        return [{
            "title": "Analysis Error",
            "level": "LOW",
            "description": "Could not analyze risks",
            "concern": "Please review manually",
            "simple_explanation": f"Error: {str(e)}"
        }]
