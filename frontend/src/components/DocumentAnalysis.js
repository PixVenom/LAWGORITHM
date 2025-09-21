import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Tabs,
  Tab,
  Button,
  Chip,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Alert,
  Divider,
  Card,
  CardContent,
  Grid,
  IconButton,
  Tooltip,
  Fade,
  Zoom,
  LinearProgress,
  Avatar,
} from '@mui/material';
import {
  ExpandMore,
  Download,
  Language,
  Description,
  Assessment,
  Chat,
  ContentCopy,
  AutoAwesome,
  Psychology,
  School,
  TrendingUp,
  CheckCircle,
  Warning,
  Error,
} from '@mui/icons-material';
import { styled, alpha } from '@mui/material/styles';

const StyledCard = styled(Card)(({ theme }) => ({
  marginBottom: theme.spacing(2),
  borderRadius: theme.spacing(2),
  border: `1px solid ${alpha(theme.palette.primary.main, 0.1)}`,
  background: `linear-gradient(135deg, ${theme.palette.background.paper} 0%, ${alpha(theme.palette.primary.main, 0.02)} 100%)`,
  boxShadow: `0 4px 20px ${alpha(theme.palette.primary.main, 0.08)}`,
  transition: 'all 0.3s ease',
  '&:hover': {
    transform: 'translateY(-2px)',
    boxShadow: `0 8px 32px ${alpha(theme.palette.primary.main, 0.12)}`,
  },
}));

const SummaryCard = styled(Card)(({ theme, level }) => ({
  height: '100%',
  borderRadius: theme.spacing(2),
  border: `2px solid ${
    level === 'eli5' ? theme.palette.success.main :
    level === 'plain' ? theme.palette.info.main :
    theme.palette.warning.main
  }`,
  background: `linear-gradient(135deg, ${
    level === 'eli5' ? alpha(theme.palette.success.main, 0.05) :
    level === 'plain' ? alpha(theme.palette.info.main, 0.05) :
    alpha(theme.palette.warning.main, 0.05)
  } 0%, ${theme.palette.background.paper} 100%)`,
  transition: 'all 0.3s ease',
  '&:hover': {
    transform: 'translateY(-4px)',
    boxShadow: `0 12px 40px ${
      level === 'eli5' ? alpha(theme.palette.success.main, 0.2) :
      level === 'plain' ? alpha(theme.palette.info.main, 0.2) :
      alpha(theme.palette.warning.main, 0.2)
    }`,
  },
}));

const StatCard = styled(Card)(({ theme }) => ({
  borderRadius: theme.spacing(2),
  background: `linear-gradient(135deg, ${theme.palette.background.paper} 0%, ${alpha(theme.palette.secondary.main, 0.05)} 100%)`,
  border: `1px solid ${alpha(theme.palette.secondary.main, 0.1)}`,
  transition: 'all 0.3s ease',
  '&:hover': {
    transform: 'translateY(-2px)',
    boxShadow: `0 8px 32px ${alpha(theme.palette.secondary.main, 0.15)}`,
  },
}));

