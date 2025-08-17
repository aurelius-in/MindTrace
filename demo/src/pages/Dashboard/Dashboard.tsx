import React, { useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Avatar,
  Chip,
  LinearProgress,
} from '@mui/material';
import {
  TrendingUp,
  Favorite,
  Chat,
  LibraryBooks,
  Analytics,
  CheckCircle,
} from '@mui/icons-material';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { RootState } from '../../store';
import { fetchWellnessHistory } from '../../store/slices/wellnessSlice';

const Dashboard: React.FC = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { user } = useSelector((state: RootState) => state.auth);
  const { analytics } = useSelector((state: RootState) => state.wellness);

  useEffect(() => {
    dispatch(fetchWellnessHistory());
  }, [dispatch]);

  const quickActions = [
    {
      title: 'Wellness Check-in',
      description: 'Complete your daily wellness assessment',
      icon: <CheckCircle sx={{ fontSize: 40, color: 'primary.main' }} />,
      path: '/wellness/check-in',
      color: '#e3f2fd',
    },
    {
      title: 'AI Wellness Chat',
      description: 'Chat with our AI wellness companion',
      icon: <Chat sx={{ fontSize: 40, color: 'secondary.main' }} />,
      path: '/wellness/chat',
      color: '#f3e5f5',
    },
    {
      title: 'Wellness Resources',
      description: 'Access wellness resources and guides',
      icon: <LibraryBooks sx={{ fontSize: 40, color: 'success.main' }} />,
      path: '/resources',
      color: '#e8f5e8',
    },
    {
      title: 'Analytics',
      description: 'View your wellness analytics',
      icon: <Analytics sx={{ fontSize: 40, color: 'warning.main' }} />,
      path: '/analytics',
      color: '#fff3e0',
    },
  ];

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Good morning';
    if (hour < 18) return 'Good afternoon';
    return 'Good evening';
  };

  return (
    <Box sx={{ p: 3 }}>
      {/* Welcome Section */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" sx={{ fontWeight: 600, mb: 1 }}>
          {getGreeting()}, {user?.firstName}!
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Welcome to your wellness dashboard. Here's how you're doing today.
        </Typography>
      </Box>

      {/* Wellness Overview Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Avatar sx={{ bgcolor: 'primary.light', mr: 2 }}>
                  <Favorite />
                </Avatar>
                <Typography variant="h6" component="div">
                  Overall Wellness
                </Typography>
              </Box>
              <Typography variant="h4" sx={{ fontWeight: 600, mb: 1 }}>
                {analytics.averageMood.toFixed(1)}/10
              </Typography>
              <LinearProgress
                variant="determinate"
                value={(analytics.averageMood / 10) * 100}
                sx={{ mb: 1 }}
              />
              <Typography variant="body2" color="text.secondary">
                {analytics.trend === 'improving' ? 'Trending up' : analytics.trend === 'declining' ? 'Needs attention' : 'Stable'}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Avatar sx={{ bgcolor: 'error.light', mr: 2 }}>
                  <TrendingUp />
                </Avatar>
                <Typography variant="h6" component="div">
                  Stress Level
                </Typography>
              </Box>
              <Typography variant="h4" sx={{ fontWeight: 600, mb: 1 }}>
                {analytics.averageStress.toFixed(1)}/10
              </Typography>
              <LinearProgress
                variant="determinate"
                value={(analytics.averageStress / 10) * 100}
                color="error"
                sx={{ mb: 1 }}
              />
              <Typography variant="body2" color="text.secondary">
                {analytics.averageStress < 5 ? 'Low stress' : analytics.averageStress < 7 ? 'Moderate stress' : 'High stress'}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Avatar sx={{ bgcolor: 'success.light', mr: 2 }}>
                  <TrendingUp />
                </Avatar>
                <Typography variant="h6" component="div">
                  Energy Level
                </Typography>
              </Box>
              <Typography variant="h4" sx={{ fontWeight: 600, mb: 1 }}>
                {analytics.averageEnergy.toFixed(1)}/10
              </Typography>
              <LinearProgress
                variant="determinate"
                value={(analytics.averageEnergy / 10) * 100}
                color="success"
                sx={{ mb: 1 }}
              />
              <Typography variant="body2" color="text.secondary">
                {analytics.averageEnergy > 7 ? 'High energy' : analytics.averageEnergy > 5 ? 'Moderate energy' : 'Low energy'}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Avatar sx={{ bgcolor: 'warning.light', mr: 2 }}>
                  <CheckCircle />
                </Avatar>
                <Typography variant="h6" component="div">
                  Check-ins
                </Typography>
              </Box>
              <Typography variant="h4" sx={{ fontWeight: 600, mb: 1 }}>
                12
              </Typography>
              <Typography variant="body2" color="text.secondary">
                This month
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Quick Actions */}
      <Typography variant="h5" sx={{ fontWeight: 600, mb: 3 }}>
        Quick Actions
      </Typography>
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {quickActions.map((action) => (
          <Grid item xs={12} sm={6} md={3} key={action.title}>
            <Card
              sx={{
                height: '100%',
                cursor: 'pointer',
                transition: 'transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  boxShadow: '0 8px 25px rgba(0,0,0,0.15)',
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
                <Button variant="outlined" size="small">
                  Get Started
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Recent Activity */}
      <Typography variant="h5" sx={{ fontWeight: 600, mb: 3 }}>
        Recent Activity
      </Typography>
      <Card>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <Chip label="Today" color="primary" size="small" sx={{ mr: 2 }} />
            <Typography variant="body2" color="text.secondary">
              Last updated: {new Date().toLocaleTimeString()}
            </Typography>
          </Box>
          <Typography variant="body1" sx={{ mb: 2 }}>
            • Completed wellness check-in with a score of 7.5/10
          </Typography>
          <Typography variant="body1" sx={{ mb: 2 }}>
            • Viewed "Mindful Breathing Techniques" resource
          </Typography>
          <Typography variant="body1" sx={{ mb: 2 }}>
            • Had a conversation with AI wellness companion
          </Typography>
          <Typography variant="body1">
            • Received wellness goal achievement notification
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Dashboard;
