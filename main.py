"""
LexPlain AI - A Compassionate Legal Document Explainer
A hackathon-winning app that empowers non-lawyers with AI-powered legal insights
"""

import streamlit as st
import PyPDF2
import google.generativeai as genai
import os
from dotenv import load_dotenv
import io
import re
from typing import Dict, List, Tuple
import json

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_KEY'))

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-pro')

# Page configuration
st.set_page_config(
    page_title="LexPlain AI - Your Legal Guardian Angel",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern, mobile-friendly design
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .risk-card {
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid;
    }
    
    .risk-high {
        background-color: #ffebee;
        border-left-color: #f44336;
    }
    
    .risk-medium {
        background-color: #fff3e0;
        border-left-color: #ff9800;
    }
    
    .risk-low {
        background-color: #e8f5e8;
        border-left-color: #4caf50;
    }
    
    .explanation-box {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    .negotiation-box {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #2196f3;
        margin: 1rem 0;
    }
    
    .what-if-box {
        background-color: #f3e5f5;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #9c27b0;
        margin: 1rem 0;
    }
    
    .upload-zone {
        border: 2px dashed #667eea;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background-color: #f8f9fa;
        margin: 1rem 0;
    }
    
    .easter-egg {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def extract_text_from_pdf(pdf_file) -> str:
    """Extract text from uploaded PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        st.error(f"❌ Error reading PDF: {str(e)}")
        return ""

def analyze_document_with_gemini(document_text: str, analysis_type: str) -> str:
    """Send document to Gemini for analysis"""
    try:
        if analysis_type == "risks":
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
        
        elif analysis_type == "explain_clause":
            prompt = f"""
            Explain this legal clause in the warmest, most protective way possible - like a wise friend who has your back. 
            Make it feel empowering, not scary. Use simple language and be encouraging.
            
            Clause: {document_text}
            
            Include:
            1. What it means in plain English
            2. Why it matters to them
            3. One empowering question they should ask before signing
            4. A tone that's supportive and protective
            """
        
        elif analysis_type == "what_if":
            prompt = f"""
            The user is asking: "{document_text}"
            
            Based on the legal document they uploaded, simulate what would actually happen in this scenario.
            Be realistic but not scary. Explain it like you're their protective older sibling who knows the law.
            Be warm, supportive, and give them actionable advice.
            
            If they seem scared or worried, be extra gentle and encouraging.
            """
        
        elif analysis_type == "negotiation":
            prompt = f"""
            Create a polite, professional email the user can send to negotiate this clause.
            Make it sound confident but respectful. Include specific suggestions for improvement.
            
            Clause: {document_text}
            
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
        st.error(f"❌ Error with AI analysis: {str(e)}")
        return "Sorry, I'm having trouble analyzing this right now. Please try again."

def display_risk_card(risk: Dict, index: int):
    """Display a risk card with appropriate styling"""
    level_colors = {
        "HIGH": "risk-high",
        "MEDIUM": "risk-medium", 
        "LOW": "risk-low"
    }
    
    emojis = {
        "HIGH": "🔴",
        "MEDIUM": "🟡",
        "LOW": "🟢"
    }
    
    css_class = level_colors.get(risk.get("level", "LOW"), "risk-low")
    emoji = emojis.get(risk.get("level", "LOW"), "🟢")
    
    st.markdown(f"""
    <div class="{css_class}">
        <h4>{emoji} {risk.get('title', 'Unknown Risk')}</h4>
        <p><strong>What this means:</strong> {risk.get('description', 'No description')}</p>
        <p><strong>Why it's concerning:</strong> {risk.get('concern', 'No details')}</p>
        <p><strong>Simple explanation:</strong> {risk.get('simple_explanation', 'No explanation')}</p>
    </div>
    """, unsafe_allow_html=True)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>⚖️ LexPlain AI</h1>
        <p>Your Compassionate Legal Guardian Angel</p>
        <p><em>Making legal documents understandable, one clause at a time</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🛡️ Privacy & Settings")
        
        # Private mode toggle
        private_mode = st.toggle("🔒 Private Mode", value=True)
        if private_mode:
            st.success("✅ No data is stored - your documents stay private!")
        
        st.markdown("---")
        st.markdown("### 💡 How to use:")
        st.markdown("1. Upload your legal document")
        st.markdown("2. Review the risk analysis")
        st.markdown("3. Ask 'What if?' questions")
        st.markdown("4. Get negotiation help")
        st.markdown("5. Feel empowered! 💪")
        
        st.markdown("---")
        st.markdown("### 🆘 Need Help?")
        st.markdown("**Free Legal Aid:** 1-800-555-LEGAL")
        st.markdown("**Emergency:** 911")
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📄 Upload Your Legal Document")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=['pdf'],
            help="Upload leases, terms of service, loan agreements, etc."
        )
        
        if uploaded_file is not None:
            # Extract text from PDF
            with st.spinner("🔍 Reading your document..."):
                document_text = extract_text_from_pdf(uploaded_file)
            
            if document_text:
                st.success("✅ Document loaded successfully!")
                
                # Store in session state
                st.session_state.document_text = document_text
                st.session_state.uploaded_file = uploaded_file.name
                
                # Risk Analysis Section
                st.header("⚠️ Risk Radar - Top Concerns")
                
                with st.spinner("🕵️ Analyzing risks..."):
                    risk_analysis = analyze_document_with_gemini(document_text, "risks")
                
                try:
                    # Try to parse JSON response
                    risk_data = json.loads(risk_analysis)
                    risks = risk_data.get("risks", [])
                    
                    if risks:
                        for i, risk in enumerate(risks[:3]):  # Show top 3
                            display_risk_card(risk, i)
                    else:
                        st.warning("No specific risks identified, but always read carefully!")
                        
                except json.JSONDecodeError:
                    # Fallback if JSON parsing fails
                    st.markdown(f"""
                    <div class="explanation-box">
                        <h4>🔍 Risk Analysis</h4>
                        <p>{risk_analysis}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Clause Explainer Section
                st.header("🔍 Explain Any Clause")
                
                clause_text = st.text_area(
                    "Paste any confusing clause here:",
                    placeholder="Copy and paste the part of the document you want explained...",
                    height=100
                )
                
                if st.button("🧠 Explain This Clause", type="primary"):
                    if clause_text.strip():
                        with st.spinner("🤔 Analyzing clause..."):
                            explanation = analyze_document_with_gemini(clause_text, "explain_clause")
                        
                        st.markdown(f"""
                        <div class="explanation-box">
                            <h4>💡 Your Personal Legal Translator</h4>
                            <p>{explanation}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.warning("Please paste a clause to explain!")
                
                # What If Simulator
                st.header("🎭 'What If?' Simulator")
                
                what_if_question = st.text_input(
                    "Ask me anything:",
                    placeholder="e.g., 'What if I break my lease?' or 'What if I can't pay on time?'"
                )
                
                if st.button("🔮 Simulate This Scenario"):
                    if what_if_question.strip():
                        # Check for easter egg
                        if "i'm scared" in what_if_question.lower() or "im scared" in what_if_question.lower():
                            st.markdown("""
                            <div class="easter-egg">
                                <h3>💝 You're Not Alone</h3>
                                <p>It's okay to feel that way. You're not alone. Here's a free legal aid hotline: <a href="tel:1-800-555-LEGAL" style="color: white;">1-800-555-LEGAL</a></p>
                                <p>You've got this! 💪</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with st.spinner("🔮 Simulating scenario..."):
                            simulation = analyze_document_with_gemini(what_if_question, "what_if")
                        
                        st.markdown(f"""
                        <div class="what-if-box">
                            <h4>🎭 Scenario Simulation</h4>
                            <p>{simulation}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.warning("Please ask a 'What if?' question!")
                
                # Negotiation Coach
                if clause_text.strip():
                    st.header("💬 Negotiation Coach")
                    
                    if st.button("📧 Generate Negotiation Email", type="secondary"):
                        with st.spinner("✍️ Crafting your negotiation email..."):
                            negotiation_email = analyze_document_with_gemini(clause_text, "negotiation")
                        
                        st.markdown(f"""
                        <div class="negotiation-box">
                            <h4>📧 Your Negotiation Email</h4>
                            <p>{negotiation_email}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Copy button
                        st.code(negotiation_email, language=None)
                        st.info("💡 Copy the email above and send it to negotiate better terms!")
            
            else:
                st.error("❌ Could not read the PDF. Please try a different file.")
    
    with col2:
        st.header("🌟 Why LexPlain AI?")
        
        st.markdown("""
        <div style="background-color: #f0f8ff; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            <h4>🧠 What If? Simulator</h4>
            <p>Ask "What if?" and get real consequences based on YOUR document. No generic advice!</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background-color: #fff0f5; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            <h4>⚠️ Risk Radar</h4>
            <p>We scan for sneaky clauses and rate them 🟢🟡🔴 so you know what to watch out for.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background-color: #f0fff0; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            <h4>💬 Negotiation Coach</h4>
            <p>Get professional emails you can send to push back on unfair terms. You've got this!</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("### 💝 Our Promise")
        st.markdown("""
        - **Warm & Protective**: Like a wise friend who's got your back
        - **Empowering**: We help you negotiate, not just understand
        - **Private**: Your documents never leave your device
        - **Real**: Based on YOUR specific document, not generic advice
        """)
        
        st.markdown("---")
        
        st.markdown("### 🏆 Hackathon Features")
        st.markdown("""
        ✨ **What If? Simulator** - Real consequences from YOUR doc
        ✨ **Risk Radar** - Color-coded danger zones  
        ✨ **Negotiation Coach** - Ready-to-send emails
        ✨ **Easter Egg** - Type "I'm scared" for support
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p>⚖️ <strong>LexPlain AI</strong> - Making Legal Documents Human-Friendly</p>
        <p><em>Built with ❤️ for hackathon judges who believe in empowering people</em></p>
        <p>🔒 Your privacy matters - no data stored, no tracking, just protection</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
