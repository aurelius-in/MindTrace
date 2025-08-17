import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Slider,
  Button,
  TextField,
  Chip,
  Avatar,
  LinearProgress,
  Alert,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Paper,
  Rating,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  FormHelperText,
} from '@mui/material';
import {
  Mood,
  Psychology,
  FitnessCenter,
  LocalHospital,
  CheckCircle,
  TrendingUp,
  TrendingDown,
  Favorite,
  EmojiEmotions,
  SentimentVeryDissatisfied,
  SentimentDissatisfied,
  SentimentNeutral,
  SentimentSatisfied,
  SentimentVerySatisfied,
  Lightbulb,
  Schedule,
  Star,
} from '@mui/icons-material';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';

import { RootState } from '../../store';
import { 
  createWellnessEntry, 
  trackMood, 
  getRecommendations,
  clearRecommendations 
} from '../../store/slices/wellnessSlice';
import { addNotification } from '../../store/slices/uiSlice';
import LoadingSpinner from '../../components/Common/LoadingSpinner';

interface WellnessMetrics {
  mood: number;
  stress: number;
  energy: number;
  sleepQuality: number;
  workLifeBalance: number;
}

interface WellnessInsights {
  overallScore: number;
  trend: 'improving' | 'declining' | 'stable';
  recommendations: string[];
  riskLevel: 'low' | 'medium' | 'high';
}

