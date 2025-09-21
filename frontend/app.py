"""
LexPlain AI - Frontend Application
Streamlit UI for the compassionate legal document explainer
"""

import streamlit as st
import os
import sys
from dotenv import load_dotenv

# Add the parent directory to the Python path so we can import backend modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.pdf_processor import extract_text_from_pdf, extract_text_from_image_file
from backend.ai_engine import (
    explain_clause, 
    summarize_document, 
    simulate_what_if, 
    generate_negotiation_email,
    analyze_risks
)

# Load environment variables
load_dotenv()

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
    
    .summary-box {
        background-color: #e8f5e8;
        padding: 0.8rem;
        border-radius: 6px;
        border-left: 3px solid #4caf50;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
    
    .summary-compact {
        background-color: #f0f8f0;
        padding: 0.6rem;
        border-radius: 4px;
        border: 1px solid #4caf50;
        margin: 0.3rem 0;
        font-size: 0.85rem;
        line-height: 1.4;
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
    
    .ocr-badge {
        background-color: #ff9800;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
        margin-left: 0.5rem;
    }
    
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid #f3f3f3;
        border-top: 3px solid #3498db;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)

def display_risk_card(risk: dict, index: int):
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
        
        # Demo mode indicator
        st.info("🎯 **Demo Mode**: OCR works with pytesseract fallback (no Google Cloud needed)")
        
        st.markdown("---")
        st.markdown("### 💡 How to use:")
        st.markdown("1. Upload your legal document (PDF or image)")
        st.markdown("2. Get a quick summary")
        st.markdown("3. Review the risk analysis")
        st.markdown("4. Ask 'What if?' questions")
        st.markdown("5. Get negotiation help")
        st.markdown("6. Feel empowered! 💪")
        
        st.markdown("---")
        st.markdown("### 📸 Image Tips:")
        st.markdown("• **Clear photos** work best")
        st.markdown("• **Good lighting** helps OCR accuracy")
        st.markdown("• **Straight angles** are easier to read")
        st.markdown("• **High resolution** images work better")
        st.markdown("• **Demo mode** uses pytesseract (works offline!)")
        
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
            "Choose a PDF file or image",
            type=['pdf', 'png', 'jpg', 'jpeg'],
            help="Upload leases, terms of service, loan agreements, or images of documents"
        )
        
        if uploaded_file is not None:
            # Determine file type and extract text accordingly
            file_extension = uploaded_file.name.lower().split('.')[-1]
            
            if file_extension == 'pdf':
                # Extract text from PDF
                with st.spinner("🔍 Reading your PDF document..."):
                    document_text, used_ocr = extract_text_from_pdf(uploaded_file)
            else:
                # Extract text from image
                with st.spinner("🖼️ Analyzing your image with OCR..."):
                    document_text, used_ocr = extract_text_from_image_file(uploaded_file)
            
            if document_text:
                st.success("✅ Document loaded successfully!")
                
                # Show OCR badge if OCR was used
                if used_ocr:
                    if file_extension == 'pdf':
                        st.markdown('<span class="ocr-badge">🖼 OCR Used (Scanned PDF)</span>', unsafe_allow_html=True)
                    else:
                        st.markdown('<span class="ocr-badge">🖼 OCR Used (Image)</span>', unsafe_allow_html=True)
                
                # Store in session state
                st.session_state.document_text = document_text
                st.session_state.uploaded_file = uploaded_file.name
                st.session_state.used_ocr = used_ocr
                
                # PDF Summary Section - Compact Design
                st.subheader("📄 Document Summary")
                
                # Inline button and summary display
                col_btn, col_status = st.columns([1, 3])
                
                with col_btn:
                    summary_clicked = st.button("📄 Get Summary", type="primary", use_container_width=True)
                
                with col_status:
                    if summary_clicked:
                        with st.spinner("📝 Creating summary..."):
                            summary = summarize_document(document_text)
                        
                        st.markdown(f"""
                        <div class="summary-compact">
                            <strong>📄 Summary:</strong> {summary}
                        </div>
                        """, unsafe_allow_html=True)
                
                # Risk Analysis Section
                st.header("⚠️ Risk Radar - Top Concerns")
                
                with st.spinner("🕵️ Analyzing risks..."):
                    risks = analyze_risks(document_text)
                
                if risks:
                    for i, risk in enumerate(risks[:3]):  # Show top 3
                        display_risk_card(risk, i)
                else:
                    st.warning("No specific risks identified, but always read carefully!")
                
                # Clause Explainer Section
                st.header("🔍 Explain Any Clause")
                
                clause_text = st.text_area(
                    "Paste any confusing clause here:",
                    placeholder="Copy and paste the part of the document you want explained...",
                    height=100
                )
                
                col_explain, col_negotiate = st.columns([1, 1])
                
                with col_explain:
                    if st.button("🧠 Explain This Clause", type="primary"):
                        if clause_text.strip():
                            with st.spinner("🤔 Analyzing clause..."):
                                explanation = explain_clause(clause_text)
                            
                            st.markdown(f"""
                            <div class="explanation-box">
                                <h4>💡 Your Personal Legal Translator</h4>
                                <p>{explanation}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.warning("Please paste a clause to explain!")
                
                with col_negotiate:
                    if clause_text.strip():
                        if st.button("📧 Generate Negotiation Email", type="secondary"):
                            with st.spinner("✍️ Crafting your negotiation email..."):
                                negotiation_email = generate_negotiation_email(clause_text)
                            
                            st.markdown(f"""
                            <div class="negotiation-box">
                                <h4>📧 Your Negotiation Email</h4>
                                <p>{negotiation_email}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Copy button
                            st.code(negotiation_email, language=None)
                            st.info("💡 Copy the email above and send it to negotiate better terms!")
                
                # What If Simulator
                st.header("🎭 'What If?' Simulator")
                
                what_if_question = st.text_input(
                    "Ask me anything:",
                    placeholder="e.g., 'What if I break my lease?' or 'What if I can't pay on time?'"
                )
                
                if st.button("🔮 Simulate This Scenario"):
                    if what_if_question.strip():
                        with st.spinner("🔮 Simulating scenario..."):
                            simulation = simulate_what_if(what_if_question, document_text)
                        
                        # Check for easter egg response
                        if "You're not alone" in simulation:
                            st.markdown(f"""
                            <div class="easter-egg">
                                <h3>💝 {simulation}</h3>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class="what-if-box">
                                <h4>🎭 Scenario Simulation</h4>
                                <p>{simulation}</p>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.warning("Please ask a 'What if?' question!")
            
            else:
                st.error("❌ Could not read the PDF. Please try a different file.")
    
    with col2:
        st.header("🌟 Why LexPlain AI?")
        
        st.markdown("""
        <div style="background-color: #f0f8ff; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            <h4>📄 Smart Summaries</h4>
            <p>Get instant 3-line summaries of complex legal documents. Know what you're signing!</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background-color: #fff0f5; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            <h4>🖼 Image Analysis</h4>
            <p>Upload photos of documents! We can read text from images using Google Document AI OCR. Perfect for handwritten notes, screenshots, or scanned documents!</p>
        </div>
        """, unsafe_allow_html=True)
        
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
        - **Smart**: OCR for scanned docs, summaries for quick understanding
        """)
        
        st.markdown("---")
        
        st.markdown("### 🏆 Hackathon Features")
        st.markdown("""
        ✨ **PDF Summaries** - 3-line plain-English summaries
        ✨ **Image Analysis** - Upload photos of documents for OCR
        ✨ **OCR Support** - Reads scanned PDFs and images
        ✨ **What If? Simulator** - Real consequences from YOUR doc
        ✨ **Risk Radar** - Color-coded danger zones  
        ✨ **Negotiation Coach** - Ready-to-send emails
        ✨ **Easter Egg** - Type "I'm scared" for support
        ✨ **Clean Architecture** - Production-ready modular code
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p>⚖️ <strong>LexPlain AI</strong> - Making Legal Documents Human-Friendly</p>
        <p><em>Built with ❤️ for hackathon judges who believe in empowering people</em></p>
        <p>🔒 Your privacy matters - no data stored, no tracking, just protection</p>
        <p>🏗️ <strong>Production-Ready Architecture</strong> - Clean separation of concerns</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
