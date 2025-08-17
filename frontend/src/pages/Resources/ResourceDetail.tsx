import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Button,
  Chip,
  Avatar,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
  LinearProgress,
  Rating,
  TextField,
  Alert,
  Tabs,
  Tab,
  Paper,
  IconButton,
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Slider,
  Fab,
  SpeedDial,
  SpeedDialAction,
  SpeedDialIcon,
  Badge,
  Skeleton,
  useTheme,
  useMediaQuery,
  Fade,
  Zoom,
  Grow,
} from '@mui/material';
import {
  PlayArrow,
  Pause,
  Stop,
  Favorite,
  FavoriteBorder,
  Share,
  Bookmark,
  BookmarkBorder,
  Star,
  AccessTime,
  Person,
  Category,
  TrendingUp,
  CheckCircle,
  ExpandMore,
  Close,
  ArrowBack,
  Download,
  Print,
  Comment,
  ThumbUp,
  ThumbDown,
  VolumeUp,
  VolumeOff,
  Fullscreen,
  FullscreenExit,
  Speed,
  Subtitles,
  Accessibility,
  Visibility,
  VisibilityOff,
  Timer,
  EmojiEvents,
  Psychology,
  SelfImprovement,
  Spa,
  FitnessCenter,
  Restaurant,
  School,
  Work,
  Family,
  Pets,
  Nature,
  MusicNote,
  VideoLibrary,
  Article,
  Podcasts,
  Web,
  Phone,
  Email,
  LinkedIn,
  Twitter,
  Facebook,
  WhatsApp,
  Telegram,
  ContentCopy,
  Check,
  Error,
  Warning,
  Info,
  Help,
} from '@mui/icons-material';
import { useDispatch, useSelector } from 'react-redux';
import { useParams, useNavigate } from 'react-router-dom';

import { RootState } from '../../store';
import { recordInteraction } from '../../store/slices/resourcesSlice';
import { addNotification } from '../../store/slices/uiSlice';
import LoadingSpinner from '../../components/Common/LoadingSpinner';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

const TabPanel: React.FC<TabPanelProps> = ({ children, value, index, ...other }) => (
  <div
    role="tabpanel"
    hidden={value !== index}
    id={`resource-tabpanel-${index}`}
    aria-labelledby={`resource-tab-${index}`}
    {...other}
  >
    {value === index && <Box sx={{ pt: 3 }}>{children}</Box>}
  </div>
);

