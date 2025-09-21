# Quick Start Guide

Get the Legal Document Simplifier running in 5 minutes!

## 🚀 One-Click Start (Recommended)

```bash
# Clone or download the project
cd legal-doc-simplifier

# Make startup script executable and run
chmod +x start.sh
./start.sh
```

That's it! The application will be available at:
- **Frontend**: http://localhost
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🔧 Manual Setup

### Option 1: Docker (Easiest)

```bash
# Start with Docker Compose
docker-compose up --build

# Access the application
open http://localhost
```

### Option 2: Local Development

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

#### Frontend
```bash
cd frontend
npm install
npm start
```

## 📝 First Steps

1. **Upload a Document**: Drag & drop a PDF or image file
2. **View Analysis**: Check the "Analysis Results" tab
3. **Assess Risks**: Review the "Risk Assessment" tab
4. **Ask Questions**: Use the "AI Chatbot" tab
5. **Export Report**: Download a PDF summary

## ⚙️ Configuration (Optional)

Edit `backend/.env` to add your API keys for enhanced features:

```env
# For better OCR (optional)
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
GOOGLE_CLOUD_PROJECT_ID=your-project-id

# For better AI summaries (optional)
OPENAI_API_KEY=your-openai-api-key
```

## 🆘 Troubleshooting

### Services won't start?
```bash
# Check logs
docker-compose logs

# Restart services
docker-compose down
docker-compose up --build
```

### OCR not working?
- The app works without API keys using local Tesseract OCR
- For better accuracy, add Google Cloud Vision API credentials

### AI features not working?
- The app includes fallback responses
- For enhanced AI, add OpenAI API key

## 🎯 What You Get

✅ **OCR Text Extraction** - Extract text from any PDF or image  
✅ **AI Summaries** - Three levels: ELI5, Plain Language, Detailed  
✅ **Risk Assessment** - Color-coded risk analysis  
✅ **Interactive Chatbot** - Ask questions about your document  
✅ **PDF Export** - Download comprehensive reports  
✅ **Responsive UI** - Works on desktop and mobile  

## 📞 Need Help?

- Check the full [README.md](README.md) for detailed documentation
- Review the [API documentation](http://localhost:8000/docs) when running
- Create an issue on GitHub for bugs or feature requests

---

**Ready to simplify legal documents? Start uploading! 🚀**
