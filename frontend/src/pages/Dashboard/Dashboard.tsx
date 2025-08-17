import React, { useEffect, useState } from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  Button,
  Chip,
  LinearProgress,
  Avatar,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Paper,
  Divider,
} from '@mui/material';
import {
  Favorite,
  TrendingUp,
  TrendingDown,
  CheckCircle,
  Warning,
  Info,
  ArrowForward,
  Mood,
  Psychology,
  FitnessCenter,
  LocalHospital,
  Spa,
  EmojiEmotions,
  SelfImprovement,
} from '@mui/icons-material';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';

import { RootState } from '../../store';
import { fetchWellnessEntries, fetchConversations } from '../../store/slices/wellnessSlice';
import { fetchOrganizationalHealth } from '../../store/slices/analyticsSlice';
import LoadingSpinner from '../../components/Common/LoadingSpinner';

const Dashboard: React.FC = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { user } = useSelector((state: RootState) => state.auth);
  const { entries, conversations, currentMood, lastCheckIn } = useSelector((state: RootState) => state.wellness);
  const { organizationalHealth } = useSelector((state: RootState) => state.analytics);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadDashboardData = async () => {
      try {
        await Promise.all([
          dispatch(fetchWellnessEntries()),
          dispatch(fetchConversations()),
        ]);

        // Load analytics data for managers and above
        if (user?.roles.some(role => ['manager', 'hr', 'admin'].includes(role))) {
          await dispatch(fetchOrganizationalHealth('30d'));
        }
      } catch (error) {
        console.error('Failed to load dashboard data:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadDashboardData();
  }, [dispatch, user]);

  const hasRole = (roles: string[]) => {
    return user?.roles.some(role => roles.includes(role)) || false;
  };

  const getWellnessScore = () => {
    if (entries.length === 0) return 0;
    const recentEntries = entries.slice(0, 7); // Last 7 entries
    const avgScore = recentEntries.reduce((sum, entry) => sum + entry.value, 0) / recentEntries.length;
    return Math.round((avgScore / 10) * 100);
  };

  const getMoodTrend = () => {
    if (entries.length < 2) return 'stable';
    const recent = entries.slice(0, 3).reduce((sum, entry) => sum + entry.value, 0) / 3;
    const previous = entries.slice(3, 6).reduce((sum, entry) => sum + entry.value, 0) / 3;
    return recent > previous ? 'up' : recent < previous ? 'down' : 'stable';
  };

  const getQuickActions = () => {
    const actions = [
      {
        title: 'Mind',
        description: 'Mental wellness and mindfulness',
        icon: <Psychology />,
        path: '/wellness/chat',
        color: '#3498db',
      },
      {
        title: 'Body',
        description: 'Physical wellness and fitness',
        icon: <FitnessCenter />,
        path: '/wellness/check-in',
        color: '#e67e22',
      },
      {
        title: 'Spirit',
        description: 'Emotional and spiritual wellness',
        icon: <Spa />,
        path: '/resources',
        color: '#9b59b6',
      },
      {
        title: 'Joy',
        description: 'Happiness and positive emotions',
        icon: <EmojiEmotions />,
        path: '/wellness/history',
        color: '#f1c40f',
      },
    ];

    return actions;
  };

  const getRecentActivity = () => {
    const activities = [];
    
    // Add recent wellness entries
    entries.slice(0, 3).forEach(entry => {
      activities.push({
        type: 'wellness',
        title: `${entry.entryType.charAt(0).toUpperCase() + entry.entryType.slice(1)} Check-in`,
        description: `Rated ${entry.value}/10`,
        time: new Date(entry.createdAt).toLocaleDateString(),
        icon: <Mood />,
        mood: entry.value,
      });
    });

    // Add recent conversations
    conversations.slice(0, 2).forEach(conversation => {
      activities.push({
        type: 'conversation',
        title: 'AI Wellness Chat',
        description: conversation.message.substring(0, 50) + '...',
        time: new Date(conversation.createdAt).toLocaleDateString(),
        icon: <Psychology />,
        mood: 7, // Default mood for conversations
      });
    });

    return activities.sort((a, b) => new Date(b.time).getTime() - new Date(a.time).getTime());
  };

  const getWellnessJourney = () => {
    return [
      { week: 'Week 1', focus: 'Mindfulness', progress: 85, status: 'completed' },
      { week: 'Week 2', focus: 'Stress Management', progress: 70, status: 'in-progress' },
      { week: 'Week 3', focus: 'Physical Wellness', progress: 45, status: 'upcoming' },
      { week: 'Week 4', focus: 'Social Connection', progress: 0, status: 'upcoming' }
    ];
  };

  if (isLoading) {
    return <LoadingSpinner message="Loading your wellness dashboard..." />;
  }

  return (
    <Box sx={{ p: 3 }}>
      <Grid container spacing={3}>
        {/* Welcome Section */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 4, borderRadius: 4, bgcolor: '#34495e', color: 'white', height: '100%' }}>
            <Typography variant="h4" sx={{ mb: 1, color: 'white' }}>
              Welcome back, {user?.firstName}! 🌟
            </Typography>
            <Typography variant="body1" sx={{ mb: 2, color: '#bdc3c7' }}>
              You're {getWellnessScore()}% through your wellness journey this month
            </Typography>
            <Button
              variant="contained"
              size="large"
              onClick={() => navigate('/wellness/check-in')}
              sx={{ 
                bgcolor: '#e74c3c', 
                '&:hover': { bgcolor: '#c0392b' },
                borderRadius: 3,
                px: 3,
                py: 1
              }}
            >
              Continue My Journey
            </Button>
          </Paper>
        </Grid>

        {/* Wellness Journey Progress */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3, borderRadius: 4, bgcolor: '#34495e', color: 'white' }}>
            <Typography variant="h5" sx={{ mb: 3, color: 'white' }}>
              Your Wellness Journey 📈
            </Typography>
            <Box sx={{ position: 'relative' }}>
              {getWellnessJourney().map((journey, index) => (
                <Box key={index} sx={{ mb: 3, display: 'flex', alignItems: 'center' }}>
                  <Box sx={{ 
                    width: 40, 
                    height: 40, 
                    borderRadius: '50%', 
                    bgcolor: journey.status === 'completed' ? '#27ae60' : 
                             journey.status === 'in-progress' ? '#f39c12' : '#7f8c8d',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white',
                    fontWeight: 'bold',
                    mr: 2
                  }}>
                    {index + 1}
                  </Box>
                  <Box sx={{ flexGrow: 1 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                      <Typography variant="h6" sx={{ color: 'white' }}>
                        {journey.focus}
                      </Typography>
                      <Typography variant="body2" sx={{ color: '#bdc3c7' }}>
                        {journey.week}
                      </Typography>
                    </Box>
                    <Typography variant="body2" sx={{ mb: 1, color: '#bdc3c7' }}>
                      Progress: {journey.progress}%
                    </Typography>
                    <LinearProgress 
                      variant="determinate" 
                      value={journey.progress} 
                      sx={{ height: 8, borderRadius: 4, bgcolor: '#2c3e50' }}
                    />
                  </Box>
                </Box>
              ))}
            </Box>
          </Paper>
        </Grid>

        {/* Quick Wellness Actions */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, borderRadius: 4, height: '100%', bgcolor: '#34495e', color: 'white' }}>
            <Typography variant="h5" sx={{ mb: 3, color: 'white' }}>
              Quick Actions ⚡
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              {getQuickActions().map((action, index) => (
                <Button
                  key={index}
                  variant="outlined"
                  fullWidth
                  startIcon={action.icon}
                  onClick={() => navigate(action.path)}
                  sx={{ 
                    borderColor: action.color, 
                    color: action.color,
                    '&:hover': { borderColor: action.color, bgcolor: '#2c3e50' },
                    borderRadius: 3,
                    py: 2,
                    fontSize: '1.1rem',
                    fontWeight: 'bold'
                  }}
                >
                  {action.title}
                </Button>
              ))}
            </Box>
          </Paper>
        </Grid>

        {/* Recent Activity with Icons */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3, borderRadius: 4, bgcolor: '#34495e', color: 'white' }}>
            <Typography variant="h5" sx={{ mb: 3, color: 'white' }}>
              Recent Wellness Moments ✨
            </Typography>
            <Grid container spacing={2}>
              {getRecentActivity().map((activity, index) => (
                <Grid item xs={12} md={4} key={index}>
                  <Card sx={{ 
                    borderRadius: 3, 
                    bgcolor: activity.mood >= 7 ? '#27ae60' : 
                             activity.mood >= 5 ? '#f39c12' : '#e74c3c',
                    border: `2px solid ${activity.mood >= 7 ? '#2ecc71' : 
                                        activity.mood >= 5 ? '#f1c40f' : '#c0392b'}`
                  }}>
                    <CardContent sx={{ textAlign: 'center' }}>
                      <Avatar sx={{ 
                        width: 50, 
                        height: 50, 
                        mx: 'auto', 
                        mb: 2,
                        bgcolor: 'rgba(255,255,255,0.2)',
                        color: 'white'
                      }}>
                        {activity.mood}
                      </Avatar>
                      <Typography variant="h6" sx={{ mb: 1, color: 'white' }}>
                        {activity.title}
                      </Typography>
                      <Typography variant="body2" sx={{ mb: 2, color: 'rgba(255,255,255,0.8)' }}>
                        {activity.description}
                      </Typography>
                      <Chip 
                        label={`Mood: ${activity.mood}/10`} 
                        size="small" 
                        sx={{ 
                          bgcolor: 'rgba(255,255,255,0.2)',
                          color: 'white'
                        }}
                      />
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </Paper>
        </Grid>

        {/* Wellness Tips */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3, borderRadius: 4, bgcolor: '#34495e', color: 'white' }}>
            <Typography variant="h5" sx={{ mb: 3, color: 'white' }}>
              Wellness Tips 💡
            </Typography>
            
            <List>
              <ListItem>
                <ListItemIcon>
                  <Info sx={{ color: '#3498db' }} />
                </ListItemIcon>
                <ListItemText
                  primary="Take Regular Breaks"
                  secondary="Step away from your desk every hour for a 5-minute stretch or walk"
                  sx={{ '& .MuiListItemText-primary': { color: 'white' }, '& .MuiListItemText-secondary': { color: '#bdc3c7' } }}
                />
              </ListItem>
              
              <ListItem>
                <ListItemIcon>
                  <Favorite sx={{ color: '#e74c3c' }} />
                </ListItemIcon>
                <ListItemText
                  primary="Practice Mindfulness"
                  secondary="Try a 2-minute breathing exercise when feeling stressed"
                  sx={{ '& .MuiListItemText-primary': { color: 'white' }, '& .MuiListItemText-secondary': { color: '#bdc3c7' } }}
                />
              </ListItem>
              
              <ListItem>
                <ListItemIcon>
                  <LocalHospital sx={{ color: '#27ae60' }} />
                </ListItemIcon>
                <ListItemText
                  primary="Stay Hydrated"
                  secondary="Drink water throughout the day to maintain energy levels"
                  sx={{ '& .MuiListItemText-primary': { color: 'white' }, '& .MuiListItemText-secondary': { color: '#bdc3c7' } }}
                />
              </ListItem>
            </List>
          </Paper>
        </Grid>

        {/* Quick Stats */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3, borderRadius: 4, bgcolor: '#34495e', color: 'white' }}>
            <Typography variant="h5" sx={{ mb: 3, color: 'white' }}>
              Quick Stats 📊
            </Typography>
            
            <List>
              <ListItem>
                <ListItemIcon>
                  <CheckCircle sx={{ color: '#27ae60' }} />
                </ListItemIcon>
                <ListItemText
                  primary={`${entries.length} Wellness Entries`}
                  secondary="This month"
                  sx={{ '& .MuiListItemText-primary': { color: 'white' }, '& .MuiListItemText-secondary': { color: '#bdc3c7' } }}
                />
              </ListItem>
              
              <ListItem>
                <ListItemIcon>
                  <Psychology sx={{ color: '#3498db' }} />
                </ListItemIcon>
                <ListItemText
                  primary={`${conversations.length} AI Conversations`}
                  secondary="This month"
                  sx={{ '& .MuiListItemText-primary': { color: 'white' }, '& .MuiListItemText-secondary': { color: '#bdc3c7' } }}
                />
              </ListItem>

              {hasRole(['manager', 'hr', 'admin']) && organizationalHealth && (
                <ListItem>
                  <ListItemIcon>
                    <TrendingUp sx={{ color: '#f39c12' }} />
                  </ListItemIcon>
                  <ListItemText
                    primary={`${Math.round(organizationalHealth.overallWellnessScore)}% Org Wellness`}
                    secondary="Organization average"
                    sx={{ '& .MuiListItemText-primary': { color: 'white' }, '& .MuiListItemText-secondary': { color: '#bdc3c7' } }}
                  />
                </ListItem>
              )}
            </List>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
