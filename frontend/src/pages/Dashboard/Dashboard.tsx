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
        title: 'Wellness Check-in',
        description: 'Track your current mood and stress level',
        icon: <CheckCircle color="primary" />,
        path: '/wellness/check-in',
        color: 'primary.main',
      },
      {
        title: 'Chat with AI',
        description: 'Get personalized wellness support',
        icon: <Psychology color="secondary" />,
        path: '/wellness/chat',
        color: 'secondary.main',
      },
      {
        title: 'Browse Resources',
        description: 'Find wellness exercises and articles',
        icon: <FitnessCenter color="success" />,
        path: '/resources',
        color: 'success.main',
      },
    ];

    // Add manager-specific actions
    if (hasRole(['manager', 'hr', 'admin'])) {
      actions.push({
        title: 'Team Analytics',
        description: 'View team wellness insights',
        icon: <TrendingUp color="info" />,
        path: '/analytics/team',
        color: 'info.main',
      });
    }

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
      });
    });

    return activities.sort((a, b) => new Date(b.time).getTime() - new Date(a.time).getTime());
  };

  if (isLoading) {
    return <LoadingSpinner message="Loading your wellness dashboard..." />;
  }

  return (
    <Box sx={{ p: 3 }}>
      {/* Welcome Section */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" sx={{ fontWeight: 600, mb: 1 }}>
          Welcome back, {user?.firstName}!
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Here's your wellness overview for today
        </Typography>
      </Box>

      <Grid container spacing={3}>
        {/* Wellness Overview */}
        <Grid item xs={12} md={8}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                Wellness Overview
              </Typography>
              
              <Grid container spacing={3}>
                {/* Wellness Score */}
                <Grid item xs={12} sm={6}>
                  <Box sx={{ textAlign: 'center' }}>
                    <Typography variant="h3" sx={{ fontWeight: 700, color: 'primary.main' }}>
                      {getWellnessScore()}%
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Overall Wellness Score
                    </Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', mt: 1 }}>
                      {getMoodTrend() === 'up' ? (
                        <TrendingUp color="success" fontSize="small" />
                      ) : getMoodTrend() === 'down' ? (
                        <TrendingDown color="error" fontSize="small" />
                      ) : (
                        <TrendingUp color="action" fontSize="small" />
                      )}
                      <Typography variant="caption" sx={{ ml: 0.5 }}>
                        {getMoodTrend() === 'up' ? 'Improving' : getMoodTrend() === 'down' ? 'Declining' : 'Stable'}
                      </Typography>
                    </Box>
                  </Box>
                </Grid>

                {/* Current Status */}
                <Grid item xs={12} sm={6}>
                  <Box>
                    <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 2 }}>
                      Current Status
                    </Typography>
                    
                    {currentMood !== null && (
                      <Box sx={{ mb: 2 }}>
                        <Typography variant="body2" color="text.secondary">
                          Current Mood
                        </Typography>
                        <LinearProgress
                          variant="determinate"
                          value={(currentMood / 10) * 100}
                          sx={{ height: 8, borderRadius: 4, mb: 1 }}
                        />
                        <Typography variant="body2">
                          {currentMood}/10
                        </Typography>
                      </Box>
                    )}

                    {lastCheckIn && (
                      <Box>
                        <Typography variant="body2" color="text.secondary">
                          Last Check-in
                        </Typography>
                        <Typography variant="body2">
                          {new Date(lastCheckIn).toLocaleDateString()}
                        </Typography>
                      </Box>
                    )}
                  </Box>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Quick Stats */}
        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                Quick Stats
              </Typography>
              
              <List>
                <ListItem>
                  <ListItemIcon>
                    <CheckCircle color="success" />
                  </ListItemIcon>
                  <ListItemText
                    primary={`${entries.length} Wellness Entries`}
                    secondary="This month"
                  />
                </ListItem>
                
                <ListItem>
                  <ListItemIcon>
                    <Psychology color="primary" />
                  </ListItemIcon>
                  <ListItemText
                    primary={`${conversations.length} AI Conversations`}
                    secondary="This month"
                  />
                </ListItem>

                {hasRole(['manager', 'hr', 'admin']) && organizationalHealth && (
                  <ListItem>
                    <ListItemIcon>
                      <TrendingUp color="info" />
                    </ListItemIcon>
                    <ListItemText
                      primary={`${Math.round(organizationalHealth.overallWellnessScore)}% Org Wellness`}
                      secondary="Organization average"
                    />
                  </ListItem>
                )}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Quick Actions */}
        <Grid item xs={12}>
          <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
            Quick Actions
          </Typography>
          <Grid container spacing={2}>
            {getQuickActions().map((action, index) => (
              <Grid item xs={12} sm={6} md={3} key={index}>
                <Card
                  sx={{
                    cursor: 'pointer',
                    transition: 'transform 0.2s ease-in-out',
                    '&:hover': {
                      transform: 'translateY(-2px)',
                    },
                  }}
                  onClick={() => navigate(action.path)}
                >
                  <CardContent sx={{ textAlign: 'center', p: 3 }}>
                    <Box sx={{ mb: 2 }}>
                      {action.icon}
                    </Box>
                    <Typography variant="h6" sx={{ fontWeight: 600, mb: 1 }}>
                      {action.title}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                      {action.description}
                    </Typography>
                    <Button
                      variant="outlined"
                      size="small"
                      endIcon={<ArrowForward />}
                      sx={{ borderColor: action.color, color: action.color }}
                    >
                      Get Started
                    </Button>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Grid>

        {/* Recent Activity */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                Recent Activity
              </Typography>
              
              <List>
                {getRecentActivity().map((activity, index) => (
                  <React.Fragment key={index}>
                    <ListItem>
                      <ListItemIcon>
                        {activity.icon}
                      </ListItemIcon>
                      <ListItemText
                        primary={activity.title}
                        secondary={
                          <Box>
                            <Typography variant="body2" color="text.secondary">
                              {activity.description}
                            </Typography>
                            <Typography variant="caption" color="text.secondary">
                              {activity.time}
                            </Typography>
                          </Box>
                        }
                      />
                    </ListItem>
                    {index < getRecentActivity().length - 1 && <Divider />}
                  </React.Fragment>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Wellness Tips */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                Wellness Tips
              </Typography>
              
              <List>
                <ListItem>
                  <ListItemIcon>
                    <Info color="info" />
                  </ListItemIcon>
                  <ListItemText
                    primary="Take Regular Breaks"
                    secondary="Step away from your desk every hour for a 5-minute stretch or walk"
                  />
                </ListItem>
                
                <ListItem>
                  <ListItemIcon>
                    <Favorite color="error" />
                  </ListItemIcon>
                  <ListItemText
                    primary="Practice Mindfulness"
                    secondary="Try a 2-minute breathing exercise when feeling stressed"
                  />
                </ListItem>
                
                <ListItem>
                  <ListItemIcon>
                    <LocalHospital color="success" />
                  </ListItemIcon>
                  <ListItemText
                    primary="Stay Hydrated"
                    secondary="Drink water throughout the day to maintain energy levels"
                  />
                </ListItem>
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
