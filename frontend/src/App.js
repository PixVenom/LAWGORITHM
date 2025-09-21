import React, { useState } from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Container,
  Box,
  Paper,
  Tabs,
  Tab,
  Alert,
  Snackbar,
  Fade,
  Slide,
  Chip,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  Gavel,
  Analytics,
  Chat,
  Upload,
  Download,
  Info,
} from '@mui/icons-material';
import { styled, alpha } from '@mui/material/styles';
import DocumentUpload from './components/DocumentUpload';
import DocumentAnalysis from './components/DocumentAnalysis';
import Chatbot from './components/Chatbot';
import RiskChart from './components/RiskChart';

const StyledContainer = styled(Container)(({ theme }) => ({
  marginTop: theme.spacing(4),
  marginBottom: theme.spacing(4),
}));

const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(4),
  marginBottom: theme.spacing(3),
  borderRadius: theme.spacing(2),
  boxShadow: `0 8px 32px ${alpha(theme.palette.primary.main, 0.1)}`,
  background: `linear-gradient(135deg, ${theme.palette.background.paper} 0%, ${alpha(theme.palette.primary.main, 0.02)} 100%)`,
  border: `1px solid ${alpha(theme.palette.primary.main, 0.1)}`,
}));

const HeroSection = styled(Box)(({ theme }) => ({
  background: `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.primary.dark} 100%)`,
  color: theme.palette.primary.contrastText,
  padding: theme.spacing(6, 0),
  marginBottom: theme.spacing(4),
  borderRadius: theme.spacing(2),
  position: 'relative',
  overflow: 'hidden',
  '&::before': {
    content: '""',
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    background: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Ccircle cx='30' cy='30' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
  },
}));

const StyledTabs = styled(Tabs)(({ theme }) => ({
  '& .MuiTab-root': {
    minHeight: 60,
    fontSize: '1rem',
    fontWeight: 500,
    textTransform: 'none',
    '&.Mui-selected': {
      color: theme.palette.primary.main,
    },
  },
  '& .MuiTabs-indicator': {
    height: 3,
    borderRadius: '3px 3px 0 0',
  },
}));

const FeatureCard = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(3),
  textAlign: 'center',
  borderRadius: theme.spacing(2),
  background: `linear-gradient(135deg, ${theme.palette.background.paper} 0%, ${alpha(theme.palette.secondary.main, 0.05)} 100%)`,
  border: `1px solid ${alpha(theme.palette.secondary.main, 0.1)}`,
  transition: 'all 0.3s ease',
  '&:hover': {
    transform: 'translateY(-4px)',
    boxShadow: `0 12px 40px ${alpha(theme.palette.secondary.main, 0.15)}`,
  },
}));

function TabPanel({ children, value, index, ...other }) {
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Fade in={value === index} timeout={300}>
          <Box sx={{ p: 3 }}>{children}</Box>
        </Fade>
      )}
    </div>
  );
}

