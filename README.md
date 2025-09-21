# LexPlain AI - Your Legal Guardian Angel
#**running on: https://doc-ai-jjt4.onrender.com**
A compassionate legal document explainer that empowers non-lawyers with AI-powered insights. Built with clean, modular architecture for hackathon success.

## 🚀 Quick Start

1. **Clone and Setup**
   ```bash
   git clone <your-repo>
   cd lexplain-ai
   pip install -r requirements.txt
   ```

2. **Environment Setup**
   ```bash
   # Copy the example env file
   cp .env.example .env
   
   # Edit .env with your API keys
   GEMINI_KEY=your_gemini_api_key_here
   GOOGLE_APPLICATION_CREDENTIALS=path/to/your/service-account-key.json
   ```

3. **Run the App**
   ```bash
   streamlit run frontend/app.py
   ```

## 🏗️ Project Structure

```
lexplain-ai/
├── .env                          # Environment variables
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── frontend/
│   └── app.py                   # Streamlit UI (clean, no AI logic)
└── backend/
    ├── __init__.py              # Backend module init
    ├── ai_engine.py             # All Gemini AI logic
    ├── pdf_processor.py         # PDF text extraction + OCR fallback
    └── ocr_engine.py            # Google Document AI OCR
```

## ✨ Features

### 🎯 Core Features
- **📄 PDF Summaries**: 3-line plain-English document summaries
- **🖼 OCR Support**: Reads scanned PDFs using Google Document AI
- **⚠️ Risk Radar**: Color-coded risk analysis (🟢🟡🔴)
- **🧠 What If? Simulator**: Real consequences from YOUR document
- **💬 Negotiation Coach**: Ready-to-send professional emails
- **🔒 Private Mode**: No data stored, complete privacy

### 🏆 Hackathon-Winning Features
- **Clean Architecture**: Separation of concerns, production-ready
- **Easter Egg**: Type "I'm scared" for emotional support
- **Loading States**: Beautiful spinners and error handling
- **Mobile-Friendly**: Responsive design for all devices
- **OCR Badge**: Shows when Document AI was used

## 🛠️ Technical Stack

- **Frontend**: Streamlit (clean UI only)
- **Backend**: Modular Python with clear separation
- **AI**: Google Gemini 1.5 Pro
- **OCR**: Google Document AI
- **PDF**: PyPDF2 with OCR fallback
- **Environment**: python-dotenv

## 🔧 API Keys Required

1. **Gemini API Key**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Google Cloud Credentials**: For Document AI OCR
   - Create a service account
   - Download JSON key file
   - Set path in `.env`

## 💡 Usage

1. Upload any legal document (PDF)
2. Get instant summary with "📄 Get 3-Line Summary"
3. Review risk analysis with color-coded warnings
4. Ask "What if?" questions for scenario simulation
5. Generate negotiation emails for unfair clauses
6. Feel empowered! 💪

## 🎨 Design Philosophy

- **Warm & Protective**: Like a wise friend who has your back
- **Empowering**: Helps you negotiate, not just understand
- **Private**: Your documents never leave your device
- **Real**: Based on YOUR specific document, not generic advice

## 🏆 Why This Wins Hackathons

1. **Production-Ready Architecture**: Clean separation of concerns
2. **Complete Feature Set**: OCR, summaries, simulations, negotiations
3. **Emotional Design**: Easter eggs, warm tone, empowering language
4. **Technical Excellence**: Error handling, loading states, mobile-friendly
5. **Real-World Impact**: Solves actual problems people face

## 🔒 Privacy & Security

- No data is stored anywhere
- All processing happens in real-time
- Private mode ensures complete privacy
- No tracking or analytics

## 🆘 Support

- **Free Legal Aid**: 1-800-555-LEGAL
- **Emergency**: 911
- **Easter Egg**: Type "I'm scared" in What If? simulator

---

Built with ❤️ for hackathon judges who believe in empowering people through technology.

