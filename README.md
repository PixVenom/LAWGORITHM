# Legal Document Simplifier

An AI-powered web application that simplifies legal documents by providing OCR text extraction, clause segmentation, risk assessment, AI-generated summaries, and an interactive chatbot for document analysis.

## Features

### 🔍 Document Analysis
- **OCR Text Extraction**: Extract text from PDFs and images using Google Vision API or Tesseract OCR
- **Language Detection**: Automatically detect document language
- **Clause Segmentation**: Break down legal documents into individual clauses
- **Risk Assessment**: Identify and color-code high, medium, and low-risk clauses

### 🤖 AI-Powered Summaries
- **Explain Like I'm 5 (ELI5)**: Simple explanations using everyday language
- **Plain Language**: Clear, jargon-free summaries
- **Detailed Summary**: Comprehensive analysis with key elements

### 💬 Interactive Chatbot
- **Document Q&A**: Ask questions about the uploaded document
- **Legal Term Explanations**: Get simplified explanations of legal jargon
- **Risk Insights**: Understand potential risks and concerns
- **Suggested Questions**: Pre-built questions to get started

### 📊 Risk Dashboard
- **Visual Risk Charts**: Pie charts and bar graphs showing risk distribution
- **Risk Factors**: Detailed breakdown of identified risk factors
- **Color-coded Clauses**: Easy identification of risk levels
- **Risk Recommendations**: AI-generated advice based on analysis

### 📄 Export & Reporting
- **PDF Export**: Generate comprehensive analysis reports
- **Copy to Clipboard**: Easy sharing of summaries and explanations

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Google Cloud Vision API**: OCR text extraction
- **Google Cloud Translation API**: Language detection
- **OpenAI API**: AI summarization and chatbot
- **Transformers**: Local AI models (BART, Pegasus)
- **ReportLab**: PDF generation
- **Pytesseract**: Fallback OCR

### Frontend
- **React 18**: Modern React with hooks
- **Material-UI (MUI)**: Beautiful, responsive UI components
- **Lottie React**: Smooth animations
- **React Dropzone**: File upload with drag & drop
- **Axios**: HTTP client for API calls
- **MUI X Charts**: Data visualization

## Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn
- Google Cloud account (optional, for enhanced OCR)
- OpenAI API key (optional, for enhanced AI features)

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp env.example .env
   ```
   
   Edit `.env` file with your configuration:
   ```env
   # Google Cloud Configuration (Optional)
   GOOGLE_APPLICATION_CREDENTIALS=path/to/your/service-account-key.json
   GOOGLE_CLOUD_PROJECT_ID=your-project-id
   
   # OpenAI Configuration (Optional)
   OPENAI_API_KEY=your-openai-api-key
   
   # Application Configuration
   DEBUG=True
   HOST=0.0.0.0
   PORT=8000
   CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
   
   # OCR Configuration
   USE_GOOGLE_VISION=True
   TESSERACT_PATH=/usr/bin/tesseract
   ```

5. **Install Tesseract OCR** (for fallback):
   ```bash
   # Ubuntu/Debian
   sudo apt-get install tesseract-ocr
   
   # macOS
   brew install tesseract
   
   # Windows
   # Download from: https://github.com/UB-Mannheim/tesseract/wiki
   ```

6. **Run the backend**:
   ```bash
   python main.py
   ```

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm start
   ```

4. **Open your browser**:
   Navigate to `http://localhost:3000`

## Usage

### 1. Upload Document
- Drag and drop a PDF or image file
- Supported formats: PDF, PNG, JPG, JPEG, GIF, BMP, TIFF
- Maximum file size: 10MB

### 2. View Analysis Results
- **Summaries Tab**: View ELI5, Plain Language, and Detailed summaries
- **Original Text Tab**: See the extracted text from your document
- **Clauses Tab**: Browse individual clauses with confidence scores

### 3. Risk Assessment
- **Risk Dashboard**: Visual overview of risk distribution
- **Risk Charts**: Pie charts and bar graphs
- **Detailed Analysis**: Expandable clauses with risk factors
- **Risk Recommendations**: AI-generated advice

### 4. Chat with AI
- Ask questions about the document
- Get explanations of legal terms
- Use suggested questions to get started
- Copy responses for easy sharing

### 5. Export Results
- Click "Export PDF Report" to download a comprehensive analysis
- Copy individual summaries to clipboard

## API Endpoints

### Document Upload
```
POST /upload
Content-Type: multipart/form-data
Body: file (PDF or image)
```

