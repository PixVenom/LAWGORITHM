import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  Chip,
  LinearProgress,
  Alert,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
  Fade,
  Zoom,
  Avatar,
  Tooltip,
  IconButton,
} from '@mui/material';
import {
  ExpandMore,
  Warning,
  Error,
  CheckCircle,
  Assessment,
  TrendingUp,
  Security,
  Info,
  AutoAwesome,
  Psychology,
} from '@mui/icons-material';
import { PieChart, BarChart } from '@mui/x-charts';
import { styled, alpha, keyframes } from '@mui/material/styles';

const pulse = keyframes`
  0% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(255, 68, 68, 0.4);
  }
  70% {
    transform: scale(1.05);
    box-shadow: 0 0 0 10px rgba(255, 68, 68, 0);
  }
  100% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(255, 68, 68, 0);
  }
`;

const RiskCard = styled(Card)(({ theme, riskLevel }) => ({
  borderRadius: theme.spacing(2),
  border: `2px solid ${
    riskLevel === 'high' ? theme.palette.error.main :
    riskLevel === 'medium' ? theme.palette.warning.main :
    theme.palette.success.main
  }`,
  background: `linear-gradient(135deg, ${
    riskLevel === 'high' ? alpha(theme.palette.error.main, 0.1) :
    riskLevel === 'medium' ? alpha(theme.palette.warning.main, 0.1) :
    alpha(theme.palette.success.main, 0.1)
  } 0%, ${theme.palette.background.paper} 100%)`,
  transition: 'all 0.3s ease',
  '&:hover': {
    transform: 'translateY(-4px)',
    boxShadow: `0 12px 40px ${
      riskLevel === 'high' ? alpha(theme.palette.error.main, 0.2) :
      riskLevel === 'medium' ? alpha(theme.palette.warning.main, 0.2) :
      alpha(theme.palette.success.main, 0.2)
    }`,
  },
  ...(riskLevel === 'high' && {
    animation: `${pulse} 2s infinite`,
  }),
}));

const ChartCard = styled(Card)(({ theme }) => ({
  borderRadius: theme.spacing(2),
  background: `linear-gradient(135deg, ${theme.palette.background.paper} 0%, ${alpha(theme.palette.primary.main, 0.02)} 100%)`,
  border: `1px solid ${alpha(theme.palette.primary.main, 0.1)}`,
  boxShadow: `0 4px 20px ${alpha(theme.palette.primary.main, 0.08)}`,
  transition: 'all 0.3s ease',
  '&:hover': {
    transform: 'translateY(-2px)',
    boxShadow: `0 8px 32px ${alpha(theme.palette.primary.main, 0.12)}`,
  },
}));

const RiskIcon = ({ level }) => {
  switch (level) {
    case 'high':
      return <Error color="error" />;
    case 'medium':
      return <Warning color="warning" />;
    case 'low':
      return <CheckCircle color="success" />;
    default:
      return <Assessment color="primary" />;
  }
};

