import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import {
  Box,
  Paper,
  Typography,
  Button,
  LinearProgress,
  Alert,
  Chip,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Fade,
  Zoom,
  Card,
  CardContent,
  Grid,
  Divider,
} from '@mui/material';
import {
  CloudUpload,
  Description,
  Image,
  CheckCircle,
  Error,
  Security,
  Speed,
  Psychology,
  Assessment,
  AutoAwesome,
} from '@mui/icons-material';
import { styled, alpha, keyframes } from '@mui/material/styles';

const pulse = keyframes`
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
  100% {
    transform: scale(1);
  }
`;

const DropzonePaper = styled(Paper)(({ theme, isDragActive }) => ({
  padding: theme.spacing(6),
  textAlign: 'center',
  border: `3px dashed ${isDragActive ? theme.palette.primary.main : theme.palette.grey[300]}`,
  backgroundColor: isDragActive 
    ? `linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.1)} 0%, ${alpha(theme.palette.primary.main, 0.05)} 100%)`
    : `linear-gradient(135deg, ${theme.palette.background.paper} 0%, ${alpha(theme.palette.primary.main, 0.02)} 100%)`,
  cursor: 'pointer',
  transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
  borderRadius: theme.spacing(3),
  position: 'relative',
  overflow: 'hidden',
  '&:hover': {
    borderColor: theme.palette.primary.main,
    backgroundColor: `linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.1)} 0%, ${alpha(theme.palette.primary.main, 0.05)} 100%)`,
    transform: 'translateY(-2px)',
    boxShadow: `0 8px 32px ${alpha(theme.palette.primary.main, 0.2)}`,
  },
  '&::before': {
    content: '""',
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    background: isDragActive 
      ? `radial-gradient(circle at center, ${alpha(theme.palette.primary.main, 0.1)} 0%, transparent 70%)`
      : 'none',
    animation: isDragActive ? `${pulse} 2s infinite` : 'none',
  },
}));

const FeatureCard = styled(Card)(({ theme }) => ({
  height: '100%',
  borderRadius: theme.spacing(2),
  background: `linear-gradient(135deg, ${theme.palette.background.paper} 0%, ${alpha(theme.palette.secondary.main, 0.05)} 100%)`,
  border: `1px solid ${alpha(theme.palette.secondary.main, 0.1)}`,
  transition: 'all 0.3s ease',
  '&:hover': {
    transform: 'translateY(-4px)',
    boxShadow: `0 12px 40px ${alpha(theme.palette.secondary.main, 0.15)}`,
  },
}));

const FeatureList = styled(List)(({ theme }) => ({
  marginTop: theme.spacing(3),
  textAlign: 'left',
}));

