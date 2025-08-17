import React, { useState } from 'react';
import {
  Box,
  Container,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  Button,
  Chip,
  LinearProgress,
  Avatar,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Divider,
  IconButton,
  AppBar,
  Toolbar,
  Drawer,
  ListItemIcon,
  Badge,
  CircularProgress,
  Fab,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Stepper,
  Step,
  StepLabel,
  StepContent,
  Accordion,
  AccordionSummary,
  AccordionDetails
} from '@mui/material';

import {
  Dashboard as DashboardIcon,
  Favorite as WellnessIcon,
  Chat as ChatIcon,
  LibraryBooks as ResourcesIcon,
  Analytics as AnalyticsIcon,
  Person as ProfileIcon,
  Settings as SettingsIcon,
  Notifications as NotificationsIcon,
  Menu as MenuIcon,
  TrendingUp,
  TrendingDown,
  CheckCircle,
  Warning,
  Info,
  ExpandMore,
  Add,
  Psychology,
  Spa,
  FitnessCenter,
  SelfImprovement,
  EmojiEmotions,
  LocalHospital,
  School,
  Work,
  Home,
  Favorite,
  Star,
  PlayArrow,
  Pause,
  Stop
} from '@mui/icons-material';

// Mock data for the demo
const mockWellnessData = {
  currentMood: 8.5,
  stressLevel: 4.2,
  energyLevel: 7.8,
  sleepQuality: 7.2,
  recentCheckins: [
    { date: '2024-01-15', mood: 8, stress: 3, note: 'Feeling great today!', activity: 'Morning meditation' },
    { date: '2024-01-14', mood: 6, stress: 6, note: 'A bit stressed with deadlines', activity: 'Deep breathing' },
    { date: '2024-01-13', mood: 9, stress: 2, note: 'Excellent weekend vibes', activity: 'Nature walk' }
  ],
  wellnessJourney: [
    { week: 'Week 1', focus: 'Mindfulness', progress: 85, status: 'completed' },
    { week: 'Week 2', focus: 'Stress Management', progress: 70, status: 'in-progress' },
    { week: 'Week 3', focus: 'Physical Wellness', progress: 45, status: 'upcoming' },
    { week: 'Week 4', focus: 'Social Connection', progress: 0, status: 'upcoming' }
  ]
};

const mockResources = [
  { id: 1, title: 'Stress Management Techniques', category: 'Mental Health', rating: 4.8, views: 1247, duration: '15 min', type: 'video', status: 'complete' },
  { id: 2, title: 'Mindful Breathing Exercises', category: 'Meditation', rating: 4.9, views: 892, duration: '8 min', type: 'audio', status: 'started' },
  { id: 3, title: 'Desk Exercises for Office Workers', category: 'Physical Wellness', rating: 4.6, views: 1563, duration: '12 min', type: 'video', status: 'not-started' },
  { id: 4, title: 'Sleep Optimization Guide', category: 'Sleep', rating: 4.7, views: 1102, duration: '20 min', type: 'article', status: 'complete' },
  { id: 5, title: 'Nutrition for Mental Performance', category: 'Nutrition', rating: 4.5, views: 743, duration: '18 min', type: 'article', status: 'not-started' },
  { id: 6, title: 'Team Building Activities', category: 'Social Wellness', rating: 4.4, views: 567, duration: '25 min', type: 'video', status: 'not-started' },
  { id: 7, title: 'Mindfulness Meditation Basics', category: 'Meditation', rating: 4.8, views: 2341, duration: '10 min', type: 'audio', status: 'not-started' },
  { id: 8, title: 'Work-Life Balance Strategies', category: 'Mental Health', rating: 4.6, views: 1892, duration: '22 min', type: 'article', status: 'started' },
  { id: 9, title: 'Ergonomic Workspace Setup', category: 'Physical Wellness', rating: 4.7, views: 1456, duration: '14 min', type: 'video', status: 'not-started' },
  { id: 10, title: 'Digital Detox Techniques', category: 'Mental Health', rating: 4.5, views: 987, duration: '16 min', type: 'article', status: 'complete' },
  { id: 11, title: 'Healthy Snacking at Work', category: 'Nutrition', rating: 4.4, views: 1234, duration: '8 min', type: 'video', status: 'not-started' },
  { id: 12, title: 'Conflict Resolution Skills', category: 'Social Wellness', rating: 4.6, views: 876, duration: '18 min', type: 'article', status: 'not-started' }
];