function App() {
  const [tabValue, setTabValue] = useState(0);
  const [documentData, setDocumentData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const handleDocumentUpload = async (file) => {
    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setDocumentData(data);
      setSuccess('Document analyzed successfully!');
      setTabValue(1); // Switch to analysis tab
    } catch (err) {
      setError(`Error analyzing document: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleExportPDF = async () => {
    if (!documentData) return;

    try {
      const response = await fetch('/export-pdf', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(documentData),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = 'legal_document_analysis.pdf';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      setSuccess('PDF exported successfully!');
    } catch (err) {
      setError(`Error exporting PDF: ${err.message}`);
    }
  };

  const handleCloseSnackbar = () => {
    setError(null);
    setSuccess(null);
  };

  return (
    <Box sx={{ flexGrow: 1, minHeight: '100vh', background: 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)' }}>
      <AppBar position="static" elevation={0} sx={{ 
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        backdropFilter: 'blur(10px)',
      }}>
        <Toolbar>
          <Gavel sx={{ mr: 2 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontWeight: 600 }}>
            Legal Document Simplifier
          </Typography>
          <Chip 
            label="AI-Powered" 
            color="secondary" 
            size="small" 
            sx={{ 
              background: 'rgba(255,255,255,0.2)', 
              color: 'white',
              fontWeight: 500,
            }} 
          />
        </Toolbar>
      </AppBar>

      <StyledContainer maxWidth="lg">
        <HeroSection>
          <Container maxWidth="md">
            <Box sx={{ position: 'relative', zIndex: 1 }}>
              <Typography variant="h3" component="h1" gutterBottom align="center" sx={{ fontWeight: 700, mb: 2 }}>
                Simplify Legal Documents
              </Typography>
              <Typography variant="h6" align="center" sx={{ opacity: 0.9, mb: 4, fontWeight: 400 }}>
                Upload any legal document and get instant AI-powered analysis, risk assessment, and plain-language explanations
              </Typography>
              
              <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2, flexWrap: 'wrap' }}>
                <Chip icon={<Upload />} label="Upload Document" color="secondary" />
                <Chip icon={<Analytics />} label="Risk Analysis" color="secondary" />
                <Chip icon={<Chat />} label="AI Chatbot" color="secondary" />
                <Chip icon={<Download />} label="Export Report" color="secondary" />
              </Box>
            </Box>
          </Container>
        </HeroSection>

        {/* Feature Cards */}
        <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: 'repeat(3, 1fr)' }, gap: 3, mb: 4 }}>
          <FeatureCard>
            <Upload sx={{ fontSize: 40, color: 'primary.main', mb: 2 }} />
            <Typography variant="h6" gutterBottom>Smart Upload</Typography>
            <Typography variant="body2" color="text.secondary">
              Drag & drop PDFs or images. Advanced OCR extracts text with high accuracy.
            </Typography>
          </FeatureCard>
          
          <FeatureCard>
            <Analytics sx={{ fontSize: 40, color: 'secondary.main', mb: 2 }} />
            <Typography variant="h6" gutterBottom>Risk Assessment</Typography>
            <Typography variant="body2" color="text.secondary">
              AI identifies high-risk clauses with color-coded visualizations and detailed explanations.
            </Typography>
          </FeatureCard>
          
          <FeatureCard>
            <Chat sx={{ fontSize: 40, color: 'success.main', mb: 2 }} />
            <Typography variant="h6" gutterBottom>AI Assistant</Typography>
            <Typography variant="body2" color="text.secondary">
              Ask questions about your document and get instant, accurate answers in plain language.
            </Typography>
          </FeatureCard>
        </Box>

        <StyledPaper elevation={3}>
          <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <StyledTabs value={tabValue} onChange={handleTabChange} aria-label="document analysis tabs">
              <Tab 
                icon={<Upload />} 
                label="Upload Document" 
                iconPosition="start"
                sx={{ minHeight: 60 }}
              />
              <Tab 
                icon={<Analytics />} 
                label="Analysis Results" 
                iconPosition="start"
                disabled={!documentData}
                sx={{ minHeight: 60 }}
              />
              <Tab 
                icon={<Info />} 
                label="Risk Assessment" 
                iconPosition="start"
                disabled={!documentData}
                sx={{ minHeight: 60 }}
              />
              <Tab 
                icon={<Chat />} 
                label="AI Chatbot" 
                iconPosition="start"
                disabled={!documentData}
                sx={{ minHeight: 60 }}
              />
            </StyledTabs>
          </Box>

          <TabPanel value={tabValue} index={0}>
            <DocumentUpload
              onUpload={handleDocumentUpload}
              loading={loading}
            />
          </TabPanel>

          <TabPanel value={tabValue} index={1}>
            {documentData && (
              <DocumentAnalysis
                documentData={documentData}
                onExportPDF={handleExportPDF}
              />
            )}
          </TabPanel>

          <TabPanel value={tabValue} index={2}>
            {documentData && (
              <RiskChart
                riskScores={documentData.risk_scores}
                clauses={documentData.clauses}
              />
            )}
          </TabPanel>

          <TabPanel value={tabValue} index={3}>
            {documentData && (
              <Chatbot
                documentContext={documentData.text}
                summaries={documentData.summaries}
              />
            )}
          </TabPanel>
        </StyledPaper>
      </StyledContainer>

      <Snackbar
        open={!!error}
        autoHideDuration={6000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
      >
        <Alert onClose={handleCloseSnackbar} severity="error" sx={{ width: '100%' }}>
          {error}
        </Alert>
      </Snackbar>

      <Snackbar
        open={!!success}
        autoHideDuration={4000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
      >
        <Alert onClose={handleCloseSnackbar} severity="success" sx={{ width: '100%' }}>
          {success}
        </Alert>
      </Snackbar>
    </Box>
  );
}

export default App;
