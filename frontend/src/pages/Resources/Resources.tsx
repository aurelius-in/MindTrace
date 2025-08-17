import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  TextField,
  InputAdornment,
  Chip,
  Button,
  Avatar,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Divider,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Rating,
  IconButton,
  Tooltip,
  Alert,
  Tabs,
  Tab,
  Paper,
  LinearProgress,
} from '@mui/material';
import {
  Search,
  FilterList,
  Favorite,
  FavoriteBorder,
  Bookmark,
  BookmarkBorder,
  PlayArrow,
  Schedule,
  Star,
  Psychology,
  FitnessCenter,
  LocalHospital,
  School,
  EmojiEmotions,
  Work,
  Family,
  TrendingUp,
  AccessTime,
  Person,
  Category,
} from '@mui/icons-material';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';

import { RootState } from '../../store';
import { fetchResources, recordInteraction } from '../../store/slices/resourcesSlice';
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
    id={`resources-tabpanel-${index}`}
    aria-labelledby={`resources-tab-${index}`}
    {...other}
  >
    {value === index && <Box sx={{ pt: 3 }}>{children}</Box>}
  </div>
);

const Resources: React.FC = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { resources, favorites, recentlyViewed, isLoading } = useSelector((state: RootState) => state.resources);
  
  const [tabValue, setTabValue] = useState(0);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedDifficulty, setSelectedDifficulty] = useState('all');
  const [selectedDuration, setSelectedDuration] = useState('all');

  const categories = [
    { value: 'all', label: 'All Categories', icon: <Category /> },
    { value: 'stress-management', label: 'Stress Management', icon: <Psychology /> },
    { value: 'physical-wellness', label: 'Physical Wellness', icon: <FitnessCenter /> },
    { value: 'mental-health', label: 'Mental Health', icon: <LocalHospital /> },
    { value: 'work-life-balance', label: 'Work-Life Balance', icon: <Work /> },
    { value: 'relationships', label: 'Relationships', icon: <Family /> },
    { value: 'mindfulness', label: 'Mindfulness', icon: <EmojiEmotions /> },
    { value: 'education', label: 'Education', icon: <School /> },
  ];

  const difficulties = [
    { value: 'all', label: 'All Levels' },
    { value: 'beginner', label: 'Beginner' },
    { value: 'intermediate', label: 'Intermediate' },
    { value: 'advanced', label: 'Advanced' },
  ];

  const durations = [
    { value: 'all', label: 'Any Duration' },
    { value: '0-15', label: '0-15 minutes' },
    { value: '15-30', label: '15-30 minutes' },
    { value: '30-60', label: '30-60 minutes' },
    { value: '60+', label: '60+ minutes' },
  ];

  useEffect(() => {
    loadResources();
  }, []);

  const loadResources = async () => {
    try {
      await dispatch(fetchResources());
    } catch (error) {
      dispatch(addNotification({
        type: 'error',
        title: 'Failed to Load Resources',
        message: 'Unable to load wellness resources. Please try again.',
      }));
    }
  };

  const getFilteredResources = () => {
    return resources.filter(resource => {
      const matchesSearch = resource.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                           resource.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
                           resource.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()));
      
      const matchesCategory = selectedCategory === 'all' || resource.category === selectedCategory;
      const matchesDifficulty = selectedDifficulty === 'all' || resource.difficultyLevel === selectedDifficulty;
      
      let matchesDuration = true;
      if (selectedDuration !== 'all' && resource.durationMinutes) {
        const duration = resource.durationMinutes;
        switch (selectedDuration) {
          case '0-15':
            matchesDuration = duration <= 15;
            break;
          case '15-30':
            matchesDuration = duration > 15 && duration <= 30;
            break;
          case '30-60':
            matchesDuration = duration > 30 && duration <= 60;
            break;
          case '60+':
            matchesDuration = duration > 60;
            break;
        }
      }
      
      return matchesSearch && matchesCategory && matchesDifficulty && matchesDuration;
    });
  };

  const getFavorites = () => {
    return resources.filter(resource => favorites.includes(resource.id));
  };

  const getRecentlyViewed = () => {
    return recentlyViewed.map(id => resources.find(resource => resource.id === id)).filter(Boolean);
  };

  const getRecommendedResources = () => {
    // In a real app, this would be based on user preferences and AI recommendations
    return resources.filter(resource => resource.tags.includes('recommended')).slice(0, 6);
  };

  const handleResourceClick = async (resourceId: string) => {
    try {
      await dispatch(recordInteraction({
        resourceId,
        interactionType: 'view',
      }));
      navigate(`/resources/${resourceId}`);
    } catch (error) {
      console.error('Failed to record interaction:', error);
    }
  };

  const handleFavoriteToggle = async (resourceId: string) => {
    try {
      await dispatch(recordInteraction({
        resourceId,
        interactionType: 'like',
      }));
      
      // Toggle favorite in local state (in real app, this would be handled by the backend)
      dispatch(addNotification({
        type: 'success',
        title: 'Favorite Updated',
        message: 'Resource added to your favorites.',
      }));
    } catch (error) {
      dispatch(addNotification({
        type: 'error',
        title: 'Failed to Update Favorite',
        message: 'Unable to update favorite status.',
      }));
    }
  };

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const getCategoryIcon = (category: string) => {
    const categoryData = categories.find(cat => cat.value === category);
    return categoryData?.icon || <Category />;
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner': return 'success';
      case 'intermediate': return 'warning';
      case 'advanced': return 'error';
      default: return 'default';
    }
  };

  const getDurationLabel = (minutes?: number) => {
    if (!minutes) return 'Variable';
    if (minutes < 60) return `${minutes} min`;
    const hours = Math.floor(minutes / 60);
    const remainingMinutes = minutes % 60;
    return remainingMinutes > 0 ? `${hours}h ${remainingMinutes}m` : `${hours}h`;
  };

  const filteredResources = getFilteredResources();
  const favoriteResources = getFavorites();
  const recentlyViewedResources = getRecentlyViewed();
  const recommendedResources = getRecommendedResources();

  if (isLoading) {
    return <LoadingSpinner message="Loading wellness resources..." />;
  }

  return (
    <Box sx={{ p: 3, maxWidth: 1400, mx: 'auto' }}>
      <Typography variant="h4" sx={{ mb: 3, fontWeight: 600, color: 'primary.main' }}>
        Wellness Resources
      </Typography>

      <Typography variant="body1" sx={{ mb: 4, color: 'text.secondary' }}>
        Discover personalized wellness resources, tools, and activities to support your mental health and well-being journey.
      </Typography>

      {/* Search and Filters */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                placeholder="Search resources..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <Search />
                    </InputAdornment>
                  ),
                }}
              />
            </Grid>
            
            <Grid item xs={12} md={2}>
              <FormControl fullWidth>
                <InputLabel>Category</InputLabel>
                <Select
                  value={selectedCategory}
                  onChange={(e) => setSelectedCategory(e.target.value)}
                  label="Category"
                >
                  {categories.map((category) => (
                    <MenuItem key={category.value} value={category.value}>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        {category.icon}
                        <Typography sx={{ ml: 1 }}>{category.label}</Typography>
                      </Box>
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12} md={2}>
              <FormControl fullWidth>
                <InputLabel>Difficulty</InputLabel>
                <Select
                  value={selectedDifficulty}
                  onChange={(e) => setSelectedDifficulty(e.target.value)}
                  label="Difficulty"
                >
                  {difficulties.map((difficulty) => (
                    <MenuItem key={difficulty.value} value={difficulty.value}>
                      {difficulty.label}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12} md={2}>
              <FormControl fullWidth>
                <InputLabel>Duration</InputLabel>
                <Select
                  value={selectedDuration}
                  onChange={(e) => setSelectedDuration(e.target.value)}
                  label="Duration"
                >
                  {durations.map((duration) => (
                    <MenuItem key={duration.value} value={duration.value}>
                      {duration.label}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Tabs */}
      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={tabValue} onChange={handleTabChange} aria-label="resources tabs">
          <Tab label={`All Resources (${filteredResources.length})`} />
          <Tab label={`Favorites (${favoriteResources.length})`} />
          <Tab label={`Recently Viewed (${recentlyViewedResources.length})`} />
          <Tab label="Recommended" />
        </Tabs>
      </Box>

      {/* All Resources Tab */}
      <TabPanel value={tabValue} index={0}>
        {filteredResources.length > 0 ? (
          <Grid container spacing={3}>
            {filteredResources.map((resource) => (
              <Grid item xs={12} md={6} lg={4} key={resource.id}>
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
                  onClick={() => handleResourceClick(resource.id)}
                >
                  <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                      <Avatar sx={{ bgcolor: 'primary.main' }}>
                        {getCategoryIcon(resource.category)}
                      </Avatar>
                      <IconButton
                        size="small"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleFavoriteToggle(resource.id);
                        }}
                      >
                        {favorites.includes(resource.id) ? <Favorite color="error" /> : <FavoriteBorder />}
                      </IconButton>
                    </Box>

                    <Typography variant="h6" sx={{ mb: 1, fontWeight: 600, lineHeight: 1.3 }}>
                      {resource.title}
                    </Typography>

                    <Typography variant="body2" color="text.secondary" sx={{ mb: 2, lineHeight: 1.5 }}>
                      {resource.description}
                    </Typography>

                    <Box sx={{ display: 'flex', gap: 1, mb: 2, flexWrap: 'wrap' }}>
                      <Chip
                        label={resource.difficultyLevel}
                        size="small"
                        color={getDifficultyColor(resource.difficultyLevel) as any}
                      />
                      {resource.durationMinutes && (
                        <Chip
                          icon={<AccessTime />}
                          label={getDurationLabel(resource.durationMinutes)}
                          size="small"
                          variant="outlined"
                        />
                      )}
                    </Box>

                    <Box sx={{ display: 'flex', gap: 1, mb: 2, flexWrap: 'wrap' }}>
                      {resource.tags.slice(0, 3).map((tag, index) => (
                        <Chip
                          key={index}
                          label={tag.replace('-', ' ')}
                          size="small"
                          variant="outlined"
                        />
                      ))}
                      {resource.tags.length > 3 && (
                        <Chip
                          label={`+${resource.tags.length - 3} more`}
                          size="small"
                          variant="outlined"
                        />
                      )}
                    </Box>

                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <Star sx={{ fontSize: 16, color: 'warning.main', mr: 0.5 }} />
                        <Typography variant="body2" color="text.secondary">
                          {resource.confidence ? `${resource.confidence}% match` : 'Recommended'}
                        </Typography>
                      </Box>
                      <Button
                        variant="outlined"
                        size="small"
                        startIcon={<PlayArrow />}
                        onClick={(e) => {
                          e.stopPropagation();
                          handleResourceClick(resource.id);
                        }}
                      >
                        View
                      </Button>
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        ) : (
          <Box sx={{ textAlign: 'center', py: 8 }}>
            <Typography variant="h6" color="text.secondary" sx={{ mb: 2 }}>
              No resources found
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Try adjusting your search criteria or filters.
            </Typography>
          </Box>
        )}
      </TabPanel>

      {/* Favorites Tab */}
      <TabPanel value={tabValue} index={1}>
        {favoriteResources.length > 0 ? (
          <Grid container spacing={3}>
            {favoriteResources.map((resource) => (
              <Grid item xs={12} md={6} lg={4} key={resource.id}>
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
                  onClick={() => handleResourceClick(resource.id)}
                >
                  <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                      <Avatar sx={{ bgcolor: 'primary.main' }}>
                        {getCategoryIcon(resource.category)}
                      </Avatar>
                      <IconButton
                        size="small"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleFavoriteToggle(resource.id);
                        }}
                      >
                        <Favorite color="error" />
                      </IconButton>
                    </Box>

                    <Typography variant="h6" sx={{ mb: 1, fontWeight: 600, lineHeight: 1.3 }}>
                      {resource.title}
                    </Typography>

                    <Typography variant="body2" color="text.secondary" sx={{ mb: 2, lineHeight: 1.5 }}>
                      {resource.description}
                    </Typography>

                    <Box sx={{ display: 'flex', gap: 1, mb: 2, flexWrap: 'wrap' }}>
                      <Chip
                        label={resource.difficultyLevel}
                        size="small"
                        color={getDifficultyColor(resource.difficultyLevel) as any}
                      />
                      {resource.durationMinutes && (
                        <Chip
                          icon={<AccessTime />}
                          label={getDurationLabel(resource.durationMinutes)}
                          size="small"
                          variant="outlined"
                        />
                      )}
                    </Box>

                    <Button
                      variant="contained"
                      size="small"
                      startIcon={<PlayArrow />}
                      onClick={(e) => {
                        e.stopPropagation();
                        handleResourceClick(resource.id);
                      }}
                      fullWidth
                    >
                      View Resource
                    </Button>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        ) : (
          <Box sx={{ textAlign: 'center', py: 8 }}>
            <Typography variant="h6" color="text.secondary" sx={{ mb: 2 }}>
              No favorite resources yet
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
              Start exploring resources and add them to your favorites for quick access.
            </Typography>
            <Button
              variant="contained"
              onClick={() => setTabValue(0)}
            >
              Browse Resources
            </Button>
          </Box>
        )}
      </TabPanel>

      {/* Recently Viewed Tab */}
      <TabPanel value={tabValue} index={2}>
        {recentlyViewedResources.length > 0 ? (
          <Grid container spacing={3}>
            {recentlyViewedResources.map((resource) => (
              <Grid item xs={12} md={6} lg={4} key={resource.id}>
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
                  onClick={() => handleResourceClick(resource.id)}
                >
                  <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                      <Avatar sx={{ bgcolor: 'primary.main' }}>
                        {getCategoryIcon(resource.category)}
                      </Avatar>
                      <IconButton
                        size="small"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleFavoriteToggle(resource.id);
                        }}
                      >
                        {favorites.includes(resource.id) ? <Favorite color="error" /> : <FavoriteBorder />}
                      </IconButton>
                    </Box>

                    <Typography variant="h6" sx={{ mb: 1, fontWeight: 600, lineHeight: 1.3 }}>
                      {resource.title}
                    </Typography>

                    <Typography variant="body2" color="text.secondary" sx={{ mb: 2, lineHeight: 1.5 }}>
                      {resource.description}
                    </Typography>

                    <Box sx={{ display: 'flex', gap: 1, mb: 2, flexWrap: 'wrap' }}>
                      <Chip
                        label={resource.difficultyLevel}
                        size="small"
                        color={getDifficultyColor(resource.difficultyLevel) as any}
                      />
                      {resource.durationMinutes && (
                        <Chip
                          icon={<AccessTime />}
                          label={getDurationLabel(resource.durationMinutes)}
                          size="small"
                          variant="outlined"
                        />
                      )}
                    </Box>

                    <Button
                      variant="outlined"
                      size="small"
                      startIcon={<PlayArrow />}
                      onClick={(e) => {
                        e.stopPropagation();
                        handleResourceClick(resource.id);
                      }}
                      fullWidth
                    >
                      View Again
                    </Button>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        ) : (
          <Box sx={{ textAlign: 'center', py: 8 }}>
            <Typography variant="h6" color="text.secondary" sx={{ mb: 2 }}>
              No recently viewed resources
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
              Start exploring resources and they'll appear here for quick access.
            </Typography>
            <Button
              variant="contained"
              onClick={() => setTabValue(0)}
            >
              Browse Resources
            </Button>
          </Box>
        )}
      </TabPanel>

      {/* Recommended Tab */}
      <TabPanel value={tabValue} index={3}>
        <Alert severity="info" sx={{ mb: 3 }}>
          These resources are personalized based on your wellness profile and preferences.
        </Alert>
        
        {recommendedResources.length > 0 ? (
          <Grid container spacing={3}>
            {recommendedResources.map((resource) => (
              <Grid item xs={12} md={6} lg={4} key={resource.id}>
                <Card 
                  sx={{ 
                    height: '100%', 
                    cursor: 'pointer',
                    transition: 'transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out',
                    border: '2px solid',
                    borderColor: 'primary.main',
                    '&:hover': {
                      transform: 'translateY(-4px)',
                      boxShadow: '0 8px 25px rgba(0,0,0,0.15)',
                    },
                  }}
                  onClick={() => handleResourceClick(resource.id)}
                >
                  <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                      <Avatar sx={{ bgcolor: 'primary.main' }}>
                        {getCategoryIcon(resource.category)}
                      </Avatar>
                      <Chip
                        label="Recommended"
                        size="small"
                        color="primary"
                        icon={<TrendingUp />}
                      />
                    </Box>

                    <Typography variant="h6" sx={{ mb: 1, fontWeight: 600, lineHeight: 1.3 }}>
                      {resource.title}
                    </Typography>

                    <Typography variant="body2" color="text.secondary" sx={{ mb: 2, lineHeight: 1.5 }}>
                      {resource.description}
                    </Typography>

                    <Box sx={{ display: 'flex', gap: 1, mb: 2, flexWrap: 'wrap' }}>
                      <Chip
                        label={resource.difficultyLevel}
                        size="small"
                        color={getDifficultyColor(resource.difficultyLevel) as any}
                      />
                      {resource.durationMinutes && (
                        <Chip
                          icon={<AccessTime />}
                          label={getDurationLabel(resource.durationMinutes)}
                          size="small"
                          variant="outlined"
                        />
                      )}
                    </Box>

                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <Star sx={{ fontSize: 16, color: 'warning.main', mr: 0.5 }} />
                        <Typography variant="body2" color="text.secondary">
                          {resource.confidence ? `${resource.confidence}% match` : 'Highly recommended'}
                        </Typography>
                      </Box>
                      <Button
                        variant="contained"
                        size="small"
                        startIcon={<PlayArrow />}
                        onClick={(e) => {
                          e.stopPropagation();
                          handleResourceClick(resource.id);
                        }}
                      >
                        Start
                      </Button>
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        ) : (
          <Box sx={{ textAlign: 'center', py: 8 }}>
            <Typography variant="h6" color="text.secondary" sx={{ mb: 2 }}>
              No recommendations available
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
              Complete your wellness profile to get personalized recommendations.
            </Typography>
            <Button
              variant="contained"
              onClick={() => navigate('/wellness/check-in')}
            >
              Complete Wellness Profile
            </Button>
          </Box>
        )}
      </TabPanel>
    </Box>
  );
};

export default Resources;
<｜tool▁call▁end｜><｜tool▁calls▁end｜>