const ResourceDetail: React.FC = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const { resourceId } = useParams<{ resourceId: string }>();
  const { resources, favorites } = useSelector((state: RootState) => state.resources);
  
  // State management
  const [tabValue, setTabValue] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [progress, setProgress] = useState(0);
  const [rating, setRating] = useState(0);
  const [comment, setComment] = useState('');
  const [showShareDialog, setShowShareDialog] = useState(false);
  const [showFeedbackDialog, setShowFeedbackDialog] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [volume, setVolume] = useState(80);
  const [isMuted, setIsMuted] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [playbackSpeed, setPlaybackSpeed] = useState(1);
  const [showSubtitles, setShowSubtitles] = useState(false);
  const [accessibilityMode, setAccessibilityMode] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(900); // 15 minutes in seconds
  const [userEngagement, setUserEngagement] = useState({
    timeSpent: 0,
    interactions: 0,
    completionRate: 0,
    lastAccessed: new Date(),
  });

  // Refs
  const progressIntervalRef = useRef<NodeJS.Timeout | null>(null);
  const mediaPlayerRef = useRef<HTMLDivElement>(null);

  // Enhanced mock resource data
  const resource = {
    id: resourceId || '1',
    title: 'Mindfulness Meditation for Stress Relief',
    description: 'A comprehensive guide to mindfulness meditation techniques designed to help reduce stress and improve mental well-being in the workplace.',
    category: 'mindfulness',
    difficultyLevel: 'beginner',
    durationMinutes: 15,
    tags: ['meditation', 'stress-relief', 'mindfulness', 'beginner-friendly'],
    content: {
      overview: 'This resource provides step-by-step guidance for practicing mindfulness meditation, specifically tailored for workplace stress management. Learn proven techniques to reduce anxiety, improve focus, and enhance overall well-being.',
      instructions: [
        'Find a quiet, comfortable space where you won\'t be interrupted',
        'Sit in a relaxed but alert posture with your back straight',
        'Close your eyes and take three deep, cleansing breaths',
        'Focus your attention on your natural breath rhythm',
        'When your mind wanders, gently bring it back to your breath',
        'Practice for 10-15 minutes daily for best results'
      ],
      benefits: [
        'Reduces stress and anxiety levels by 40-60%',
        'Improves focus and concentration in work tasks',
        'Enhances emotional regulation and resilience',
        'Promotes better sleep quality and recovery',
        'Increases self-awareness and mindfulness',
        'Lowers blood pressure and heart rate',
        'Strengthens immune system function'
      ],
      tips: [
        'Start with just 5 minutes and gradually increase duration',
        'Be patient with yourself - meditation is a learned skill',
        'Try different times of day to find what works best for you',
        'Use guided meditations if you\'re new to practice',
        'Don\'t worry about "clearing your mind" - just observe thoughts',
        'Practice consistently rather than for long periods occasionally',
        'Create a dedicated meditation space in your home or office'
      ],
      scientificEvidence: [
        'Harvard study shows 8 weeks of mindfulness reduces stress by 35%',
        'Stanford research links meditation to improved cognitive function',
        'NIH study demonstrates reduced anxiety in workplace settings',
        'Meta-analysis of 47 studies shows consistent stress reduction'
      ]
    },
    author: 'Dr. Sarah Johnson',
    authorCredentials: 'Licensed Clinical Psychologist, Mindfulness Expert',
    authorBio: 'Dr. Johnson has over 15 years of experience in clinical psychology and mindfulness-based interventions. She has published over 50 peer-reviewed articles and has helped thousands of individuals reduce stress and improve mental well-being.',
    publishedDate: '2024-01-15',
    lastUpdated: '2024-01-20',
    rating: 4.7,
    reviewCount: 124,
    completionRate: 78,
    estimatedTime: '15 minutes',
    prerequisites: 'None - suitable for all experience levels',
    materials: ['Quiet space', 'Comfortable seating', 'Timer (optional)', 'Meditation cushion (optional)'],
    mediaType: 'video', // 'video', 'audio', 'interactive', 'document'
    mediaUrl: 'https://example.com/meditation-video.mp4',
    thumbnail: 'https://example.com/meditation-thumbnail.jpg',
    transcript: 'Welcome to mindfulness meditation...',
    accessibility: {
      hasSubtitles: true,
      hasAudioDescription: false,
      hasTranscript: true,
      keyboardNavigable: true,
      screenReaderCompatible: true,
    },
    relatedResources: [
      { id: '2', title: 'Breathing Exercises for Anxiety', category: 'stress-management', duration: 10 },
      { id: '3', title: 'Progressive Muscle Relaxation', category: 'relaxation', duration: 20 },
      { id: '4', title: 'Mindful Walking Practice', category: 'mindfulness', duration: 15 },
      { id: '5', title: 'Body Scan Meditation', category: 'mindfulness', duration: 25 },
    ],
    userProgress: {
      completed: false,
      timeSpent: 0,
      lastPosition: 0,
      bookmarks: [],
      notes: [],
    },
    analytics: {
      views: 1247,
      completions: 973,
      averageRating: 4.7,
      engagementScore: 8.5,
      popularTimes: ['9:00 AM', '12:00 PM', '6:00 PM'],
    }
  };

  const isFavorite = favorites.includes(resource.id);
  const isBookmarked = false; // Would come from user state

  useEffect(() => {
    // Record view interaction
    if (resourceId) {
      dispatch(recordInteraction({
        resourceId,
        interactionType: 'view',
      }));
    }

    // Simulate loading
    setIsLoading(true);
    setTimeout(() => setIsLoading(false), 1000);

    // Cleanup interval on unmount
    return () => {
      if (progressIntervalRef.current) {
        clearInterval(progressIntervalRef.current);
      }
    };
  }, [resourceId, dispatch]);

  // Track user engagement
  useEffect(() => {
    const engagementInterval = setInterval(() => {
      if (isPlaying) {
        setUserEngagement(prev => ({
          ...prev,
          timeSpent: prev.timeSpent + 1,
          interactions: prev.interactions + 1,
        }));
      }
    }, 1000);

    return () => clearInterval(engagementInterval);
  }, [isPlaying]);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handlePlayPause = () => {
    setIsPlaying(!isPlaying);
    if (!isPlaying) {
      // Start progress simulation
      progressIntervalRef.current = setInterval(() => {
        setProgress(prev => {
          if (prev >= 100) {
            if (progressIntervalRef.current) {
              clearInterval(progressIntervalRef.current);
            }
            setIsPlaying(false);
            // Mark as completed
            dispatch(addNotification({
              type: 'success',
              title: 'Resource Completed!',
              message: 'Great job! You\'ve completed this mindfulness resource.',
            }));
            return 100;
          }
          return prev + (100 / (duration / 60)); // Progress based on duration
        });
      }, 1000);
    } else {
      // Pause
      if (progressIntervalRef.current) {
        clearInterval(progressIntervalRef.current);
      }
    }
  };

  const handleStop = () => {
    setIsPlaying(false);
    setProgress(0);
    setCurrentTime(0);
    if (progressIntervalRef.current) {
      clearInterval(progressIntervalRef.current);
    }
  };

  const handleSeek = (event: Event, newValue: number | number[]) => {
    const seekTime = newValue as number;
    setProgress(seekTime);
    setCurrentTime((seekTime / 100) * duration);
  };

  const handleVolumeChange = (event: Event, newValue: number | number[]) => {
    const newVolume = newValue as number;
    setVolume(newVolume);
    setIsMuted(newVolume === 0);
  };

  const handleSpeedChange = (speed: number) => {
    setPlaybackSpeed(speed);
    dispatch(addNotification({
      type: 'info',
      title: 'Playback Speed Changed',
      message: `Speed set to ${speed}x`,
    }));
  };

  const handleFavorite = () => {
    dispatch(recordInteraction({
      resourceId: resource.id,
      interactionType: 'like',
    }));
    dispatch(addNotification({
      type: 'success',
      title: isFavorite ? 'Removed from Favorites' : 'Added to Favorites',
      message: isFavorite ? 'Resource removed from your favorites.' : 'Resource added to your favorites!',
    }));
  };

  const handleBookmark = () => {
    dispatch(addNotification({
      type: 'success',
      title: 'Bookmarked',
      message: 'Resource added to your bookmarks.',
    }));
  };

  const handleShare = () => {
    setShowShareDialog(true);
  };

  const handleRating = (newRating: number) => {
    setRating(newRating);
    dispatch(addNotification({
      type: 'success',
      title: 'Rating Submitted',
      message: 'Thank you for your feedback!',
    }));
  };

  const handleComment = () => {
    if (comment.trim()) {
      dispatch(addNotification({
        type: 'success',
        title: 'Comment Submitted',
        message: 'Your comment has been posted.',
      }));
      setComment('');
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner': return 'success';
      case 'intermediate': return 'warning';
      case 'advanced': return 'error';
      default: return 'default';
    }
  };

  const getCategoryIcon = (category: string) => {
    const iconMap: { [key: string]: React.ReactNode } = {
      'mindfulness': <Psychology />,
      'stress-management': <Spa />,
      'relaxation': <SelfImprovement />,
      'exercise': <FitnessCenter />,
      'nutrition': <Restaurant />,
      'education': <School />,
      'work-life-balance': <Work />,
      'relationships': <Family />,
      'pet-therapy': <Pets />,
      'nature': <Nature />,
      'music': <MusicNote />,
      'video': <VideoLibrary />,
      'article': <Article />,
      'podcast': <Podcasts />,
      'webinar': <Web />,
    };
    return iconMap[category] || <Category />;
  };

  const getMediaTypeIcon = (mediaType: string) => {
    switch (mediaType) {
      case 'video': return <VideoLibrary />;
      case 'audio': return <MusicNote />;
      case 'interactive': return <Web />;
      case 'document': return <Article />;
      default: return <Article />;
    }
  };

  if (isLoading) {
    return (
      <Box sx={{ p: 3, maxWidth: 1200, mx: 'auto' }}>
        <Skeleton variant="rectangular" height={60} sx={{ mb: 3 }} />
        <Grid container spacing={3}>
          <Grid item xs={12} lg={8}>
            <Skeleton variant="rectangular" height={400} sx={{ mb: 3 }} />
            <Skeleton variant="rectangular" height={300} />
          </Grid>
          <Grid item xs={12} lg={4}>
            <Skeleton variant="rectangular" height={200} sx={{ mb: 3 }} />
            <Skeleton variant="rectangular" height={200} sx={{ mb: 3 }} />
            <Skeleton variant="rectangular" height={200} />
          </Grid>
        </Grid>
      </Box>
    );
  }

  return (
    <Box sx={{ p: { xs: 2, md: 3 }, maxWidth: 1200, mx: 'auto' }}>
      {/* Header */}
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
        <IconButton 
          onClick={() => navigate('/resources')} 
          sx={{ mr: 2 }}
          aria-label="Go back to resources"
        >
          <ArrowBack />
        </IconButton>
        <Typography 
          variant="h4" 
          sx={{ 
            fontWeight: 600, 
            color: 'primary.main',
            fontSize: { xs: '1.5rem', md: '2.125rem' }
          }}
        >
          {resource.title}
        </Typography>
      </Box>

      <Grid container spacing={3}>
        {/* Main Content */}
        <Grid item xs={12} lg={8}>
          {/* Enhanced Resource Header */}
          <Card sx={{ mb: 3, position: 'relative', overflow: 'visible' }}>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                <Box sx={{ flex: 1 }}>
                  <Typography 
                    variant="h5" 
                    sx={{ 
                      fontWeight: 600, 
                      mb: 1,
                      fontSize: { xs: '1.25rem', md: '1.5rem' }
                    }}
                  >
                    {resource.title}
                  </Typography>
                  <Typography 
                    variant="body1" 
                    color="text.secondary" 
                    sx={{ mb: 2, lineHeight: 1.6 }}
                  >
                    {resource.description}
                  </Typography>
                  
                  <Box sx={{ display: 'flex', gap: 1, mb: 2, flexWrap: 'wrap' }}>
                    <Chip
                      label={resource.difficultyLevel}
                      color={getDifficultyColor(resource.difficultyLevel) as any}
                      size="small"
                      icon={getCategoryIcon(resource.category)}
                    />
                    <Chip
                      icon={<AccessTime />}
                      label={`${resource.durationMinutes} min`}
                      size="small"
                      variant="outlined"
                    />
                    <Chip
                      icon={<Person />}
                      label={resource.author}
                      size="small"
                      variant="outlined"
                    />
                    <Chip
                      icon={getMediaTypeIcon(resource.mediaType)}
                      label={resource.mediaType}
                      size="small"
                      variant="outlined"
                    />
                  </Box>
                </Box>
                
                <Box sx={{ display: 'flex', gap: 1, flexShrink: 0 }}>
                  <Tooltip title={isFavorite ? "Remove from favorites" : "Add to favorites"}>
                    <IconButton onClick={handleFavorite} color={isFavorite ? "error" : "default"}>
                      {isFavorite ? <Favorite /> : <FavoriteBorder />}
                    </IconButton>
                  </Tooltip>
                  <Tooltip title={isBookmarked ? "Remove bookmark" : "Add bookmark"}>
                    <IconButton onClick={handleBookmark} color={isBookmarked ? "primary" : "default"}>
                      {isBookmarked ? <Bookmark /> : <BookmarkBorder />}
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="Share resource">
                    <IconButton onClick={handleShare}>
                      <Share />
                    </IconButton>
                  </Tooltip>
                </Box>
              </Box>

              {/* Enhanced Progress Bar */}
              <Box sx={{ mb: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2" color="text.secondary">
                    Progress
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {Math.round(progress)}%
                  </Typography>
                </Box>
                <LinearProgress
                  variant="determinate"
                  value={progress}
                  sx={{ 
                    height: 8, 
                    borderRadius: 4,
                    backgroundColor: 'grey.200',
                    '& .MuiLinearProgress-bar': {
                      borderRadius: 4,
                      background: 'linear-gradient(90deg, #4CAF50 0%, #8BC34A 100%)',
                    }
                  }}
                />
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 0.5 }}>
                  <Typography variant="caption" color="text.secondary">
                    {formatTime(currentTime)}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    {formatTime(duration)}
                  </Typography>
                </Box>
              </Box>

              {/* Enhanced Action Buttons */}
              <Box sx={{ display: 'flex', gap: 2, mb: 2, flexWrap: 'wrap' }}>
                <Button
                  variant="contained"
                  startIcon={isPlaying ? <Pause /> : <PlayArrow />}
                  onClick={handlePlayPause}
                  sx={{ 
                    minWidth: 120,
                    background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)',
                    boxShadow: '0 3px 5px 2px rgba(33, 203, 243, .3)',
                  }}
                >
                  {isPlaying ? 'Pause' : 'Start'}
                </Button>
                <Button
                  variant="outlined"
                  startIcon={<Stop />}
                  onClick={handleStop}
                >
                  Stop
                </Button>
                <Button
                  variant="outlined"
                  startIcon={<Download />}
                >
                  Download
                </Button>
                {resource.accessibility.hasSubtitles && (
                  <Button
                    variant="outlined"
                    startIcon={showSubtitles ? <Visibility /> : <VisibilityOff />}
                    onClick={() => setShowSubtitles(!showSubtitles)}
                  >
                    {showSubtitles ? 'Hide' : 'Show'} Subtitles
                  </Button>
                )}
              </Box>

              {/* Enhanced Rating Display */}
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, flexWrap: 'wrap' }}>
                <Rating
                  value={resource.rating}
                  readOnly
                  precision={0.1}
                  size="small"
                />
                <Typography variant="body2" color="text.secondary">
                  {resource.rating} ({resource.reviewCount} reviews)
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  • {resource.completionRate}% completion rate
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  • {resource.analytics.views} views
                </Typography>
              </Box>
            </CardContent>
          </Card>

          {/* Enhanced Content Tabs */}
          <Card>
            <CardContent>
              <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}>
                <Tabs 
                  value={tabValue} 
                  onChange={handleTabChange} 
                  aria-label="resource content tabs"
                  variant={isMobile ? "scrollable" : "fullWidth"}
                  scrollButtons={isMobile ? "auto" : false}
                >
                  <Tab label="Overview" />
                  <Tab label="Instructions" />
                  <Tab label="Benefits" />
                  <Tab label="Tips" />
                  <Tab label="Evidence" />
                </Tabs>
              </Box>

              {/* Overview Tab */}
              <TabPanel value={tabValue} index={0}>
                <Typography variant="body1" sx={{ mb: 3, lineHeight: 1.7 }}>
                  {resource.content.overview}
                </Typography>
                
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 1 }}>
                      Estimated Time
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {resource.estimatedTime}
                    </Typography>
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 1 }}>
                      Prerequisites
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {resource.prerequisites}
                    </Typography>
                  </Grid>
                  <Grid item xs={12}>
                    <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 1 }}>
                      Materials Needed
                    </Typography>
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                      {resource.materials.map((material, index) => (
                        <Chip
                          key={index}
                          label={material}
                          size="small"
                          variant="outlined"
                          icon={<CheckCircle />}
                        />
                      ))}
                    </Box>
                  </Grid>
                  <Grid item xs={12}>
                    <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 1 }}>
                      Accessibility Features
                    </Typography>
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                      {resource.accessibility.hasSubtitles && (
                        <Chip label="Subtitles" size="small" variant="outlined" />
                      )}
                      {resource.accessibility.hasTranscript && (
                        <Chip label="Transcript" size="small" variant="outlined" />
                      )}
                      {resource.accessibility.keyboardNavigable && (
                        <Chip label="Keyboard Navigation" size="small" variant="outlined" />
                      )}
                      {resource.accessibility.screenReaderCompatible && (
                        <Chip label="Screen Reader Compatible" size="small" variant="outlined" />
                      )}
                    </Box>
                  </Grid>
                </Grid>
              </TabPanel>

              {/* Instructions Tab */}
              <TabPanel value={tabValue} index={1}>
                <List>
                  {resource.content.instructions.map((instruction, index) => (
                    <ListItem key={index} sx={{ py: 1.5 }}>
                      <ListItemIcon>
                        <Avatar 
                          sx={{ 
                            bgcolor: 'primary.main', 
                            width: 32, 
                            height: 32,
                            fontSize: '0.875rem',
                            fontWeight: 600
                          }}
                        >
                          {index + 1}
                        </Avatar>
                      </ListItemIcon>
                      <ListItemText 
                        primary={instruction} 
                        sx={{ 
                          '& .MuiListItemText-primary': {
                            lineHeight: 1.6,
                            fontSize: '1rem'
                          }
                        }}
                      />
                    </ListItem>
                  ))}
                </List>
              </TabPanel>

              {/* Benefits Tab */}
              <TabPanel value={tabValue} index={2}>
                <List>
                  {resource.content.benefits.map((benefit, index) => (
                    <ListItem key={index} sx={{ py: 1.5 }}>
                      <ListItemIcon>
                        <CheckCircle color="success" sx={{ fontSize: 28 }} />
                      </ListItemIcon>
                      <ListItemText 
                        primary={benefit} 
                        sx={{ 
                          '& .MuiListItemText-primary': {
                            lineHeight: 1.6,
                            fontSize: '1rem'
                          }
                        }}
                      />
                    </ListItem>
                  ))}
                </List>
              </TabPanel>

              {/* Tips Tab */}
              <TabPanel value={tabValue} index={3}>
                <List>
                  {resource.content.tips.map((tip, index) => (
                    <ListItem key={index} sx={{ py: 1.5 }}>
                      <ListItemIcon>
                        <Star color="primary" sx={{ fontSize: 28 }} />
                      </ListItemIcon>
                      <ListItemText 
                        primary={tip} 
                        sx={{ 
                          '& .MuiListItemText-primary': {
                            lineHeight: 1.6,
                            fontSize: '1rem'
                          }
                        }}
                      />
                    </ListItem>
                  ))}
                </List>
              </TabPanel>

              {/* Scientific Evidence Tab */}
              <TabPanel value={tabValue} index={4}>
                <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                  Scientific Evidence & Research
                </Typography>
                <List>
                  {resource.content.scientificEvidence.map((evidence, index) => (
                    <ListItem key={index} sx={{ py: 1.5 }}>
                      <ListItemIcon>
                        <School color="info" sx={{ fontSize: 28 }} />
                      </ListItemIcon>
                      <ListItemText 
                        primary={evidence} 
                        sx={{ 
                          '& .MuiListItemText-primary': {
                            lineHeight: 1.6,
                            fontSize: '1rem'
                          }
                        }}
                      />
                    </ListItem>
                  ))}
                </List>
              </TabPanel>
            </CardContent>
          </Card>
        </Grid>

        {/* Enhanced Sidebar */}
        <Grid item xs={12} lg={4}>
          {/* Enhanced Author Info */}
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                About the Author
              </Typography>
              
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Avatar 
                  sx={{ 
                    mr: 2, 
                    bgcolor: 'primary.main',
                    width: 56,
                    height: 56,
                    fontSize: '1.25rem'
                  }}
                >
                  {resource.author.split(' ').map(n => n[0]).join('')}
                </Avatar>
                <Box>
                  <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                    {resource.author}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {resource.authorCredentials}
                  </Typography>
                </Box>
              </Box>
              
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2, lineHeight: 1.6 }}>
                {resource.authorBio}
              </Typography>
              
              <Divider sx={{ my: 2 }} />
              
              <Typography variant="body2" color="text.secondary">
                Published: {new Date(resource.publishedDate).toLocaleDateString()}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Updated: {new Date(resource.lastUpdated).toLocaleDateString()}
              </Typography>
            </CardContent>
          </Card>

          {/* Enhanced Related Resources */}
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                Related Resources
              </Typography>
              
              <List dense>
                {resource.relatedResources.map((related) => (
                  <ListItem
                    key={related.id}
                    button
                    onClick={() => navigate(`/resources/${related.id}`)}
                    sx={{ 
                      borderRadius: 1, 
                      mb: 1,
                      '&:hover': {
                        backgroundColor: 'action.hover',
                      }
                    }}
                  >
                    <ListItemIcon>
                      {getCategoryIcon(related.category)}
                    </ListItemIcon>
                    <ListItemText
                      primary={related.title}
                      secondary={`${related.category.replace('-', ' ')} • ${related.duration} min`}
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>

          {/* Enhanced Feedback */}
          <Card>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                Rate This Resource
              </Typography>
              
              <Rating
                value={rating}
                onChange={(_, newValue) => handleRating(newValue || 0)}
                size="large"
                sx={{ mb: 2 }}
              />
              
              <TextField
                fullWidth
                multiline
                rows={3}
                placeholder="Share your experience with this resource..."
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                sx={{ mb: 2 }}
                variant="outlined"
              />
              
              <Button
                variant="contained"
                onClick={handleComment}
                disabled={!comment.trim()}
                fullWidth
                sx={{
                  background: 'linear-gradient(45deg, #4CAF50 30%, #8BC34A 90%)',
                  boxShadow: '0 3px 5px 2px rgba(76, 175, 80, .3)',
                }}
              >
                Submit Feedback
              </Button>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Enhanced Share Dialog */}
      <Dialog
        open={showShareDialog}
        onClose={() => setShowShareDialog(false)}
        maxWidth="sm"
        fullWidth
        TransitionComponent={Zoom}
      >
        <DialogTitle>
          Share Resource
          <IconButton
            aria-label="close"
            onClick={() => setShowShareDialog(false)}
            sx={{
              position: 'absolute',
              right: 8,
              top: 8,
              color: (theme) => theme.palette.grey[500],
            }}
          >
            <Close />
          </IconButton>
        </DialogTitle>
        <DialogContent>
          <Typography variant="body2" sx={{ mb: 3 }}>
            Share this resource with your colleagues or on social media.
          </Typography>
          
          <Grid container spacing={2}>
            <Grid item xs={6}>
              <Button
                variant="outlined"
                fullWidth
                startIcon={<ContentCopy />}
                onClick={() => {
                  navigator.clipboard.writeText(window.location.href);
                  dispatch(addNotification({
                    type: 'success',
                    title: 'Link Copied',
                    message: 'Resource link copied to clipboard.',
                  }));
                  setShowShareDialog(false);
                }}
              >
                Copy Link
              </Button>
            </Grid>
            <Grid item xs={6}>
              <Button
                variant="outlined"
                fullWidth
                startIcon={<Email />}
                onClick={() => {
                  const subject = encodeURIComponent(`Check out this resource: ${resource.title}`);
                  const body = encodeURIComponent(`I found this great wellness resource that might help you: ${resource.title}\n\n${resource.description}\n\n${window.location.href}`);
                  window.open(`mailto:?subject=${subject}&body=${body}`);
                  setShowShareDialog(false);
                }}
              >
                Email
              </Button>
            </Grid>
            <Grid item xs={6}>
              <Button
                variant="outlined"
                fullWidth
                startIcon={<LinkedIn />}
                onClick={() => {
                  const url = encodeURIComponent(window.location.href);
                  const title = encodeURIComponent(resource.title);
                  const summary = encodeURIComponent(resource.description);
                  window.open(`https://www.linkedin.com/sharing/share-offsite/?url=${url}&title=${title}&summary=${summary}`);
                  setShowShareDialog(false);
                }}
              >
                LinkedIn
              </Button>
            </Grid>
            <Grid item xs={6}>
              <Button
                variant="outlined"
                fullWidth
                startIcon={<Twitter />}
                onClick={() => {
                  const text = encodeURIComponent(`Check out this wellness resource: ${resource.title}`);
                  const url = encodeURIComponent(window.location.href);
                  window.open(`https://twitter.com/intent/tweet?text=${text}&url=${url}`);
                  setShowShareDialog(false);
                }}
              >
                Twitter
              </Button>
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowShareDialog(false)}>Cancel</Button>
        </DialogActions>
      </Dialog>

      {/* Speed Dial for Quick Actions */}
      <SpeedDial
        ariaLabel="Quick actions"
        sx={{ position: 'fixed', bottom: 16, right: 16 }}
        icon={<SpeedDialIcon />}
      >
        <SpeedDialAction
          icon={<Accessibility />}
          tooltipTitle="Accessibility"
          onClick={() => setAccessibilityMode(!accessibilityMode)}
        />
        <SpeedDialAction
          icon={<Speed />}
          tooltipTitle="Playback Speed"
          onClick={() => handleSpeedChange(playbackSpeed === 1 ? 1.5 : 1)}
        />
        <SpeedDialAction
          icon={<VolumeUp />}
          tooltipTitle="Volume"
          onClick={() => setIsMuted(!isMuted)}
        />
        <SpeedDialAction
          icon={<Fullscreen />}
          tooltipTitle="Fullscreen"
          onClick={() => setIsFullscreen(!isFullscreen)}
        />
      </SpeedDial>

      {/* Accessibility Mode Overlay */}
      {accessibilityMode && (
        <Box
          sx={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(0, 0, 0, 0.1)',
            zIndex: 1000,
            pointerEvents: 'none',
          }}
        />
      )}
    </Box>
  );
};

export default ResourceDetail;