function TabPanel({ children, value, index, ...other }) {
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`analysis-tabpanel-${index}`}
      aria-labelledby={`analysis-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 2 }}>{children}</Box>}
    </div>
  );
}

function DocumentAnalysis({ documentData, onExportPDF }) {
  const [tabValue, setTabValue] = useState(0);
  const [copiedText, setCopiedText] = useState('');

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const handleCopyText = (text, label) => {
    navigator.clipboard.writeText(text);
    setCopiedText(label);
    setTimeout(() => setCopiedText(''), 2000);
  };

  const getLanguageName = (code) => {
    const languages = {
      'en': 'English',
      'es': 'Spanish',
      'fr': 'French',
      'de': 'German',
      'it': 'Italian',
      'pt': 'Portuguese',
      'ru': 'Russian',
      'zh': 'Chinese',
      'ja': 'Japanese',
      'ko': 'Korean',
      'ar': 'Arabic',
      'hi': 'Hindi',
    };
    return languages[code] || code;
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return 'success';
    if (confidence >= 0.6) return 'warning';
    return 'error';
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h5">
          Document Analysis Results
        </Typography>
        <Button
          variant="contained"
          startIcon={<Download />}
          onClick={onExportPDF}
          color="primary"
        >
          Export PDF Report
        </Button>
      </Box>

      {/* Document Information */}
      <Fade in timeout={600}>
        <StyledCard>
          <CardContent sx={{ p: 4 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3 }}>
              <Avatar sx={{ bgcolor: 'primary.main', width: 48, height: 48 }}>
                <Description />
              </Avatar>
              <Box>
                <Typography variant="h5" gutterBottom sx={{ fontWeight: 600 }}>
                  Document Analysis Results
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Comprehensive analysis completed successfully
                </Typography>
              </Box>
            </Box>
            
            <Grid container spacing={3}>
              <Grid item xs={12} sm={6} md={3}>
                <StatCard>
                  <CardContent sx={{ textAlign: 'center', p: 3 }}>
                    <Avatar sx={{ bgcolor: 'primary.main', width: 56, height: 56, mx: 'auto', mb: 2 }}>
                      <Language />
                    </Avatar>
                    <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                      {getLanguageName(documentData.language)}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Detected Language
                    </Typography>
                  </CardContent>
                </StatCard>
              </Grid>
              
              <Grid item xs={12} sm={6} md={3}>
                <StatCard>
                  <CardContent sx={{ textAlign: 'center', p: 3 }}>
                    <Avatar sx={{ bgcolor: getConfidenceColor(documentData.confidence) === 'success' ? 'success.main' : getConfidenceColor(documentData.confidence) === 'warning' ? 'warning.main' : 'error.main', width: 56, height: 56, mx: 'auto', mb: 2 }}>
                      <TrendingUp />
                    </Avatar>
                    <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                      {(documentData.confidence * 100).toFixed(1)}%
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Analysis Confidence
                    </Typography>
                    <LinearProgress 
                      variant="determinate" 
                      value={documentData.confidence * 100} 
                      color={getConfidenceColor(documentData.confidence)}
                      sx={{ mt: 1, borderRadius: 1 }}
                    />
                  </CardContent>
                </StatCard>
              </Grid>
              
              <Grid item xs={12} sm={6} md={3}>
                <StatCard>
                  <CardContent sx={{ textAlign: 'center', p: 3 }}>
                    <Avatar sx={{ bgcolor: 'secondary.main', width: 56, height: 56, mx: 'auto', mb: 2 }}>
                      <Assessment />
                    </Avatar>
                    <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                      {documentData.clauses?.length || 0}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Segmented Clauses
                    </Typography>
                  </CardContent>
                </StatCard>
              </Grid>
              
              <Grid item xs={12} sm={6} md={3}>
                <StatCard>
                  <CardContent sx={{ textAlign: 'center', p: 3 }}>
                    <Avatar sx={{ bgcolor: 'info.main', width: 56, height: 56, mx: 'auto', mb: 2 }}>
                      <Chat />
                    </Avatar>
                    <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                      {(documentData.text?.length || 0).toLocaleString()}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Characters Extracted
                    </Typography>
                  </CardContent>
                </StatCard>
              </Grid>
            </Grid>
          </CardContent>
        </StyledCard>
      </Fade>

      {/* Analysis Tabs */}
      <Paper sx={{ mt: 2 }}>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs value={tabValue} onChange={handleTabChange} aria-label="analysis tabs">
            <Tab label="Summaries" />
            <Tab label="Original Text" />
            <Tab label="Clauses" />
          </Tabs>
        </Box>

        <TabPanel value={tabValue} index={0}>
          <Box sx={{ textAlign: 'center', mb: 4 }}>
            <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, color: 'primary.main' }}>
              AI-Generated Summaries
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Three levels of analysis to help you understand your document
            </Typography>
          </Box>
          
          <Grid container spacing={3}>
            <Grid item xs={12} md={4}>
              <Zoom in timeout={600}>
                <SummaryCard level="eli5">
                  <CardContent sx={{ p: 3 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3 }}>
                      <Avatar sx={{ bgcolor: 'success.main', width: 48, height: 48 }}>
                        <School />
                      </Avatar>
                      <Box sx={{ flex: 1 }}>
                        <Typography variant="h6" color="success.main" sx={{ fontWeight: 600 }}>
                          Explain Like I'm 5
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Simple explanations
                        </Typography>
                      </Box>
                      <Tooltip title="Copy text">
                        <IconButton
                          size="small"
                          onClick={() => handleCopyText(documentData.summaries?.eli5 || '', 'ELI5')}
                        >
                          <ContentCopy fontSize="small" />
                        </IconButton>
                      </Tooltip>
                    </Box>
                    <Typography variant="body2" color="text.secondary" sx={{ lineHeight: 1.6 }}>
                      {documentData.summaries?.eli5 || 'No summary available'}
                    </Typography>
                    {copiedText === 'ELI5' && (
                      <Alert severity="success" sx={{ mt: 2 }}>
                        Copied to clipboard!
                      </Alert>
                    )}
                  </CardContent>
                </SummaryCard>
              </Zoom>
            </Grid>
            
            <Grid item xs={12} md={4}>
              <Zoom in timeout={800}>
                <SummaryCard level="plain">
                  <CardContent sx={{ p: 3 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3 }}>
                      <Avatar sx={{ bgcolor: 'info.main', width: 48, height: 48 }}>
                        <Psychology />
                      </Avatar>
                      <Box sx={{ flex: 1 }}>
                        <Typography variant="h6" color="info.main" sx={{ fontWeight: 600 }}>
                          Plain Language
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Clear & concise
                        </Typography>
                      </Box>
                      <Tooltip title="Copy text">
                        <IconButton
                          size="small"
                          onClick={() => handleCopyText(documentData.summaries?.plain_language || '', 'Plain')}
                        >
                          <ContentCopy fontSize="small" />
                        </IconButton>
                      </Tooltip>
                    </Box>
                    <Typography variant="body2" color="text.secondary" sx={{ lineHeight: 1.6 }}>
                      {documentData.summaries?.plain_language || 'No summary available'}
                    </Typography>
                    {copiedText === 'Plain' && (
                      <Alert severity="success" sx={{ mt: 2 }}>
                        Copied to clipboard!
                      </Alert>
                    )}
                  </CardContent>
                </SummaryCard>
              </Zoom>
            </Grid>
            
            <Grid item xs={12} md={4}>
              <Zoom in timeout={1000}>
                <SummaryCard level="detailed">
                  <CardContent sx={{ p: 3 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3 }}>
                      <Avatar sx={{ bgcolor: 'warning.main', width: 48, height: 48 }}>
                        <AutoAwesome />
                      </Avatar>
                      <Box sx={{ flex: 1 }}>
                        <Typography variant="h6" color="warning.main" sx={{ fontWeight: 600 }}>
                          Detailed Summary
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Comprehensive analysis
                        </Typography>
                      </Box>
                      <Tooltip title="Copy text">
                        <IconButton
                          size="small"
                          onClick={() => handleCopyText(documentData.summaries?.detailed || '', 'Detailed')}
                        >
                          <ContentCopy fontSize="small" />
                        </IconButton>
                      </Tooltip>
                    </Box>
                    <Typography variant="body2" color="text.secondary" sx={{ lineHeight: 1.6 }}>
                      {documentData.summaries?.detailed || 'No summary available'}
                    </Typography>
                    {copiedText === 'Detailed' && (
                      <Alert severity="success" sx={{ mt: 2 }}>
                        Copied to clipboard!
                      </Alert>
                    )}
                  </CardContent>
                </SummaryCard>
              </Zoom>
            </Grid>
          </Grid>
        </TabPanel>

        <TabPanel value={tabValue} index={1}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h6">
              Original Document Text
            </Typography>
            <Tooltip title="Copy text">
              <IconButton
                onClick={() => handleCopyText(documentData.text || '', 'Original')}
              >
                <ContentCopy />
              </IconButton>
            </Tooltip>
          </Box>
          <Paper sx={{ p: 2, maxHeight: 400, overflow: 'auto' }}>
            <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap' }}>
              {documentData.text || 'No text available'}
            </Typography>
          </Paper>
          {copiedText === 'Original' && (
            <Alert severity="success" sx={{ mt: 1 }}>
              Copied to clipboard!
            </Alert>
          )}
        </TabPanel>

        <TabPanel value={tabValue} index={2}>
          <Typography variant="h6" gutterBottom>
            Document Clauses
          </Typography>
          {documentData.clauses?.map((clause, index) => (
            <Accordion key={clause.id || index} sx={{ mb: 1 }}>
              <AccordionSummary expandIcon={<ExpandMore />}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, width: '100%' }}>
                  <Typography variant="subtitle1">
                    Clause {clause.id || index + 1}
                  </Typography>
                  <Chip
                    label={clause.type || 'general'}
                    color="primary"
                    size="small"
                  />
                  <Chip
                    label={`${(clause.confidence * 100).toFixed(0)}% confidence`}
                    color={getConfidenceColor(clause.confidence)}
                    size="small"
                    variant="outlined"
                  />
                </Box>
              </AccordionSummary>
              <AccordionDetails>
                <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap' }}>
                  {clause.text || 'No text available'}
                </Typography>
                <Divider sx={{ my: 2 }} />
                <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                  <Typography variant="caption" color="text.secondary">
                    Start: {clause.start_index || 0} | End: {clause.end_index || 0}
                  </Typography>
                </Box>
              </AccordionDetails>
            </Accordion>
          )) || (
            <Alert severity="info">
              No clauses found in the document.
            </Alert>
          )}
        </TabPanel>
      </Paper>
    </Box>
  );
}

export default DocumentAnalysis;