const WellnessCheckIn: React.FC = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { user } = useSelector((state: RootState) => state.auth);
  const { isLoading, recommendations, entries } = useSelector((state: RootState) => state.wellness);
  
  const [metrics, setMetrics] = useState<WellnessMetrics>({
    mood: 5,
    stress: 5,
    energy: 5,
    sleepQuality: 5,
    workLifeBalance: 5,
  });
  
  const [description, setDescription] = useState('');
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [insights, setInsights] = useState<WellnessInsights | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showInsights, setShowInsights] = useState(false);

  const availableTags = [
    'work-pressure', 'personal-life', 'health', 'relationships', 
    'financial', 'career-growth', 'team-dynamics', 'workload',
    'burnout-risk', 'positive-moment', 'achievement', 'gratitude'
  ];

  const moodIcons = [
    <SentimentVeryDissatisfied key="1" color="error" />,
    <SentimentDissatisfied key="2" color="warning" />,
    <SentimentNeutral key="3" color="action" />,
    <SentimentSatisfied key="4" color="success" />,
    <SentimentVerySatisfied key="5" color="primary" />,
  ];

  const getMoodLabel = (value: number) => {
    const labels = ['Very Poor', 'Poor', 'Okay', 'Good', 'Excellent'];
    return labels[value - 1] || 'Okay';
  };

  const getStressLabel = (value: number) => {
    if (value <= 2) return 'Very Low';
    if (value <= 4) return 'Low';
    if (value <= 6) return 'Moderate';
    if (value <= 8) return 'High';
    return 'Very High';
  };

  const getEnergyLabel = (value: number) => {
    if (value <= 2) return 'Very Low';
    if (value <= 4) return 'Low';
    if (value <= 6) return 'Moderate';
    if (value <= 8) return 'High';
    return 'Very High';
  };

  const getSleepQualityLabel = (value: number) => {
    if (value <= 2) return 'Poor';
    if (value <= 4) return 'Fair';
    if (value <= 6) return 'Good';
    if (value <= 8) return 'Very Good';
    return 'Excellent';
  };

  const getWorkLifeBalanceLabel = (value: number) => {
    if (value <= 2) return 'Poor';
    if (value <= 4) return 'Fair';
    if (value <= 6) return 'Good';
    if (value <= 8) return 'Very Good';
    return 'Excellent';
  };

  const calculateOverallScore = (): number => {
    const weights = { mood: 0.3, stress: 0.25, energy: 0.2, sleepQuality: 0.15, workLifeBalance: 0.1 };
    const weightedSum = Object.entries(metrics).reduce((sum, [key, value]) => {
      return sum + (value * weights[key as keyof WellnessMetrics]);
    }, 0);
    return Math.round(weightedSum);
  };

  const analyzeTrend = (): 'improving' | 'declining' | 'stable' => {
    if (entries.length < 2) return 'stable';
    
    const recentEntries = entries.slice(0, 3);
    const olderEntries = entries.slice(3, 6);
    
    if (olderEntries.length === 0) return 'stable';
    
    const recentAvg = recentEntries.reduce((sum, entry) => sum + entry.value, 0) / recentEntries.length;
    const olderAvg = olderEntries.reduce((sum, entry) => sum + entry.value, 0) / olderEntries.length;
    
    const difference = recentAvg - olderAvg;
    if (difference > 1) return 'improving';
    if (difference < -1) return 'declining';
    return 'stable';
  };

  const assessRiskLevel = (): 'low' | 'medium' | 'high' => {
    const overallScore = calculateOverallScore();
    if (overallScore >= 7) return 'low';
    if (overallScore >= 4) return 'medium';
    return 'high';
  };

  const generateRecommendations = (): string[] => {
    const recs: string[] = [];
    const riskLevel = assessRiskLevel();
    
    if (metrics.stress > 7) {
      recs.push('Consider taking short breaks throughout the day');
      recs.push('Try deep breathing exercises or meditation');
    }
    
    if (metrics.energy < 4) {
      recs.push('Ensure you\'re getting adequate sleep');
      recs.push('Consider light physical activity to boost energy');
    }
    
    if (metrics.sleepQuality < 4) {
      recs.push('Establish a consistent bedtime routine');
      recs.push('Limit screen time before bed');
    }
    
    if (metrics.workLifeBalance < 4) {
      recs.push('Set clear boundaries between work and personal time');
      recs.push('Schedule regular breaks and time off');
    }
    
    if (riskLevel === 'high') {
      recs.push('Consider speaking with a mental health professional');
      recs.push('Reach out to your manager or HR for support');
    }
    
    return recs.length > 0 ? recs : ['Keep up the great work! Your wellness routine is working well.'];
  };

  const handleMetricChange = (metric: keyof WellnessMetrics, value: number) => {
    setMetrics(prev => ({ ...prev, [metric]: value }));
  };

  const handleTagToggle = (tag: string) => {
    setSelectedTags(prev => 
      prev.includes(tag) 
        ? prev.filter(t => t !== tag)
        : [...prev, tag]
    );
  };

  const handleSubmit = async () => {
    setIsSubmitting(true);
    try {
      // Create wellness entries for each metric
      const entryPromises = Object.entries(metrics).map(([key, value]) =>
        dispatch(createWellnessEntry({
          entryType: key as any,
          value,
          description: key === 'mood' ? description : undefined,
          tags: key === 'mood' ? selectedTags : undefined,
          metadata: {
            checkInType: 'comprehensive',
            timestamp: new Date().toISOString(),
          }
        }))
      );

      await Promise.all(entryPromises);

      // Generate insights
      const overallScore = calculateOverallScore();
      const trend = analyzeTrend();
      const riskLevel = assessRiskLevel();
      const recommendations = generateRecommendations();

      setInsights({
        overallScore,
        trend,
        recommendations,
        riskLevel,
      });

      setShowInsights(true);

      // Get AI recommendations
      const needs = `Wellness score: ${overallScore}/10, Stress: ${metrics.stress}/10, Energy: ${metrics.energy}/10, Risk level: ${riskLevel}`;
      await dispatch(getRecommendations(needs));

      dispatch(addNotification({
        type: 'success',
        title: 'Check-in Complete',
        message: 'Your wellness check-in has been recorded successfully!',
      }));

    } catch (error) {
      dispatch(addNotification({
        type: 'error',
        title: 'Check-in Failed',
        message: 'Failed to record your wellness check-in. Please try again.',
      }));
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleQuickCheckIn = async () => {
    setIsSubmitting(true);
    try {
      await dispatch(trackMood({ value: metrics.mood, description }));
      
      dispatch(addNotification({
        type: 'success',
        title: 'Quick Check-in Complete',
        message: 'Your mood has been recorded successfully!',
      }));

      navigate('/dashboard');
    } catch (error) {
      dispatch(addNotification({
        type: 'error',
        title: 'Check-in Failed',
        message: 'Failed to record your mood. Please try again.',
      }));
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return <LoadingSpinner message="Loading wellness data..." />;
  }

  return (
    <Box sx={{ p: 3, maxWidth: 1200, mx: 'auto' }}>
      <Typography variant="h4" sx={{ mb: 3, fontWeight: 600, color: 'primary.main' }}>
        Wellness Check-in
      </Typography>
      
      <Typography variant="body1" sx={{ mb: 4, color: 'text.secondary' }}>
        Take a moment to reflect on your current wellness state. This helps us provide personalized support and track your well-being over time.
      </Typography>

      <Grid container spacing={3}>
        {/* Main Check-in Form */}
        <Grid item xs={12} lg={8}>
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                How are you feeling today?
              </Typography>

              {/* Mood Assessment */}
              <Box sx={{ mb: 4 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Mood sx={{ mr: 1, color: 'primary.main' }} />
                  <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                    Overall Mood
                  </Typography>
                </Box>
                
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Rating
                    value={metrics.mood}
                    onChange={(_, value) => value && handleMetricChange('mood', value)}
                    max={5}
                    size="large"
                  />
                  <Typography variant="body2" sx={{ ml: 2, fontWeight: 500 }}>
                    {getMoodLabel(metrics.mood)}
                  </Typography>
                </Box>

                <TextField
                  fullWidth
                  multiline
                  rows={3}
                  placeholder="How are you feeling today? (optional)"
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  sx={{ mb: 2 }}
                />

                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" sx={{ mb: 1, fontWeight: 500 }}>
                    Tags (select all that apply):
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                    {availableTags.map((tag) => (
                      <Chip
                        key={tag}
                        label={tag.replace('-', ' ')}
                        onClick={() => handleTagToggle(tag)}
                        color={selectedTags.includes(tag) ? 'primary' : 'default'}
                        variant={selectedTags.includes(tag) ? 'filled' : 'outlined'}
                        size="small"
                      />
                    ))}
                  </Box>
                </Box>
              </Box>

              <Divider sx={{ my: 3 }} />

              {/* Detailed Metrics */}
              <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                Detailed Wellness Assessment
              </Typography>

              {/* Stress Level */}
              <Box sx={{ mb: 3 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body1" sx={{ fontWeight: 500 }}>
                    Stress Level
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {getStressLabel(metrics.stress)}
                  </Typography>
                </Box>
                <Slider
                  value={metrics.stress}
                  onChange={(_, value) => handleMetricChange('stress', value as number)}
                  min={1}
                  max={10}
                  marks
                  valueLabelDisplay="auto"
                  color={metrics.stress > 7 ? 'error' : metrics.stress > 5 ? 'warning' : 'primary'}
                />
              </Box>

              {/* Energy Level */}
              <Box sx={{ mb: 3 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body1" sx={{ fontWeight: 500 }}>
                    Energy Level
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {getEnergyLabel(metrics.energy)}
                  </Typography>
                </Box>
                <Slider
                  value={metrics.energy}
                  onChange={(_, value) => handleMetricChange('energy', value as number)}
                  min={1}
                  max={10}
                  marks
                  valueLabelDisplay="auto"
                  color={metrics.energy < 4 ? 'error' : metrics.energy < 6 ? 'warning' : 'primary'}
                />
              </Box>

              {/* Sleep Quality */}
              <Box sx={{ mb: 3 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body1" sx={{ fontWeight: 500 }}>
                    Sleep Quality (Last Night)
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {getSleepQualityLabel(metrics.sleepQuality)}
                  </Typography>
                </Box>
                <Slider
                  value={metrics.sleepQuality}
                  onChange={(_, value) => handleMetricChange('sleepQuality', value as number)}
                  min={1}
                  max={10}
                  marks
                  valueLabelDisplay="auto"
                  color={metrics.sleepQuality < 4 ? 'error' : metrics.sleepQuality < 6 ? 'warning' : 'primary'}
                />
              </Box>

              {/* Work-Life Balance */}
              <Box sx={{ mb: 3 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body1" sx={{ fontWeight: 500 }}>
                    Work-Life Balance
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {getWorkLifeBalanceLabel(metrics.workLifeBalance)}
                  </Typography>
                </Box>
                <Slider
                  value={metrics.workLifeBalance}
                  onChange={(_, value) => handleMetricChange('workLifeBalance', value as number)}
                  min={1}
                  max={10}
                  marks
                  valueLabelDisplay="auto"
                  color={metrics.workLifeBalance < 4 ? 'error' : metrics.workLifeBalance < 6 ? 'warning' : 'primary'}
                />
              </Box>

              {/* Action Buttons */}
              <Box sx={{ display: 'flex', gap: 2, mt: 4 }}>
                <Button
                  variant="contained"
                  size="large"
                  onClick={handleSubmit}
                  disabled={isSubmitting}
                  startIcon={<CheckCircle />}
                  sx={{ flex: 1 }}
                >
                  {isSubmitting ? 'Submitting...' : 'Complete Check-in'}
                </Button>
                
                <Button
                  variant="outlined"
                  size="large"
                  onClick={handleQuickCheckIn}
                  disabled={isSubmitting}
                  startIcon={<Schedule />}
                >
                  Quick Mood Only
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Insights and Recommendations */}
        <Grid item xs={12} lg={4}>
          {/* Wellness Score */}
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                Your Wellness Score
              </Typography>
              
              <Box sx={{ textAlign: 'center', mb: 2 }}>
                <Typography variant="h3" sx={{ fontWeight: 700, color: 'primary.main' }}>
                  {calculateOverallScore()}/10
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Overall Wellness
                </Typography>
              </Box>

              <LinearProgress
                variant="determinate"
                value={calculateOverallScore() * 10}
                sx={{ 
                  height: 8, 
                  borderRadius: 4,
                  backgroundColor: 'grey.200',
                  '& .MuiLinearProgress-bar': {
                    backgroundColor: calculateOverallScore() >= 7 ? 'success.main' : 
                                   calculateOverallScore() >= 4 ? 'warning.main' : 'error.main',
                  }
                }}
              />

              <Box sx={{ mt: 2, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                {insights?.trend === 'improving' && <TrendingUp color="success" />}
                {insights?.trend === 'declining' && <TrendingDown color="error" />}
                <Typography variant="body2" sx={{ ml: 1 }}>
                  {insights?.trend === 'improving' ? 'Improving' : 
                   insights?.trend === 'declining' ? 'Needs attention' : 'Stable'}
                </Typography>
              </Box>
            </CardContent>
          </Card>

          {/* Quick Tips */}
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                Quick Wellness Tips
              </Typography>
              
              <List dense>
                <ListItem>
                  <ListItemIcon>
                    <Lightbulb color="primary" />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Take regular breaks"
                    secondary="5-minute breaks every hour can improve focus"
                  />
                </ListItem>
                
                <ListItem>
                  <ListItemIcon>
                    <Favorite color="error" />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Practice gratitude"
                    secondary="Write down 3 things you're grateful for"
                  />
                </ListItem>
                
                <ListItem>
                  <ListItemIcon>
                    <FitnessCenter color="success" />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Move your body"
                    secondary="Even a short walk can boost your mood"
                  />
                </ListItem>
              </List>
            </CardContent>
          </Card>

          {/* Risk Assessment */}
          {insights && (
            <Card sx={{ mb: 3 }}>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                  Risk Assessment
                </Typography>
                
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Chip
                    label={insights.riskLevel.toUpperCase()}
                    color={insights.riskLevel === 'high' ? 'error' : 
                           insights.riskLevel === 'medium' ? 'warning' : 'success'}
                    sx={{ fontWeight: 600 }}
                  />
                </Box>

                {insights.riskLevel === 'high' && (
                  <Alert severity="warning" sx={{ mb: 2 }}>
                    Consider reaching out for support. You're not alone.
                  </Alert>
                )}

                <Typography variant="body2" color="text.secondary">
                  Based on your current wellness metrics
                </Typography>
              </CardContent>
            </Card>
          )}

          {/* AI Recommendations */}
          {recommendations.length > 0 && (
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                  Personalized Recommendations
                </Typography>
                
                <List dense>
                  {recommendations.slice(0, 3).map((rec, index) => (
                    <ListItem key={index}>
                      <ListItemIcon>
                        <Star color="primary" />
                      </ListItemIcon>
                      <ListItemText 
                        primary={rec}
                        primaryTypographyProps={{ variant: 'body2' }}
                      />
                    </ListItem>
                  ))}
                </List>

                <Button
                  variant="text"
                  size="small"
                  onClick={() => navigate('/resources')}
                  sx={{ mt: 1 }}
                >
                  View More Resources
                </Button>
              </CardContent>
            </Card>
          )}
        </Grid>
      </Grid>

      {/* Insights Modal */}
      {showInsights && insights && (
        <Card sx={{ mt: 3 }}>
          <CardContent>
            <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
              Wellness Insights
            </Typography>
            
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1 }}>
                  Recommendations:
                </Typography>
                <List dense>
                  {insights.recommendations.map((rec, index) => (
                    <ListItem key={index}>
                      <ListItemIcon>
                        <CheckCircle color="primary" />
                      </ListItemIcon>
                      <ListItemText primary={rec} />
                    </ListItem>
                  ))}
                </List>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1 }}>
                  Next Steps:
                </Typography>
                <List dense>
                  <ListItem>
                    <ListItemIcon>
                      <Schedule color="primary" />
                    </ListItemIcon>
                    <ListItemText primary="Schedule your next check-in" />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <Psychology color="primary" />
                    </ListItemIcon>
                    <ListItemText primary="Try the wellness chat for support" />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <LocalHospital color="primary" />
                    </ListItemIcon>
                    <ListItemText primary="Explore wellness resources" />
                  </ListItem>
                </List>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      )}
    </Box>
  );
};

export default WellnessCheckIn;