function RiskChart({ riskScores, clauses }) {
  const [expandedClause, setExpandedClause] = useState(false);

  if (!riskScores || riskScores.length === 0) {
    return (
      <Alert severity="info">
        No risk assessment data available for this document.
      </Alert>
    );
  }

  // Calculate risk statistics
  const totalClauses = riskScores.length;
  const highRisk = riskScores.filter(r => r.risk_level === 'high').length;
  const mediumRisk = riskScores.filter(r => r.risk_level === 'medium').length;
  const lowRisk = riskScores.filter(r => r.risk_level === 'low').length;
  
  const averageRisk = riskScores.reduce((sum, r) => sum + r.risk_score, 0) / totalClauses;
  const maxRisk = Math.max(...riskScores.map(r => r.risk_score));
  const minRisk = Math.min(...riskScores.map(r => r.risk_score));

  // Prepare data for charts
  const pieData = [
    { id: 0, value: highRisk, label: 'High Risk', color: '#ff4444' },
    { id: 1, value: mediumRisk, label: 'Medium Risk', color: '#ffaa00' },
    { id: 2, value: lowRisk, label: 'Low Risk', color: '#44aa44' },
  ];

  const barData = riskScores.map((risk, index) => ({
    clause: `Clause ${risk.clause_id}`,
    score: risk.risk_score,
    level: risk.risk_level,
  }));

  const getRiskColor = (level) => {
    switch (level) {
      case 'high': return '#ff4444';
      case 'medium': return '#ffaa00';
      case 'low': return '#44aa44';
      default: return '#666666';
    }
  };

  const getRiskRecommendation = (averageRisk) => {
    if (averageRisk >= 0.7) {
      return {
        severity: 'error',
        title: 'High Risk Document',
        message: 'This document contains significant risks. Consider consulting with a legal professional before proceeding.',
        icon: <Error />
      };
    } else if (averageRisk >= 0.4) {
      return {
        severity: 'warning',
        title: 'Medium Risk Document',
        message: 'This document has moderate risks. Review the highlighted clauses carefully.',
        icon: <Warning />
      };
    } else {
      return {
        severity: 'success',
        title: 'Low Risk Document',
        message: 'This document appears to have low overall risk, but still review all terms carefully.',
        icon: <CheckCircle />
      };
    }
  };

  const recommendation = getRiskRecommendation(averageRisk);

  return (
    <Box>
      <Box sx={{ textAlign: 'center', mb: 4 }}>
        <Typography variant="h4" gutterBottom sx={{ fontWeight: 600, color: 'primary.main' }}>
          Risk Assessment Dashboard
        </Typography>
        <Typography variant="h6" color="text.secondary">
          AI-powered analysis of document risks and potential concerns
        </Typography>
      </Box>
      
      {/* Risk Overview Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Zoom in timeout={400}>
            <RiskCard riskLevel="high">
              <CardContent sx={{ textAlign: 'center', p: 3 }}>
                <Avatar sx={{ bgcolor: 'error.main', width: 64, height: 64, mx: 'auto', mb: 2 }}>
                  <Error sx={{ fontSize: 32 }} />
                </Avatar>
                <Typography variant="h3" color="error.main" gutterBottom sx={{ fontWeight: 700 }}>
                  {highRisk}
                </Typography>
                <Typography variant="h6" color="error.main" gutterBottom sx={{ fontWeight: 600 }}>
                  High Risk
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {((highRisk / totalClauses) * 100).toFixed(1)}% of clauses
                </Typography>
                <LinearProgress
                  variant="determinate"
                  value={(highRisk / totalClauses) * 100}
                  color="error"
                  sx={{ mt: 2, borderRadius: 1 }}
                />
              </CardContent>
            </RiskCard>
          </Zoom>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Zoom in timeout={600}>
            <RiskCard riskLevel="medium">
              <CardContent sx={{ textAlign: 'center', p: 3 }}>
                <Avatar sx={{ bgcolor: 'warning.main', width: 64, height: 64, mx: 'auto', mb: 2 }}>
                  <Warning sx={{ fontSize: 32 }} />
                </Avatar>
                <Typography variant="h3" color="warning.main" gutterBottom sx={{ fontWeight: 700 }}>
                  {mediumRisk}
                </Typography>
                <Typography variant="h6" color="warning.main" gutterBottom sx={{ fontWeight: 600 }}>
                  Medium Risk
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {((mediumRisk / totalClauses) * 100).toFixed(1)}% of clauses
                </Typography>
                <LinearProgress
                  variant="determinate"
                  value={(mediumRisk / totalClauses) * 100}
                  color="warning"
                  sx={{ mt: 2, borderRadius: 1 }}
                />
              </CardContent>
            </RiskCard>
          </Zoom>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Zoom in timeout={800}>
            <RiskCard riskLevel="low">
              <CardContent sx={{ textAlign: 'center', p: 3 }}>
                <Avatar sx={{ bgcolor: 'success.main', width: 64, height: 64, mx: 'auto', mb: 2 }}>
                  <CheckCircle sx={{ fontSize: 32 }} />
                </Avatar>
                <Typography variant="h3" color="success.main" gutterBottom sx={{ fontWeight: 700 }}>
                  {lowRisk}
                </Typography>
                <Typography variant="h6" color="success.main" gutterBottom sx={{ fontWeight: 600 }}>
                  Low Risk
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {((lowRisk / totalClauses) * 100).toFixed(1)}% of clauses
                </Typography>
                <LinearProgress
                  variant="determinate"
                  value={(lowRisk / totalClauses) * 100}
                  color="success"
                  sx={{ mt: 2, borderRadius: 1 }}
                />
              </CardContent>
            </RiskCard>
          </Zoom>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Zoom in timeout={1000}>
            <RiskCard riskLevel="average">
              <CardContent sx={{ textAlign: 'center', p: 3 }}>
                <Avatar sx={{ bgcolor: 'primary.main', width: 64, height: 64, mx: 'auto', mb: 2 }}>
                  <TrendingUp sx={{ fontSize: 32 }} />
                </Avatar>
                <Typography variant="h3" color="primary.main" gutterBottom sx={{ fontWeight: 700 }}>
                  {(averageRisk * 100).toFixed(1)}%
                </Typography>
                <Typography variant="h6" color="primary.main" gutterBottom sx={{ fontWeight: 600 }}>
                  Average Risk
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Overall document risk
                </Typography>
                <LinearProgress
                  variant="determinate"
                  value={averageRisk * 100}
                  color="primary"
                  sx={{ mt: 2, borderRadius: 1 }}
                />
              </CardContent>
            </RiskCard>
          </Zoom>
        </Grid>
      </Grid>

      {/* Risk Recommendation */}
      <Alert severity={recommendation.severity} sx={{ mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          {recommendation.icon}
          <Box>
            <Typography variant="subtitle1" fontWeight="bold">
              {recommendation.title}
            </Typography>
            <Typography variant="body2">
              {recommendation.message}
            </Typography>
          </Box>
        </Box>
      </Alert>

      {/* Charts */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={6}>
          <Fade in timeout={800}>
            <ChartCard>
              <CardContent sx={{ p: 3 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3 }}>
                  <Avatar sx={{ bgcolor: 'primary.main', width: 48, height: 48 }}>
                    <Assessment />
                  </Avatar>
                  <Box>
                    <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                      Risk Distribution
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Visual breakdown of risk levels
                    </Typography>
                  </Box>
                </Box>
                <PieChart
                  series={[
                    {
                      data: pieData,
                      highlightScope: { faded: 'global', highlighted: 'item' },
                      faded: { innerRadius: 30, additionalRadius: -30, color: 'gray' },
                    },
                  ]}
                  height={300}
                />
              </CardContent>
            </ChartCard>
          </Fade>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Fade in timeout={1000}>
            <ChartCard>
              <CardContent sx={{ p: 3 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3 }}>
                  <Avatar sx={{ bgcolor: 'secondary.main', width: 48, height: 48 }}>
                    <TrendingUp />
                  </Avatar>
                  <Box>
                    <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                      Risk Scores by Clause
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Individual clause risk analysis
                    </Typography>
                  </Box>
                </Box>
                <BarChart
                  dataset={barData}
                  xAxis={[{ scaleType: 'band', dataKey: 'clause' }]}
                  series={[
                    {
                      dataKey: 'score',
                      label: 'Risk Score',
                      color: '#1976d2',
                    },
                  ]}
                  height={300}
                />
              </CardContent>
            </ChartCard>
          </Fade>
        </Grid>
      </Grid>

      {/* Detailed Risk Analysis */}
      <Paper sx={{ p: 2 }}>
        <Typography variant="h6" gutterBottom>
          Detailed Risk Analysis
        </Typography>
        
        {riskScores.map((risk, index) => {
          const clause = clauses?.find(c => c.id === risk.clause_id);
          return (
            <Accordion
              key={risk.clause_id || index}
              expanded={expandedClause === risk.clause_id}
              onChange={() => setExpandedClause(expandedClause === risk.clause_id ? false : risk.clause_id)}
            >
              <AccordionSummary expandIcon={<ExpandMore />}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, width: '100%' }}>
                  <RiskIcon level={risk.risk_level} />
                  <Typography variant="subtitle1">
                    Clause {risk.clause_id}
                  </Typography>
                  <Chip
                    label={risk.risk_level.toUpperCase()}
                    sx={{
                      backgroundColor: getRiskColor(risk.risk_level),
                      color: 'white',
                      fontWeight: 'bold',
                    }}
                  />
                  <Box sx={{ flexGrow: 1 }} />
                  <Typography variant="body2" color="text.secondary">
                    Risk Score: {(risk.risk_score * 100).toFixed(1)}%
                  </Typography>
                </Box>
              </AccordionSummary>
              <AccordionDetails>
                <Grid container spacing={2}>
                  <Grid item xs={12} md={8}>
                    <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap', mb: 2 }}>
                      {clause?.text || 'Clause text not available'}
                    </Typography>
                    <Typography variant="subtitle2" gutterBottom>
                      Risk Explanation:
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {risk.explanation || 'No explanation available'}
                    </Typography>
                  </Grid>
                  <Grid item xs={12} md={4}>
                    <Typography variant="subtitle2" gutterBottom>
                      Risk Factors:
                    </Typography>
                    <List dense>
                      {risk.risk_factors?.map((factor, factorIndex) => (
                        <ListItem key={factorIndex}>
                          <ListItemIcon>
                            <Security fontSize="small" />
                          </ListItemIcon>
                          <ListItemText
                            primary={factor}
                            primaryTypographyProps={{ variant: 'body2' }}
                          />
                        </ListItem>
                      )) || (
                        <ListItem>
                          <ListItemText
                            primary="No specific risk factors identified"
                            primaryTypographyProps={{ variant: 'body2', color: 'text.secondary' }}
                          />
                        </ListItem>
                      )}
                    </List>
                    <Divider sx={{ my: 1 }} />
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Typography variant="body2" color="text.secondary">
                        Risk Level:
                      </Typography>
                      <Chip
                        label={risk.risk_level.toUpperCase()}
                        size="small"
                        sx={{
                          backgroundColor: getRiskColor(risk.risk_level),
                          color: 'white',
                        }}
                      />
                    </Box>
                  </Grid>
                </Grid>
              </AccordionDetails>
            </Accordion>
          );
        })}
      </Paper>
    </Box>
  );
}

export default RiskChart;
