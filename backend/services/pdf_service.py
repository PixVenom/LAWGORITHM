import os
import logging
from typing import Dict, Any
import asyncio
import tempfile
from datetime import datetime

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

logger = logging.getLogger(__name__)

class PDFService:
    def __init__(self):
        if not REPORTLAB_AVAILABLE:
            logger.warning("ReportLab not available. PDF export will not work.")
    
    async def create_pdf(self, document_data: Dict[str, Any]) -> str:
        """
        Create a PDF report from document analysis data
        """
        try:
            if not REPORTLAB_AVAILABLE:
                raise Exception("ReportLab library not available")
            
            # Create temporary file for PDF
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                pdf_path = tmp_file.name
            
            # Run PDF creation in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None, self._create_pdf_content, pdf_path, document_data
            )
            
            return pdf_path
            
        except Exception as e:
            logger.error(f"Error creating PDF: {e}")
            raise
    
    def _create_pdf_content(self, pdf_path: str, document_data: Dict[str, Any]):
        """
        Create the actual PDF content
        """
        try:
            # Create PDF document
            doc = SimpleDocTemplate(pdf_path, pagesize=A4)
            styles = getSampleStyleSheet()
            
            # Define custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                spaceAfter=30,
                alignment=TA_CENTER,
                textColor=colors.darkblue
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=14,
                spaceAfter=12,
                textColor=colors.darkblue
            )
            
            subheading_style = ParagraphStyle(
                'CustomSubHeading',
                parent=styles['Heading3'],
                fontSize=12,
                spaceAfter=8,
                textColor=colors.darkgreen
            )
            
            normal_style = ParagraphStyle(
                'CustomNormal',
                parent=styles['Normal'],
                fontSize=10,
                spaceAfter=6,
                alignment=TA_JUSTIFY
            )
            
            # Build content
            content = []
            
            # Title
            content.append(Paragraph("Legal Document Analysis Report", title_style))
            content.append(Spacer(1, 20))
            
            # Document information
            content.append(Paragraph("Document Information", heading_style))
            content.append(Paragraph(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal_style))
            content.append(Paragraph(f"Language: {document_data.get('language', 'Unknown')}", normal_style))
            content.append(Paragraph(f"Confidence: {document_data.get('confidence', 0):.2f}", normal_style))
            content.append(Spacer(1, 20))
            
            # Original text (truncated)
            content.append(Paragraph("Original Document Text", heading_style))
            original_text = document_data.get('text', '')
            if len(original_text) > 1000:
                original_text = original_text[:1000] + "... [truncated]"
            content.append(Paragraph(original_text, normal_style))
            content.append(Spacer(1, 20))
            
            # Summaries
            content.append(Paragraph("Document Summaries", heading_style))
            
            summaries = document_data.get('summaries', {})
            
            # ELI5 Summary
            if 'eli5' in summaries:
                content.append(Paragraph("Explain Like I'm 5", subheading_style))
                content.append(Paragraph(summaries['eli5'], normal_style))
                content.append(Spacer(1, 10))
            
            # Plain Language Summary
            if 'plain_language' in summaries:
                content.append(Paragraph("Plain Language Summary", subheading_style))
                content.append(Paragraph(summaries['plain_language'], normal_style))
                content.append(Spacer(1, 10))
            
            # Detailed Summary
            if 'detailed' in summaries:
                content.append(Paragraph("Detailed Summary", subheading_style))
                content.append(Paragraph(summaries['detailed'], normal_style))
                content.append(Spacer(1, 20))
            
            # Risk Analysis
            content.append(Paragraph("Risk Analysis", heading_style))
            
            risk_scores = document_data.get('risk_scores', [])
            if risk_scores:
                # Create risk summary table
                risk_data = [['Clause ID', 'Risk Level', 'Risk Score', 'Risk Factors']]
                
                for risk in risk_scores:
                    risk_data.append([
                        str(risk.get('clause_id', '')),
                        risk.get('risk_level', '').title(),
                        f"{risk.get('risk_score', 0):.2f}",
                        ', '.join(risk.get('risk_factors', []))[:50] + '...' if len(', '.join(risk.get('risk_factors', []))) > 50 else ', '.join(risk.get('risk_factors', []))
                    ])
                
                risk_table = Table(risk_data, colWidths=[1*inch, 1.2*inch, 1*inch, 2.5*inch])
                risk_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                content.append(risk_table)
                content.append(Spacer(1, 20))
            
            # Clause Analysis
            content.append(Paragraph("Clause Analysis", heading_style))
            
            clauses = document_data.get('clauses', [])
            for i, clause in enumerate(clauses[:10]):  # Limit to first 10 clauses
                clause_id = clause.get('id', i+1)
                clause_text = clause.get('text', '')
                clause_type = clause.get('type', 'unknown')
                
                # Truncate long clauses
                if len(clause_text) > 300:
                    clause_text = clause_text[:300] + "... [truncated]"
                
                content.append(Paragraph(f"Clause {clause_id} ({clause_type.title()})", subheading_style))
                content.append(Paragraph(clause_text, normal_style))
                
                # Add risk information if available
                clause_risk = next((r for r in risk_scores if r.get('clause_id') == clause_id), None)
                if clause_risk:
                    risk_level = clause_risk.get('risk_level', 'unknown')
                    risk_explanation = clause_risk.get('explanation', '')
                    content.append(Paragraph(f"Risk Level: {risk_level.title()}", normal_style))
                    content.append(Paragraph(f"Risk Explanation: {risk_explanation}", normal_style))
                
                content.append(Spacer(1, 10))
            
            if len(clauses) > 10:
                content.append(Paragraph(f"... and {len(clauses) - 10} more clauses", normal_style))
            
            # Footer
            content.append(Spacer(1, 30))
            content.append(Paragraph("Generated by Legal Document Simplifier", 
                                   ParagraphStyle('Footer', parent=styles['Normal'], 
                                                fontSize=8, alignment=TA_CENTER, 
                                                textColor=colors.grey)))
            
            # Build PDF
            doc.build(content)
            
        except Exception as e:
            logger.error(f"Error creating PDF content: {e}")
            raise
    
    async def create_simple_pdf(self, text: str, filename: str = "document.pdf") -> str:
        """
        Create a simple PDF with just the text content
        """
        try:
            if not REPORTLAB_AVAILABLE:
                raise Exception("ReportLab library not available")
            
            # Create temporary file for PDF
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                pdf_path = tmp_file.name
            
            # Run PDF creation in thread pool
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None, self._create_simple_pdf_content, pdf_path, text
            )
            
            return pdf_path
            
        except Exception as e:
            logger.error(f"Error creating simple PDF: {e}")
            raise
    
    def _create_simple_pdf_content(self, pdf_path: str, text: str):
        """
        Create simple PDF content
        """
        try:
            doc = SimpleDocTemplate(pdf_path, pagesize=A4)
            styles = getSampleStyleSheet()
            
            content = []
            content.append(Paragraph("Legal Document", styles['Title']))
            content.append(Spacer(1, 20))
            content.append(Paragraph(text, styles['Normal']))
            
            doc.build(content)
            
        except Exception as e:
            logger.error(f"Error creating simple PDF content: {e}")
            raise
