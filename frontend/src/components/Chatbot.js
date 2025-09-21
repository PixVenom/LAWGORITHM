import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  TextField,
  Button,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Avatar,
  Chip,
  Alert,
  CircularProgress,
  LinearProgress,
  Divider,
  IconButton,
  Tooltip,
  Fade,
  Zoom,
  Card,
  CardContent,
  Grid,
} from '@mui/material';
import {
  Send,
  SmartToy,
  Person,
  ContentCopy,
  Refresh,
  Lightbulb,
  AutoAwesome,
  Psychology,
  School,
  TrendingUp,
  Security,
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

const ChatContainer = styled(Paper)(({ theme }) => ({
  height: '600px',
  display: 'flex',
  flexDirection: 'column',
  overflow: 'hidden',
  borderRadius: theme.spacing(2),
  background: `linear-gradient(135deg, ${theme.palette.background.paper} 0%, ${alpha(theme.palette.primary.main, 0.02)} 100%)`,
  border: `1px solid ${alpha(theme.palette.primary.main, 0.1)}`,
  boxShadow: `0 8px 32px ${alpha(theme.palette.primary.main, 0.1)}`,
}));

const MessagesContainer = styled(Box)(({ theme }) => ({
  flex: 1,
  overflow: 'auto',
  padding: theme.spacing(2),
  background: `linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.02)} 0%, transparent 100%)`,
}));

const MessageBubble = styled(Paper)(({ theme, isUser }) => ({
  padding: theme.spacing(2),
  marginBottom: theme.spacing(2),
  maxWidth: '85%',
  borderRadius: theme.spacing(2),
  background: isUser 
    ? `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.primary.dark} 100%)`
    : `linear-gradient(135deg, ${theme.palette.background.paper} 0%, ${alpha(theme.palette.grey[100], 0.5)} 100%)`,
  color: isUser ? theme.palette.primary.contrastText : theme.palette.text.primary,
  marginLeft: isUser ? 'auto' : 0,
  marginRight: isUser ? 0 : 'auto',
  boxShadow: `0 4px 20px ${alpha(isUser ? theme.palette.primary.main : theme.palette.grey[500], 0.2)}`,
  transition: 'all 0.3s ease',
  '&:hover': {
    transform: 'translateY(-2px)',
    boxShadow: `0 8px 32px ${alpha(isUser ? theme.palette.primary.main : theme.palette.grey[500], 0.3)}`,
  },
}));

const InputContainer = styled(Box)(({ theme }) => ({
  padding: theme.spacing(3),
  borderTop: `1px solid ${alpha(theme.palette.divider, 0.5)}`,
  display: 'flex',
  gap: theme.spacing(2),
  background: `linear-gradient(135deg, ${theme.palette.background.paper} 0%, ${alpha(theme.palette.primary.main, 0.02)} 100%)`,
}));

const SuggestionCard = styled(Card)(({ theme }) => ({
  borderRadius: theme.spacing(2),
  background: `linear-gradient(135deg, ${theme.palette.background.paper} 0%, ${alpha(theme.palette.secondary.main, 0.05)} 100%)`,
  border: `1px solid ${alpha(theme.palette.secondary.main, 0.1)}`,
  transition: 'all 0.3s ease',
  cursor: 'pointer',
  '&:hover': {
    transform: 'translateY(-2px)',
    boxShadow: `0 8px 32px ${alpha(theme.palette.secondary.main, 0.15)}`,
  },
}));

function Chatbot({ documentContext, summaries }) {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Add welcome message
    if (messages.length === 0) {
      setMessages([
        {
          id: 1,
          text: "Hello! I'm your AI legal assistant. I can help you understand this document, explain legal terms, identify risks, and answer questions about the content. What would you like to know?",
          isUser: false,
          timestamp: new Date(),
        },
      ]);
    }
  }, []);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || loading) return;

    const userMessage = {
      id: Date.now(),
      text: inputValue,
      isUser: true,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputValue,
          document_context: documentContext,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      const botMessage = {
        id: Date.now() + 1,
        text: data.response,
        isUser: false,
        timestamp: new Date(),
        confidence: data.confidence,
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (err) {
      setError(`Error: ${err.message}`);
      const errorMessage = {
        id: Date.now() + 1,
        text: "I'm sorry, I'm having trouble processing your request right now. Please try again later.",
        isUser: false,
        timestamp: new Date(),
        isError: true,
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSendMessage();
    }
  };

  const handleCopyMessage = (text) => {
    navigator.clipboard.writeText(text);
  };

  const handleSuggestedQuestion = (question) => {
    setInputValue(question);
  };

  const suggestedQuestions = [
    "What are the main risks in this document?",
    "Can you explain the liability clauses?",
    "What happens if I breach this agreement?",
    "Are there any automatic termination clauses?",
    "What are my payment obligations?",
    "What confidential information is protected?",
    "Can you explain the key terms in simple language?",
    "What should I be most concerned about?",
  ];

  return (
    <Box>
      <Box sx={{ textAlign: 'center', mb: 4 }}>
        <Typography variant="h4" gutterBottom sx={{ fontWeight: 600, color: 'primary.main' }}>
          AI Legal Assistant
        </Typography>
        <Typography variant="h6" color="text.secondary">
          Ask questions about the document, get explanations of legal terms, and understand potential risks
        </Typography>
      </Box>

      {/* Suggested Questions */}
      <Fade in timeout={600}>
        <SuggestionCard sx={{ mb: 3 }}>
          <CardContent sx={{ p: 3 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3 }}>
              <Avatar sx={{ bgcolor: 'primary.main', width: 48, height: 48 }}>
                <Lightbulb />
              </Avatar>
              <Box>
                <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                  Suggested Questions
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Click on any question to get started
                </Typography>
              </Box>
            </Box>
            
            <Grid container spacing={2}>
              {suggestedQuestions.slice(0, 4).map((question, index) => (
                <Grid item xs={12} sm={6} key={index}>
                  <Zoom in timeout={800 + index * 200}>
                    <Chip
                      label={question}
                      onClick={() => handleSuggestedQuestion(question)}
                      variant="outlined"
                      sx={{ 
                        cursor: 'pointer',
                        width: '100%',
                        height: 'auto',
                        padding: 2,
                        '&:hover': {
                          backgroundColor: 'primary.main',
                          color: 'white',
                        },
                      }}
                    />
                  </Zoom>
                </Grid>
              ))}
            </Grid>
          </CardContent>
        </SuggestionCard>
      </Fade>

      {/* Chat Interface */}
      <ChatContainer elevation={3}>
        <MessagesContainer>
          {messages.map((message, index) => (
            <Fade in timeout={300} key={message.id}>
              <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 2, mb: 3 }}>
                <Avatar sx={{ 
                  bgcolor: message.isUser ? 'primary.main' : 'secondary.main',
                  width: 40,
                  height: 40,
                  boxShadow: `0 4px 12px ${alpha(message.isUser ? '#1976d2' : '#dc004e', 0.3)}`,
                }}>
                  {message.isUser ? <Person /> : <SmartToy />}
                </Avatar>
                <Box sx={{ flex: 1 }}>
                  <MessageBubble isUser={message.isUser} elevation={0}>
                    <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap', lineHeight: 1.6 }}>
                      {message.text}
                    </Typography>
                    {message.confidence && (
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 2 }}>
                        <Typography variant="caption" color="text.secondary">
                          Confidence: {(message.confidence * 100).toFixed(0)}%
                        </Typography>
                        <Box sx={{ flex: 1 }}>
                          <LinearProgress
                            variant="determinate"
                            value={message.confidence * 100}
                            color={message.confidence > 0.8 ? 'success' : message.confidence > 0.6 ? 'warning' : 'error'}
                            sx={{ height: 4, borderRadius: 2 }}
                          />
                        </Box>
                      </Box>
                    )}
                  </MessageBubble>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 1, ml: 1 }}>
                    <Typography variant="caption" color="text.secondary">
                      {message.timestamp.toLocaleTimeString()}
                    </Typography>
                    {!message.isUser && (
                      <Tooltip title="Copy message">
                        <IconButton
                          size="small"
                          onClick={() => handleCopyMessage(message.text)}
                          sx={{ 
                            color: 'text.secondary',
                            '&:hover': { color: 'primary.main' }
                          }}
                        >
                          <ContentCopy fontSize="small" />
                        </IconButton>
                      </Tooltip>
                    )}
                  </Box>
                </Box>
              </Box>
            </Fade>
          ))}
          
          {loading && (
            <Fade in timeout={300}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3 }}>
                <Avatar sx={{ 
                  bgcolor: 'secondary.main', 
                  width: 40, 
                  height: 40,
                  animation: `${pulse} 2s infinite`,
                }}>
                  <SmartToy />
                </Avatar>
                <MessageBubble isUser={false} elevation={0}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                    <CircularProgress size={20} color="secondary" />
                    <Typography variant="body1">
                      AI is thinking...
                    </Typography>
                  </Box>
                </MessageBubble>
              </Box>
            </Fade>
          )}
          
          <div ref={messagesEndRef} />
        </MessagesContainer>

        {error && (
          <Alert severity="error" sx={{ m: 1 }}>
            {error}
          </Alert>
        )}

        <InputContainer>
          <TextField
            fullWidth
            multiline
            maxRows={3}
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask a question about the document..."
            disabled={loading}
            variant="outlined"
            size="medium"
            sx={{
              '& .MuiOutlinedInput-root': {
                borderRadius: 3,
                backgroundColor: 'background.paper',
                '&:hover': {
                  '& .MuiOutlinedInput-notchedOutline': {
                    borderColor: 'primary.main',
                  },
                },
                '&.Mui-focused': {
                  '& .MuiOutlinedInput-notchedOutline': {
                    borderWidth: 2,
                  },
                },
              },
            }}
          />
          <Button
            variant="contained"
            onClick={handleSendMessage}
            disabled={!inputValue.trim() || loading}
            startIcon={loading ? <CircularProgress size={20} color="inherit" /> : <Send />}
            sx={{
              borderRadius: 3,
              px: 3,
              py: 1.5,
              minWidth: 120,
              background: 'linear-gradient(135deg, #1976d2 0%, #1565c0 100%)',
              boxShadow: '0 4px 20px rgba(25, 118, 210, 0.3)',
              '&:hover': {
                background: 'linear-gradient(135deg, #1565c0 0%, #0d47a1 100%)',
                boxShadow: '0 8px 32px rgba(25, 118, 210, 0.4)',
                transform: 'translateY(-2px)',
              },
              '&:disabled': {
                background: 'grey.300',
                boxShadow: 'none',
                transform: 'none',
              },
            }}
          >
            {loading ? 'Sending...' : 'Send'}
          </Button>
        </InputContainer>
      </ChatContainer>

      {/* Document Context Info */}
      <Fade in timeout={1200}>
        <SuggestionCard sx={{ mt: 3 }}>
          <CardContent sx={{ p: 3 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
              <Avatar sx={{ bgcolor: 'info.main', width: 40, height: 40 }}>
                <AutoAwesome />
              </Avatar>
              <Box>
                <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                  Document Context Available
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  AI has access to the following document information
                </Typography>
              </Box>
            </Box>
            
            <Grid container spacing={2}>
              <Grid item xs={12} sm={4}>
                <Box sx={{ textAlign: 'center', p: 2 }}>
                  <Typography variant="h4" color="primary.main" gutterBottom sx={{ fontWeight: 700 }}>
                    {(documentContext?.length || 0).toLocaleString()}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Characters Extracted
                  </Typography>
                </Box>
              </Grid>
              <Grid item xs={12} sm={4}>
                <Box sx={{ textAlign: 'center', p: 2 }}>
                  <Typography variant="h4" color="secondary.main" gutterBottom sx={{ fontWeight: 700 }}>
                    OCR
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Text Recognition
                  </Typography>
                </Box>
              </Grid>
              <Grid item xs={12} sm={4}>
                <Box sx={{ textAlign: 'center', p: 2 }}>
                  <Typography variant="h4" color="success.main" gutterBottom sx={{ fontWeight: 700 }}>
                    AI
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Smart Summaries
                  </Typography>
                </Box>
              </Grid>
            </Grid>
          </CardContent>
        </SuggestionCard>
      </Fade>
    </Box>
  );
}

export default Chatbot;