const mockAnalytics = {
  organizationalHealth: 7.8,
  teamCollaboration: 8.3,
  employeeSatisfaction: 8.1,
  workLifeBalance: 7.4,
  riskLevel: 'Low',
  trends: [
    { metric: 'Overall Wellness', value: 7.8, trend: 'up', change: '+0.3' },
    { metric: 'Stress Levels', value: 6.2, trend: 'down', change: '-0.5' },
    { metric: 'Team Morale', value: 8.3, trend: 'up', change: '+0.2' },
    { metric: 'Productivity', value: 8.7, trend: 'up', change: '+0.4' }
  ]
};

function App() {
  const [tabValue, setTabValue] = useState(0);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [checkinDialogOpen, setCheckinDialogOpen] = useState(false);
  const [activeStep, setActiveStep] = useState(0);

  const handleTabChange = (newValue: number) => {
    setTabValue(newValue);
  };

  const handleDemoAction = () => {
    setCheckinDialogOpen(true);
  };

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const handleReset = () => {
    setActiveStep(0);
    setCheckinDialogOpen(false);
  };

  const steps = [
    {
      label: 'How are you feeling?',
      description: `Rate your current mood: ${mockWellnessData.currentMood}/10`,
    },
    {
      label: 'Stress Assessment',
      description: `Current stress level: ${mockWellnessData.stressLevel}/10`,
    },
    {
      label: 'Energy Check',
      description: `Energy level: ${mockWellnessData.energyLevel}/10`,
    },
    {
      label: 'Sleep Quality',
      description: `Sleep quality: ${mockWellnessData.sleepQuality}/10`,
    },
  ];

  const renderContent = () => {
    switch (tabValue) {
      case 0:
        return (
          <Grid container spacing={3}>
            {/* Welcome Section with Circular Progress */}
            <Grid item xs={12}>
              <Paper sx={{ p: 3, textAlign: 'center', bgcolor: '#2c3e50', color: 'white', borderRadius: 4 }}>
                <Box sx={{ position: 'relative', display: 'inline-flex', mb: 2 }}>
                  <CircularProgress
                    variant="determinate"
                    value={75}
                    size={100}
                    thickness={4}
                    sx={{ color: '#e74c3c' }}
                  />
                  <Box
                    sx={{
                      top: 0,
                      left: 0,
                      bottom: 0,
                      right: 0,
                      position: 'absolute',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                    }}
                  >
                    <Typography variant="h5" component="div" sx={{ color: 'white' }}>
                      75%
                    </Typography>
                  </Box>
                </Box>
                <Typography variant="h4" sx={{ mb: 1, color: 'white' }}>
                  Welcome back, John! 🌟
                </Typography>
                <Typography variant="body1" sx={{ mb: 2, color: '#bdc3c7' }}>
                  You're 75% through your wellness journey this month
                </Typography>
                <Button
                  variant="contained"
                  size="large"
                  onClick={handleDemoAction}
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
                  {mockWellnessData.wellnessJourney.map((journey, index) => (
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
                   <Button
                     variant="outlined"
                     fullWidth
                     startIcon={<Psychology />}
                     onClick={() => setTabValue(2)}
                     sx={{ 
                       borderColor: '#3498db', 
                       color: '#3498db',
                       '&:hover': { borderColor: '#2980b9', bgcolor: '#2c3e50' },
                       borderRadius: 3,
                       py: 2,
                       fontSize: '1.1rem',
                       fontWeight: 'bold'
                     }}
                   >
                     Mind
                   </Button>
                   <Button
                     variant="outlined"
                     fullWidth
                     startIcon={<FitnessCenter />}
                     onClick={() => setTabValue(3)}
                     sx={{ 
                       borderColor: '#e67e22', 
                       color: '#e67e22',
                       '&:hover': { borderColor: '#d35400', bgcolor: '#2c3e50' },
                       borderRadius: 3,
                       py: 2,
                       fontSize: '1.1rem',
                       fontWeight: 'bold'
                     }}
                   >
                     Body
                   </Button>
                   <Button
                     variant="outlined"
                     fullWidth
                     startIcon={<Spa />}
                     onClick={() => setTabValue(1)}
                     sx={{ 
                       borderColor: '#9b59b6', 
                       color: '#9b59b6',
                       '&:hover': { borderColor: '#8e44ad', bgcolor: '#2c3e50' },
                       borderRadius: 3,
                       py: 2,
                       fontSize: '1.1rem',
                       fontWeight: 'bold'
                     }}
                   >
                     Spirit
                   </Button>
                   <Button
                     variant="outlined"
                     fullWidth
                     startIcon={<EmojiEmotions />}
                     onClick={() => setTabValue(4)}
                     sx={{ 
                       borderColor: '#f1c40f', 
                       color: '#f1c40f',
                       '&:hover': { borderColor: '#f39c12', bgcolor: '#2c3e50' },
                       borderRadius: 3,
                       py: 2,
                       fontSize: '1.1rem',
                       fontWeight: 'bold'
                     }}
                   >
                     Joy
                   </Button>
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
                  {mockWellnessData.recentCheckins.map((checkin, index) => (
                    <Grid item xs={12} md={4} key={index}>
                      <Card sx={{ 
                        borderRadius: 3, 
                        bgcolor: checkin.mood >= 7 ? '#27ae60' : 
                                 checkin.mood >= 5 ? '#f39c12' : '#e74c3c',
                        border: `2px solid ${checkin.mood >= 7 ? '#2ecc71' : 
                                            checkin.mood >= 5 ? '#f1c40f' : '#c0392b'}`
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
                            {checkin.mood}
                          </Avatar>
                          <Typography variant="h6" sx={{ mb: 1, color: 'white' }}>
                            {checkin.activity}
                          </Typography>
                          <Typography variant="body2" sx={{ mb: 2, color: 'rgba(255,255,255,0.8)' }}>
                            {checkin.note}
                          </Typography>
                          <Chip 
                            label={`Mood: ${checkin.mood}/10`} 
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
          </Grid>
        );

      case 1:
        return (
          <Paper sx={{ p: 4, maxWidth: 800, mx: 'auto', borderRadius: 4, bgcolor: '#34495e', color: 'white' }}>
            <Typography variant="h4" sx={{ mb: 3, textAlign: 'center', color: 'white' }}>
              How are you feeling today? 🌸
            </Typography>
            <Typography variant="body1" sx={{ mb: 4, textAlign: 'center', color: '#bdc3c7' }}>
              Let's take a moment to check in with yourself
            </Typography>

            <Stepper activeStep={activeStep} orientation="vertical" sx={{ mb: 4 }}>
              {steps.map((step, index) => (
                <Step key={step.label}>
                  <StepLabel
                    optional={
                      index === 3 ? (
                        <Typography variant="caption" sx={{ color: '#bdc3c7' }}>Final step</Typography>
                      ) : null
                    }
                  >
                    <Typography sx={{ color: 'white' }}>{step.label}</Typography>
                  </StepLabel>
                  <StepContent>
                    <Typography sx={{ color: '#bdc3c7' }}>{step.description}</Typography>
                    <Box sx={{ mb: 2 }}>
                      <div>
                        <Button
                          variant="contained"
                          onClick={handleNext}
                          sx={{ mt: 1, mr: 1, bgcolor: '#e74c3c' }}
                        >
                          {index === steps.length - 1 ? 'Finish' : 'Continue'}
                        </Button>
                        <Button
                          disabled={index === 0}
                          onClick={handleBack}
                          sx={{ mt: 1, mr: 1 }}
                        >
                          Back
                        </Button>
                      </div>
                    </Box>
                  </StepContent>
                </Step>
              ))}
            </Stepper>
                         {activeStep === steps.length && (
               <Paper square elevation={0} sx={{ p: 3, my: 3, bgcolor: '#27ae60', borderRadius: 3 }}>
                 <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                   <Button onClick={handleReset} sx={{ bgcolor: 'rgba(255,255,255,0.2)', color: 'white', px: 3, py: 1.5 }}>
                     Reset
                   </Button>
                   <Typography sx={{ color: 'white', fontSize: '1.5rem', fontWeight: 'bold' }}>
                     All steps completed - you're all set! 🎉
                   </Typography>
                 </Box>
               </Paper>
             )}
          </Paper>
        );

             case 2:
         return (
           <Paper sx={{ p: 4, maxWidth: 900, mx: 'auto', borderRadius: 4, bgcolor: '#34495e', color: 'white' }}>
                           <Typography variant="h4" sx={{ mb: 3, textAlign: 'center', color: 'white' }}>
                AI Wellness Companion
              </Typography>
                           <Typography variant="body1" sx={{ mb: 4, textAlign: 'center', color: '#bdc3c7', fontSize: '1.1rem', fontWeight: 500 }}>
                Have a confidential conversation about your wellness journey
              </Typography>

             <Box sx={{ 
               height: 500, 
               border: 3, 
               borderColor: '#3498db', 
               borderRadius: 4, 
               p: 3, 
               mb: 3,
               bgcolor: '#2c3e50',
               display: 'flex',
               flexDirection: 'column',
               justifyContent: 'space-between'
             }}>
               <Box>
                                   <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <Avatar sx={{ bgcolor: '#3498db', mr: 2, width: 50, height: 50, fontSize: '1.5rem' }}>🤖</Avatar>
                    <Box>
                      <Typography variant="h6" sx={{ color: 'white', fontSize: '1.2rem', fontWeight: 'bold' }}>Wellness AI Assistant</Typography>
                      <Typography variant="body2" sx={{ color: '#bdc3c7', fontSize: '1rem', fontWeight: 500 }}>Online • Ready to help</Typography>
                    </Box>
                  </Box>
                 
                                   <Paper sx={{ p: 2, mb: 2, bgcolor: '#3498db', color: 'white', borderRadius: 3 }}>
                    <Typography variant="body2" sx={{ 
                      fontSize: '1.1rem', 
                      lineHeight: 1.2,
                      fontFamily: 'monospace',
                      fontWeight: 'bold'
                    }}>
                      Hello! I'm here to support your wellness journey. How are you feeling today? I can help with stress management, mood tracking, or any wellness concerns you might have.
                    </Typography>
                  </Paper>
                 
                                   <Paper sx={{ p: 2, mb: 2, bgcolor: '#7f8c8d', ml: 6, borderRadius: 3 }}>
                    <Typography variant="body2" sx={{ 
                      color: 'white', 
                      fontSize: '1.1rem', 
                      lineHeight: 1.2,
                      fontFamily: 'monospace',
                      fontWeight: 'bold'
                    }}>
                      I've been feeling a bit stressed lately with work deadlines. Any suggestions?
                    </Typography>
                  </Paper>
                 
                                   <Paper sx={{ p: 2, bgcolor: '#3498db', color: 'white', borderRadius: 3 }}>
                    <Typography variant="body2" sx={{ 
                      fontSize: '1.1rem', 
                      lineHeight: 1.2,
                      fontFamily: 'monospace',
                      fontWeight: 'bold'
                    }}>
                      I understand work stress can be challenging! Let me suggest some techniques: 
                      <br/>• Take regular 5-minute breaks every hour
                      <br/>• Practice deep breathing exercises  
                      <br/>• Prioritize your tasks
                      <br/><br/>Would you like me to guide you through a quick stress relief exercise?
                    </Typography>
                  </Paper>
               </Box>
             </Box>

                         <Button
               variant="contained"
               size="large"
               fullWidth
               onClick={() => alert('Demo: This would open a full chat interface with the AI assistant!')}
               sx={{ 
                 py: 2, 
                 bgcolor: '#e67e22',
                 '&:hover': { bgcolor: '#d35400' },
                 borderRadius: 3,
                 color: 'black',
                 fontWeight: 'bold',
                 fontSize: '1.1rem'
               }}
             >
               Start New Conversation
             </Button>
          </Paper>
        );

      case 3:
        return (
          <Box>
            <Typography variant="h4" sx={{ mb: 3, color: 'white' }}>
              Learning Hub 📚
            </Typography>
            <Typography variant="body1" sx={{ mb: 4, color: '#bdc3c7' }}>
              Explore wellness resources tailored to your journey
            </Typography>
            
            <Grid container spacing={3}>
              {mockResources.map((resource) => (
                <Grid item xs={12} md={6} key={resource.id}>
                                     <Accordion sx={{ 
                     borderRadius: 3, 
                     mb: 2, 
                     bgcolor: resource.status === 'complete' ? '#7f8c8d' : 
                              resource.status === 'started' ? '#27ae60' : '#3498db',
                     position: 'relative'
                   }}>
                     <AccordionSummary expandIcon={<ExpandMore sx={{ color: 'white' }} />}>
                       <Box sx={{ display: 'flex', alignItems: 'center', width: '100%' }}>
                         <Avatar sx={{ 
                           mr: 2, 
                           bgcolor: 'rgba(255,255,255,0.2)'
                         }}>
                           {resource.status === 'complete' ? <CheckCircle /> : 
                            resource.status === 'started' ? <Pause /> : <PlayArrow />}
                         </Avatar>
                         <Box sx={{ flexGrow: 1 }}>
                           <Typography variant="h6" sx={{ color: 'white' }}>{resource.title}</Typography>
                           <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.8)' }}>
                             {resource.category} • {resource.duration}
                           </Typography>
                         </Box>
                         <Box sx={{ display: 'flex', alignItems: 'center' }}>
                           <Star sx={{ color: '#f1c40f', mr: 0.5 }} />
                           <Typography variant="body2" sx={{ color: 'white' }}>{resource.rating}</Typography>
                         </Box>
                                                   <Typography 
                            variant="caption" 
                            sx={{ 
                              position: 'absolute',
                              top: 0,
                              right: 0,
                              color: 'white',
                              fontStyle: 'italic',
                              fontSize: '0.65rem',
                              fontWeight: 500,
                              backgroundColor: 'rgba(0,0,0,0.3)',
                              padding: '2px 6px',
                              borderRadius: '0 12px 0 8px',
                              zIndex: 1
                            }}
                          >
                            {resource.status === 'complete' ? 'Complete!' : 
                             resource.status === 'started' ? 'Started!' : 'Not started!'}
                          </Typography>
                       </Box>
                     </AccordionSummary>
                    <AccordionDetails sx={{ bgcolor: '#2c3e50' }}>
                      <Typography variant="body2" sx={{ mb: 2, color: '#bdc3c7' }}>
                        This resource will help you improve your {resource.category.toLowerCase()} and overall wellness.
                      </Typography>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <Typography variant="body2" sx={{ color: '#bdc3c7' }}>
                          {resource.views} views
                        </Typography>
                        <Button 
                          variant="contained" 
                          size="small"
                          onClick={() => alert(`Demo: This would open "${resource.title}" resource!`)}
                          sx={{ bgcolor: '#e74c3c' }}
                        >
                          Start Learning
                        </Button>
                      </Box>
                    </AccordionDetails>
                  </Accordion>
                </Grid>
              ))}
            </Grid>
          </Box>
        );

      case 4:
        return (
          <Box>
            <Typography variant="h4" sx={{ mb: 3, color: 'white' }}>
              Wellness Insights 📊
            </Typography>
            
            <Grid container spacing={3}>
              {/* Main Insight Card */}
              <Grid item xs={12}>
                <Paper sx={{ p: 4, borderRadius: 4, bgcolor: '#34495e', color: 'white' }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                    <Avatar sx={{ bgcolor: '#27ae60', mr: 2, width: 60, height: 60 }}>
                      <TrendingUp sx={{ fontSize: 30 }} />
                    </Avatar>
                    <Box>
                      <Typography variant="h5" sx={{ color: 'white' }}>
                        Overall Wellness Score
                      </Typography>
                      <Typography variant="h3" sx={{ color: '#27ae60', fontWeight: 'bold' }}>
                        {mockAnalytics.organizationalHealth}/10
                      </Typography>
                    </Box>
                  </Box>
                  <Typography variant="body1" sx={{ mb: 2, color: '#bdc3c7' }}>
                    Your wellness journey is showing positive trends! Keep up the great work. 🌟
                  </Typography>
                </Paper>
              </Grid>

              {/* Trend Cards in a Circle Layout */}
              <Grid item xs={12}>
                <Paper sx={{ p: 4, borderRadius: 4, bgcolor: '#34495e' }}>
                  <Typography variant="h5" sx={{ mb: 3, textAlign: 'center', color: 'white' }}>
                    Recent Trends 📈
                  </Typography>
                  <Grid container spacing={3} justifyContent="center">
                    {mockAnalytics.trends.map((trend, index) => (
                      <Grid item xs={12} sm={6} md={3} key={index}>
                        <Card sx={{ 
                          borderRadius: '50%', 
                          width: 150, 
                          height: 150, 
                          mx: 'auto',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          bgcolor: trend.trend === 'up' ? '#27ae60' : '#e74c3c',
                          border: `3px solid ${trend.trend === 'up' ? '#2ecc71' : '#c0392b'}`
                        }}>
                          <CardContent sx={{ textAlign: 'center' }}>
                            <Typography variant="h4" sx={{ color: 'white' }}>
                              {trend.value}
                            </Typography>
                            <Typography variant="body2" sx={{ fontSize: '0.8rem', color: 'white' }}>
                              {trend.metric}
                            </Typography>
                            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', mt: 1 }}>
                              {trend.trend === 'up' ? (
                                <TrendingUp sx={{ color: 'white', fontSize: 20 }} />
                              ) : (
                                <TrendingDown sx={{ color: 'white', fontSize: 20 }} />
                              )}
                              <Typography variant="caption" sx={{ ml: 0.5, color: 'white' }}>
                                {trend.change}
                              </Typography>
                            </Box>
                          </CardContent>
                        </Card>
                      </Grid>
                    ))}
                  </Grid>
                </Paper>
              </Grid>

              {/* Risk Assessment */}
              <Grid item xs={12} md={6}>
                <Paper sx={{ p: 3, borderRadius: 4, bgcolor: '#34495e' }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <CheckCircle sx={{ color: '#27ae60', mr: 1, fontSize: 30 }} />
                    <Typography variant="h5" sx={{ color: '#27ae60' }}>
                      Risk Assessment
                    </Typography>
                  </Box>
                  <Typography variant="h4" sx={{ mb: 2, color: '#27ae60' }}>
                    {mockAnalytics.riskLevel} Risk
                  </Typography>
                  <Typography variant="body2" sx={{ mb: 1, color: '#bdc3c7' }}>
                    • High workload periods: Medium risk
                  </Typography>
                  <Typography variant="body2" sx={{ mb: 1, color: '#bdc3c7' }}>
                    • Screen time exposure: Low risk
                  </Typography>
                  <Typography variant="body2" sx={{ mb: 1, color: '#bdc3c7' }}>
                    • Sedentary work style: Low risk
                  </Typography>
                </Paper>
              </Grid>

              {/* Wellness Areas */}
              <Grid item xs={12} md={6}>
                <Paper sx={{ p: 3, borderRadius: 4, bgcolor: '#34495e' }}>
                  <Typography variant="h5" sx={{ mb: 3, color: 'white' }}>
                    Wellness Areas
                  </Typography>
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="body2" sx={{ mb: 1, color: '#bdc3c7' }}>Team Collaboration</Typography>
                    <LinearProgress 
                      variant="determinate" 
                      value={mockAnalytics.teamCollaboration * 10} 
                      sx={{ height: 10, borderRadius: 5, bgcolor: '#2c3e50' }}
                    />
                  </Box>
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="body2" sx={{ mb: 1, color: '#bdc3c7' }}>Employee Satisfaction</Typography>
                    <LinearProgress 
                      variant="determinate" 
                      value={mockAnalytics.employeeSatisfaction * 10} 
                      sx={{ height: 10, borderRadius: 5, bgcolor: '#2c3e50' }}
                    />
                  </Box>
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="body2" sx={{ mb: 1, color: '#bdc3c7' }}>Work-Life Balance</Typography>
                    <LinearProgress 
                      variant="determinate" 
                      value={mockAnalytics.workLifeBalance * 10} 
                      sx={{ height: 10, borderRadius: 5, bgcolor: '#2c3e50' }}
                    />
                  </Box>
                </Paper>
              </Grid>
            </Grid>
          </Box>
        );

                           case 5:
          return (
            <Paper sx={{ p: 4, maxWidth: 600, mx: 'auto', borderRadius: 4, bgcolor: '#34495e', color: 'white' }}>
              <Typography variant="h4" sx={{ mb: 3, textAlign: 'center', color: 'white' }}>
                Your Profile
              </Typography>
              <Box sx={{ textAlign: 'center', mb: 4 }}>
                                 <Box 
                   sx={{ 
                     width: 120, 
                     height: 120, 
                     mx: 'auto', 
                     mb: 3, 
                     borderRadius: '50%',
                     backgroundImage: 'url(https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face)',
                     backgroundSize: 'cover',
                     backgroundPosition: 'center',
                     border: '3px solid #ffffff',
                     boxShadow: '0 4px 12px rgba(0,0,0,0.3)'
                   }}
                 />
                <Typography variant="h5" sx={{ color: 'white' }}>John Doe</Typography>
                <Typography variant="body1" sx={{ color: '#bdc3c7' }}>Software Engineer</Typography>
                <Chip 
                  label="Wellness Champion" 
                  sx={{ 
                    mt: 2, 
                    bgcolor: '#27ae60', 
                    color: 'white',
                    fontWeight: 'bold',
                    fontSize: '1rem',
                    padding: '8px 16px',
                    borderRadius: '20px',
                    boxShadow: '0 4px 8px rgba(0,0,0,0.3)',
                    textShadow: '0 1px 2px rgba(0,0,0,0.5)',
                    border: '2px solid #2ecc71'
                  }} 
                />
              </Box>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Button variant="contained" fullWidth onClick={() => alert('Demo: This would open profile editing form!')} sx={{ bgcolor: '#e74c3c' }}>
                  Edit Profile
                </Button>
              </Grid>
              <Grid item xs={12}>
                <Button variant="outlined" fullWidth onClick={() => alert('Demo: This would open privacy settings!')} sx={{ borderColor: '#bdc3c7', color: '#bdc3c7' }}>
                  Privacy Settings
                </Button>
              </Grid>
              <Grid item xs={12}>
                <Button variant="outlined" fullWidth onClick={() => alert('Demo: This would open notification preferences!')} sx={{ borderColor: '#bdc3c7', color: '#bdc3c7' }}>
                  Notification Preferences
                </Button>
              </Grid>
            </Grid>
          </Paper>
        );

      case 6:
        return (
          <Paper sx={{ p: 4, maxWidth: 600, mx: 'auto', borderRadius: 4, bgcolor: '#34495e', color: 'white' }}>
            <Typography variant="h4" sx={{ mb: 3, textAlign: 'center', color: 'white' }}>
              Settings ⚙️
            </Typography>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Button variant="contained" fullWidth onClick={() => alert('Demo: This would open theme settings!')} sx={{ bgcolor: '#e74c3c' }}>
                  Theme Settings
                </Button>
              </Grid>
              <Grid item xs={12}>
                <Button variant="outlined" fullWidth onClick={() => alert('Demo: This would open data export options!')} sx={{ borderColor: '#bdc3c7', color: '#bdc3c7' }}>
                  Export My Data
                </Button>
              </Grid>
              <Grid item xs={12}>
                <Button variant="outlined" fullWidth onClick={() => alert('Demo: This would open account deletion options!')} sx={{ borderColor: '#bdc3c7', color: '#bdc3c7' }}>
                  Account Settings
                </Button>
              </Grid>
              <Grid item xs={12}>
                <Button variant="outlined" color="error" fullWidth onClick={() => alert('Demo: This would open logout confirmation!')} sx={{ borderColor: '#e74c3c', color: '#e74c3c' }}>
                  Logout
                </Button>
              </Grid>
            </Grid>
          </Paper>
        );

      default:
        return null;
    }
  };

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: '#2c3e50' }}>
      {/* Header */}
      <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1, bgcolor: '#1a252f' }}>
        <Toolbar>
          <IconButton
            color="inherit"
            edge="start"
            onClick={() => setDrawerOpen(!drawerOpen)}
            sx={{ mr: 2 }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            🌟 Wellness Journey
          </Typography>
          <IconButton color="inherit">
            <Badge badgeContent={3} color="error">
              <NotificationsIcon />
            </Badge>
          </IconButton>
                     <Box 
             sx={{ 
               ml: 2, 
               width: 40,
               height: 40,
               borderRadius: '50%',
               backgroundImage: 'url(https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=40&h=40&fit=crop&crop=face)',
               backgroundSize: 'cover',
               backgroundPosition: 'center',
               border: '2px solid #ffffff'
             }}
           />
        </Toolbar>
      </AppBar>

      {/* Sidebar */}
      <Drawer
        variant="permanent"
        sx={{
          width: 240,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: 240,
            boxSizing: 'border-box',
            top: 64,
            height: 'calc(100% - 64px)',
            bgcolor: '#1a252f',
            color: 'white',
          },
        }}
      >
        <List sx={{ pt: 2 }}>
          <ListItem button selected={tabValue === 0} onClick={() => handleTabChange(0)} sx={{ '&.Mui-selected': { bgcolor: '#e74c3c' } }}>
            <ListItemIcon sx={{ color: 'white' }}><DashboardIcon /></ListItemIcon>
            <ListItemText primary="My Journey" />
          </ListItem>
          <ListItem button selected={tabValue === 1} onClick={() => handleTabChange(1)} sx={{ '&.Mui-selected': { bgcolor: '#e74c3c' } }}>
            <ListItemIcon sx={{ color: 'white' }}><WellnessIcon /></ListItemIcon>
            <ListItemText primary="Daily Check-in" />
          </ListItem>
          <ListItem button selected={tabValue === 2} onClick={() => handleTabChange(2)} sx={{ '&.Mui-selected': { bgcolor: '#e74c3c' } }}>
            <ListItemIcon sx={{ color: 'white' }}><ChatIcon /></ListItemIcon>
            <ListItemText primary="AI Companion" />
          </ListItem>
          <ListItem button selected={tabValue === 3} onClick={() => handleTabChange(3)} sx={{ '&.Mui-selected': { bgcolor: '#e74c3c' } }}>
            <ListItemIcon sx={{ color: 'white' }}><ResourcesIcon /></ListItemIcon>
            <ListItemText primary="Learning Hub" />
          </ListItem>
          <ListItem button selected={tabValue === 4} onClick={() => handleTabChange(4)} sx={{ '&.Mui-selected': { bgcolor: '#e74c3c' } }}>
            <ListItemIcon sx={{ color: 'white' }}><AnalyticsIcon /></ListItemIcon>
            <ListItemText primary="Insights" />
          </ListItem>
          <ListItem button selected={tabValue === 5} onClick={() => handleTabChange(5)} sx={{ '&.Mui-selected': { bgcolor: '#e74c3c' } }}>
            <ListItemIcon sx={{ color: 'white' }}><ProfileIcon /></ListItemIcon>
            <ListItemText primary="Profile" />
          </ListItem>
          <ListItem button selected={tabValue === 6} onClick={() => handleTabChange(6)} sx={{ '&.Mui-selected': { bgcolor: '#e74c3c' } }}>
            <ListItemIcon sx={{ color: 'white' }}><SettingsIcon /></ListItemIcon>
            <ListItemText primary="Settings" />
          </ListItem>
        </List>
      </Drawer>

      {/* Main Content */}
      <Box component="main" sx={{ flexGrow: 1, p: 3, mt: 8 }}>
        <Container maxWidth="xl">
          {renderContent()}
        </Container>
      </Box>

      {/* Floating Action Button */}
      <Fab
        color="primary"
        aria-label="add"
        sx={{ 
          position: 'fixed', 
          bottom: 16, 
          right: 16, 
          bgcolor: '#e74c3c',
          '&:hover': { bgcolor: '#c0392b' }
        }}
        onClick={handleDemoAction}
      >
        <Add />
      </Fab>

      {/* Check-in Dialog */}
      <Dialog open={checkinDialogOpen} onClose={() => setCheckinDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle sx={{ bgcolor: '#34495e', color: 'white' }}>Daily Wellness Check-in 🌟</DialogTitle>
        <DialogContent sx={{ bgcolor: '#2c3e50', color: 'white' }}>
          <Typography>
            This would open a comprehensive wellness check-in form with mood sliders, stress assessment, and AI-powered recommendations!
          </Typography>
        </DialogContent>
        <DialogActions sx={{ bgcolor: '#2c3e50' }}>
          <Button onClick={() => setCheckinDialogOpen(false)} sx={{ color: '#bdc3c7' }}>Close</Button>
          <Button onClick={() => setCheckinDialogOpen(false)} variant="contained" sx={{ bgcolor: '#e74c3c' }}>
            Start Check-in
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default App;
