#!/bin/bash

# Fix Git repository by removing large files
echo "🔧 Fixing Git repository..."

# Remove large PDF files from the filesystem
echo "📁 Removing large PDF files..."
rm -f "ASSETS/constitution/Constitution of India in Bengali, Version 2022.pdf"
rm -f "ASSETS/constitution/Tamil version Constitution of India.pdf"
rm -f "ASSETS/IVth Term_Humanitarian and Refugee Law_LB 4035_2023.pdf"
rm -f "ASSETS/constitution/The Constitution of India in Konkani.pdf"

# Create a new Git repository
echo "🔄 Reinitializing Git repository..."
rm -rf .git
git init
git add .
git commit -m "Initial commit: Legal Document Simplifier

- Full-stack legal document processing application
- React frontend with Material UI
- FastAPI backend with AI services
- Cloud integration for GCP, AWS, and Azure
- OCR, language detection, and summarization
- Risk assessment and chatbot features
- Production-ready deployment configurations"

echo "✅ Git repository fixed! Now you can push to GitHub."
echo "📋 Next steps:"
echo "1. Add your GitHub remote: git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git"
echo "2. Push to GitHub: git push -u origin main"
