import React, { useState, useEffect } from 'react';
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
  const { resourceId } = useParams<{ resourceId: string }>();
  const { resources, favorites } = useSelector((state: RootState) => state.resources);
  
  const [tabValue, setTabValue] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [progress, setProgress] = useState(0);
  const [rating, setRating] = useState(0);
  const [comment, setComment] = useState('');
  const [showShareDialog, setShowShareDialog] = useState(false);
  const [showFeedbackDialog, setShowFeedbackDialog] = useState(false);

  // Mock resource data (in real app, this would come from API)
  const resource = {
    id: resourceId || '1',
    title: 'Mindfulness Meditation for Stress Relief',
    description: 'A comprehensive guide to mindfulness meditation techniques designed to help reduce stress and improve mental well-being in the workplace.',
    category: 'mindfulness',
    difficultyLevel: 'beginner',
    durationMinutes: 15,
    tags: ['meditation', 'stress-relief', 'mindfulness', 'beginner-friendly'],
    content: {
      overview: 'This resource provides step-by-step guidance for practicing mindfulness meditation, specifically tailored for workplace stress management.',
      instructions: [
        'Find a quiet, comfortable space',
        'Sit in a relaxed but alert posture',
        'Close your eyes and take deep breaths',
        'Focus on your breath and let thoughts pass by',
        'Practice for 10-15 minutes daily'
      ],
      benefits: [
        'Reduces stress and anxiety',
        'Improves focus and concentration',
        'Enhances emotional regulation',
        'Promotes better sleep quality',
        'Increases self-awareness'
      ],
      tips: [
        'Start with just 5 minutes and gradually increase',
        'Be patient with yourself - meditation is a skill',
        'Try different times of day to find what works best',
        'Use guided meditations if you\'re new to practice',
        'Don\'t worry about "clearing your mind" - just observe thoughts'
      ]
    },
    author: 'Dr. Sarah Johnson',
    authorCredentials: 'Licensed Clinical Psychologist, Mindfulness Expert',
    publishedDate: '2024-01-15',
    lastUpdated: '2024-01-20',
    rating: 4.7,
    reviewCount: 124,
    completionRate: 78,
    estimatedTime: '15 minutes',
    prerequisites: 'None',
    materials: ['Quiet space', 'Comfortable seating', 'Timer (optional)'],
    relatedResources: [
      { id: '2', title: 'Breathing Exercises for Anxiety', category: 'stress-management' },
      { id: '3', title: 'Progressive Muscle Relaxation', category: 'relaxation' },
      { id: '4', title: 'Mindful Walking Practice', category: 'mindfulness' }
    ]
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
  }, [resourceId, dispatch]);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handlePlayPause = () => {
    setIsPlaying(!isPlaying);
    if (!isPlaying) {
      // Start progress simulation
      const interval = setInterval(() => {
        setProgress(prev => {
          if (prev >= 100) {
            clearInterval(interval);
            setIsPlaying(false);
            return 100;
          }
          return prev + 1;
        });
      }, 1000);
    }
  };

  const handleStop = () => {
    setIsPlaying(false);
    setProgress(0);
  };

  const handleFavorite = () => {
    dispatch(recordInteraction({
      resourceId: resource.id,
      interactionType: 'like',
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

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner': return 'success';
      case 'intermediate': return 'warning';
      case 'advanced': return 'error';
      default: return 'default';
    }
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'mindfulness': return '🧘';
      case 'stress-management': return '😌';
      case 'relaxation': return '🌿';
      case 'exercise': return '💪';
      case 'nutrition': return '🥗';
      default: return '📚';
    }
  };

  return (
    <Box sx={{ p: 3, maxWidth: 1200, mx: 'auto' }}>
      {/* Header */}
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
        <IconButton onClick={() => navigate('/resources')} sx={{ mr: 2 }}>
          <ArrowBack />
        </IconButton>
        <Typography variant="h4" sx={{ fontWeight: 600, color: 'primary.main' }}>
          {resource.title}
        </Typography>
      </Box>

      <Grid container spacing={3}>
        {/* Main Content */}
        <Grid item xs={12} lg={8}>
          {/* Resource Header */}
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                <Box>
                  <Typography variant="h5" sx={{ fontWeight: 600, mb: 1 }}>
                    {resource.title}
                  </Typography>
                  <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
                    {resource.description}
                  </Typography>
                  
                  <Box sx={{ display: 'flex', gap: 1, mb: 2, flexWrap: 'wrap' }}>
                    <Chip
                      label={resource.difficultyLevel}
                      color={getDifficultyColor(resource.difficultyLevel) as any}
                      size="small"
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
                  </Box>
                </Box>
                
                <Box sx={{ display: 'flex', gap: 1 }}>
                  <IconButton onClick={handleFavorite}>
                    {isFavorite ? <Favorite color="error" /> : <FavoriteBorder />}
                  </IconButton>
                  <IconButton onClick={handleBookmark}>
                    {isBookmarked ? <Bookmark color="primary" /> : <BookmarkBorder />}
                  </IconButton>
                  <IconButton onClick={handleShare}>
                    <Share />
                  </IconButton>
                </Box>
              </Box>

              {/* Progress Bar */}
              <Box sx={{ mb: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2" color="text.secondary">
                    Progress
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {progress}%
                  </Typography>
                </Box>
                <LinearProgress
                  variant="determinate"
                  value={progress}
                  sx={{ height: 8, borderRadius: 4 }}
                />
              </Box>

              {/* Action Buttons */}
              <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
                <Button
                  variant="contained"
                  startIcon={isPlaying ? <Pause /> : <PlayArrow />}
                  onClick={handlePlayPause}
                  sx={{ minWidth: 120 }}
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
              </Box>

              {/* Rating */}
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
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
              </Box>
            </CardContent>
          </Card>

          {/* Content Tabs */}
          <Card>
            <CardContent>
              <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}>
                <Tabs value={tabValue} onChange={handleTabChange} aria-label="resource content tabs">
                  <Tab label="Overview" />
                  <Tab label="Instructions" />
                  <Tab label="Benefits" />
                  <Tab label="Tips" />
                </Tabs>
              </Box>

              {/* Overview Tab */}
              <TabPanel value={tabValue} index={0}>
                <Typography variant="body1" sx={{ mb: 3 }}>
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
                        />
                      ))}
                    </Box>
                  </Grid>
                </Grid>
              </TabPanel>

              {/* Instructions Tab */}
              <TabPanel value={tabValue} index={1}>
                <List>
                  {resource.content.instructions.map((instruction, index) => (
                    <ListItem key={index}>
                      <ListItemIcon>
                        <Avatar sx={{ bgcolor: 'primary.main', width: 32, height: 32 }}>
                          {index + 1}
                        </Avatar>
                      </ListItemIcon>
                      <ListItemText primary={instruction} />
                    </ListItem>
                  ))}
                </List>
              </TabPanel>

              {/* Benefits Tab */}
              <TabPanel value={tabValue} index={2}>
                <List>
                  {resource.content.benefits.map((benefit, index) => (
                    <ListItem key={index}>
                      <ListItemIcon>
                        <CheckCircle color="success" />
                      </ListItemIcon>
                      <ListItemText primary={benefit} />
                    </ListItem>
                  ))}
                </List>
              </TabPanel>

              {/* Tips Tab */}
              <TabPanel value={tabValue} index={3}>
                <List>
                  {resource.content.tips.map((tip, index) => (
                    <ListItem key={index}>
                      <ListItemIcon>
                        <Star color="primary" />
                      </ListItemIcon>
                      <ListItemText primary={tip} />
                    </ListItem>
                  ))}
                </List>
              </TabPanel>
            </CardContent>
          </Card>
        </Grid>

        {/* Sidebar */}
        <Grid item xs={12} lg={4}>
          {/* Author Info */}
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                About the Author
              </Typography>
              
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Avatar sx={{ mr: 2, bgcolor: 'primary.main' }}>
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
              
              <Typography variant="body2" color="text.secondary">
                Published: {new Date(resource.publishedDate).toLocaleDateString()}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Updated: {new Date(resource.lastUpdated).toLocaleDateString()}
              </Typography>
            </CardContent>
          </Card>

          {/* Related Resources */}
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
                  >
                    <ListItemIcon>
                      <span style={{ fontSize: '1.5rem' }}>
                        {getCategoryIcon(related.category)}
                      </span>
                    </ListItemIcon>
                    <ListItemText
                      primary={related.title}
                      secondary={related.category.replace('-', ' ')}
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>

          {/* Feedback */}
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
              />
              
              <Button
                variant="contained"
                onClick={handleComment}
                disabled={!comment.trim()}
                fullWidth
              >
                Submit Feedback
              </Button>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Share Dialog */}
      <Dialog
        open={showShareDialog}
        onClose={() => setShowShareDialog(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Share Resource</DialogTitle>
        <DialogContent>
          <Typography variant="body2" sx={{ mb: 2 }}>
            Share this resource with your colleagues or on social media.
          </Typography>
          
          <Grid container spacing={2}>
            <Grid item xs={6}>
              <Button
                variant="outlined"
                fullWidth
                onClick={() => {
                  navigator.share?.({
                    title: resource.title,
                    text: resource.description,
                    url: window.location.href,
                  });
                  setShowShareDialog(false);
                }}
              >
                Share Link
              </Button>
            </Grid>
            <Grid item xs={6}>
              <Button
                variant="outlined"
                fullWidth
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
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowShareDialog(false)}>Cancel</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default ResourceDetail;