### Chat with Document
```
POST /chat
Content-Type: application/json
Body: {
  "message": "Your question",
  "document_context": "Document text (optional)"
}
```

### Export PDF
```
POST /export-pdf
Content-Type: application/json
Body: Document analysis data
```

### Health Check
```
GET /health
```

## Configuration Options

### OCR Configuration
- **Google Vision API**: High accuracy, requires Google Cloud setup
- **Tesseract OCR**: Free, local processing, good for basic needs
- **Fallback**: Automatic fallback if primary OCR fails

### AI Services
- **OpenAI API**: High-quality summaries and chatbot responses
- **Local Models**: BART and Pegasus for offline processing
- **Fallback**: Rule-based responses when AI services unavailable

### Risk Assessment
- **Pattern Matching**: Identifies common legal risk patterns
- **Machine Learning**: Enhanced risk scoring (future feature)
- **Customizable**: Risk patterns can be modified in code

## Deployment

### Docker Deployment (Recommended)

1. **Build backend image**:
   ```bash
   cd backend
   docker build -t legal-doc-backend .
   ```

2. **Build frontend image**:
   ```bash
   cd frontend
   docker build -t legal-doc-frontend .
   ```

3. **Run with docker-compose**:
   ```bash
   docker-compose up -d
   ```

### Cloud Deployment

#### Google Cloud Run
1. **Deploy backend**:
   ```bash
   gcloud run deploy legal-doc-backend --source backend
   ```

2. **Deploy frontend**:
   ```bash
   gcloud run deploy legal-doc-frontend --source frontend
   ```

#### AWS/Azure
- Use similar container deployment strategies
- Ensure environment variables are properly configured
- Set up proper CORS origins for production

## Development

### Project Structure
```
legal-doc-simplifier/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── services/               # Business logic services
│   │   ├── ocr_service.py      # OCR text extraction
│   │   ├── language_service.py # Language detection
│   │   ├── segmentation_service.py # Clause segmentation
│   │   ├── summarization_service.py # AI summarization
│   │   ├── risk_service.py     # Risk assessment
│   │   ├── chatbot_service.py  # AI chatbot
│   │   └── pdf_service.py      # PDF generation
│   ├── requirements.txt        # Python dependencies
│   └── env.example            # Environment variables template
├── frontend/
│   ├── src/
│   │   ├── components/         # React components
│   │   │   ├── DocumentUpload.js
│   │   │   ├── DocumentAnalysis.js
│   │   │   ├── RiskChart.js
│   │   │   └── Chatbot.js
│   │   ├── animations/         # Lottie animations
│   │   ├── App.js             # Main React app
│   │   └── index.js           # React entry point
│   ├── public/                # Static assets
│   └── package.json           # Node.js dependencies
└── README.md                  # This file
```

### Adding New Features

1. **Backend Services**: Add new services in `backend/services/`
2. **API Endpoints**: Extend `main.py` with new routes
3. **Frontend Components**: Create new React components in `src/components/`
4. **Styling**: Use Material-UI theme system for consistent styling

### Testing

1. **Backend Tests**:
   ```bash
   cd backend
   python -m pytest tests/
   ```

2. **Frontend Tests**:
   ```bash
   cd frontend
   npm test
   ```

## Troubleshooting

### Common Issues

1. **OCR Not Working**:
   - Check Tesseract installation
   - Verify Google Cloud credentials
   - Check file format support

2. **AI Services Failing**:
   - Verify API keys in environment variables
   - Check internet connectivity
   - Review API rate limits

3. **Frontend Not Loading**:
   - Ensure backend is running on port 8000
   - Check CORS configuration
   - Verify proxy settings in package.json

4. **File Upload Issues**:
   - Check file size limits (10MB)
   - Verify supported file formats
   - Check browser console for errors

### Performance Optimization

1. **Large Documents**:
   - Consider chunking for very large files
   - Implement progress indicators
   - Add timeout handling

2. **AI Response Times**:
   - Use local models for faster responses
   - Implement caching for repeated queries
   - Add loading states

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the API documentation

## Roadmap

### Version 2.0
- [ ] Multi-language support
- [ ] Advanced risk scoring with ML
- [ ] Document comparison features
- [ ] Batch processing
- [ ] User authentication
- [ ] Document history

### Version 3.0
- [ ] Mobile app
- [ ] Real-time collaboration
- [ ] Advanced analytics
- [ ] Integration with legal databases
- [ ] Custom AI model training

---

**Built with ❤️ for making legal documents accessible to everyone.**