function DocumentUpload({ onUpload, loading }) {
  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      onUpload(acceptedFiles[0]);
    }
  }, [onUpload]);

  const { getRootProps, getInputProps, isDragActive, fileRejections } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'image/*': ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'],
    },
    maxFiles: 1,
    maxSize: 10 * 1024 * 1024, // 10MB
  });

  const getFileIcon = (file) => {
    if (file.type === 'application/pdf') {
      return <Description color="error" />;
    }
    return <Image color="primary" />;
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <Box>
      <Box sx={{ textAlign: 'center', mb: 4 }}>
        <Typography variant="h4" gutterBottom sx={{ fontWeight: 600, color: 'primary.main' }}>
          Upload Legal Document
        </Typography>
        <Typography variant="h6" color="text.secondary" paragraph sx={{ maxWidth: 600, mx: 'auto' }}>
          Upload a PDF or image file to get AI-powered analysis, risk assessment, and simplified explanations.
        </Typography>
      </Box>

      <Zoom in timeout={500}>
        <DropzonePaper
          {...getRootProps()}
          isDragActive={isDragActive}
          elevation={0}
        >
          <input {...getInputProps()} />
          
          <Box sx={{ position: 'relative', zIndex: 1 }}>
            <CloudUpload
              sx={{
                fontSize: 80,
                color: isDragActive ? 'primary.main' : 'grey.400',
                mb: 3,
                transition: 'all 0.3s ease',
                transform: isDragActive ? 'scale(1.1)' : 'scale(1)',
              }}
            />
            
            <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, mb: 2 }}>
              {isDragActive
                ? 'Drop the file here...'
                : 'Drag & drop a file here, or click to select'}
            </Typography>
            
            <Typography variant="body1" color="text.secondary" paragraph sx={{ mb: 2 }}>
              Supports PDF and image files (PNG, JPG, JPEG, GIF, BMP, TIFF)
            </Typography>
            
            <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2, flexWrap: 'wrap' }}>
              <Chip label="PDF" color="primary" variant="outlined" />
              <Chip label="PNG" color="primary" variant="outlined" />
              <Chip label="JPG" color="primary" variant="outlined" />
              <Chip label="Max 10MB" color="secondary" variant="outlined" />
            </Box>
          </Box>
        </DropzonePaper>
      </Zoom>

      {fileRejections.length > 0 && (
        <Alert severity="error" sx={{ mt: 2 }}>
          <Typography variant="subtitle2" gutterBottom>
            File rejected:
          </Typography>
          {fileRejections.map(({ file, errors }) => (
            <Box key={file.name}>
              <Typography variant="body2">
                <strong>{file.name}</strong> ({formatFileSize(file.size)})
              </Typography>
              {errors.map((error) => (
                <Typography key={error.code} variant="caption" display="block">
                  • {error.message}
                </Typography>
              ))}
            </Box>
          ))}
        </Alert>
      )}

      {loading && (
        <Box sx={{ mt: 2 }}>
          <Typography variant="body2" gutterBottom>
            Analyzing document...
          </Typography>
          <LinearProgress />
        </Box>
      )}

      <Box sx={{ mt: 6 }}>
        <Typography variant="h5" gutterBottom align="center" sx={{ fontWeight: 600, mb: 4 }}>
          What You'll Get
        </Typography>
        
        <Grid container spacing={3}>
          <Grid item xs={12} sm={6} md={4}>
            <FeatureCard>
              <CardContent sx={{ textAlign: 'center', p: 3 }}>
                <Speed sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
                <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                  OCR Text Extraction
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Extract text from PDFs and images using advanced OCR technology with high accuracy
                </Typography>
              </CardContent>
            </FeatureCard>
          </Grid>
          
          <Grid item xs={12} sm={6} md={4}>
            <FeatureCard>
              <CardContent sx={{ textAlign: 'center', p: 3 }}>
                <Psychology sx={{ fontSize: 48, color: 'secondary.main', mb: 2 }} />
                <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                  AI Summaries
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Get three levels of summaries: ELI5, Plain Language, and Detailed explanations
                </Typography>
              </CardContent>
            </FeatureCard>
          </Grid>
          
          <Grid item xs={12} sm={6} md={4}>
            <FeatureCard>
              <CardContent sx={{ textAlign: 'center', p: 3 }}>
                <Assessment sx={{ fontSize: 48, color: 'error.main', mb: 2 }} />
                <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                  Risk Assessment
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Identify high-risk clauses with color-coded risk levels and detailed explanations
                </Typography>
              </CardContent>
            </FeatureCard>
          </Grid>
          
          <Grid item xs={12} sm={6} md={4}>
            <FeatureCard>
              <CardContent sx={{ textAlign: 'center', p: 3 }}>
                <AutoAwesome sx={{ fontSize: 48, color: 'success.main', mb: 2 }} />
                <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                  Language Detection
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Automatically detect the document language with confidence scores
                </Typography>
              </CardContent>
            </FeatureCard>
          </Grid>
          
          <Grid item xs={12} sm={6} md={4}>
            <FeatureCard>
              <CardContent sx={{ textAlign: 'center', p: 3 }}>
                <Security sx={{ fontSize: 48, color: 'warning.main', mb: 2 }} />
                <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                  Clause Segmentation
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Break down the document into individual clauses for detailed analysis
                </Typography>
              </CardContent>
            </FeatureCard>
          </Grid>
          
          <Grid item xs={12} sm={6} md={4}>
            <FeatureCard>
              <CardContent sx={{ textAlign: 'center', p: 3 }}>
                <CheckCircle sx={{ fontSize: 48, color: 'info.main', mb: 2 }} />
                <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                  AI Chatbot
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Ask questions about the document and get instant, accurate answers
                </Typography>
              </CardContent>
            </FeatureCard>
          </Grid>
        </Grid>
      </Box>

      <Box sx={{ mt: 3, display: 'flex', gap: 1, flexWrap: 'wrap' }}>
        <Chip label="PDF Support" color="primary" size="small" />
        <Chip label="Image OCR" color="primary" size="small" />
        <Chip label="Multi-language" color="primary" size="small" />
        <Chip label="Risk Analysis" color="secondary" size="small" />
        <Chip label="AI Summaries" color="secondary" size="small" />
        <Chip label="Chatbot Q&A" color="secondary" size="small" />
      </Box>
    </Box>
  );
}

export default DocumentUpload;
