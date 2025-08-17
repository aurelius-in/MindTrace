import React, { useEffect, useState } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  CardMedia,
  Typography,
  TextField,
  InputAdornment,
  Chip,
  Rating,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  Search,
  FilterList,
  Bookmark,
  BookmarkBorder,
  AccessTime,
  Person,
  Star,
} from '@mui/icons-material';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { RootState } from '../../store';
import { fetchResources, setSearchQuery, filterResources, clearFilters } from '../../store/slices/resourcesSlice';
import { addNotification } from '../../store/slices/uiSlice';

const Resources: React.FC = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { resources, filteredResources, categories, searchQuery, selectedCategory, selectedDifficulty, isLoading } = useSelector((state: RootState) => state.resources);
  const [searchTerm, setSearchTerm] = useState('stress management techniques');
  const [showFilters, setShowFilters] = useState(false);

  useEffect(() => {
    dispatch(fetchResources());
  }, [dispatch]);

  useEffect(() => {
    // Pre-load search with demo data
    if (searchTerm) {
      dispatch(setSearchQuery(searchTerm));
      dispatch(filterResources());
    }
  }, [dispatch, searchTerm]);

  const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const value = event.target.value;
    setSearchTerm(value);
    dispatch(setSearchQuery(value));
    dispatch(filterResources());
  };

  const handleCategoryChange = (event: any) => {
    dispatch({ type: 'resources/setSelectedCategory', payload: event.target.value });
    dispatch(filterResources());
  };

  const handleDifficultyChange = (event: any) => {
    dispatch({ type: 'resources/setSelectedDifficulty', payload: event.target.value });
    dispatch(filterResources());
  };

  const handleClearFilters = () => {
    setSearchTerm('');
    dispatch(clearFilters());
  };

  const handleResourceClick = (resourceId: string) => {
    navigate(`/resources/${resourceId}`);
  };

  const handleBookmark = (resourceId: string) => {
    dispatch(addNotification({
      message: 'Resource bookmarked successfully!',
      type: 'success',
    }));
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner':
        return 'success';
      case 'intermediate':
        return 'warning';
      case 'advanced':
        return 'error';
      default:
        return 'default';
    }
  };

  const getCategoryColor = (category: string) => {
    const colors = ['primary', 'secondary', 'success', 'warning', 'error', 'info'];
    return colors[category.length % colors.length];
  };

  if (isLoading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '400px' }}>
        <Typography>Loading resources...</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" sx={{ fontWeight: 600, mb: 1 }}>
          Wellness Resources
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Discover tools, guides, and resources to support your wellness journey.
        </Typography>
      </Box>

      {/* Search and Filters */}
      <Box sx={{ mb: 4 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              placeholder="Search resources..."
              value={searchTerm}
              onChange={handleSearchChange}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <Search />
                  </InputAdornment>
                ),
              }}
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
              <Button
                variant="outlined"
                startIcon={<FilterList />}
                onClick={() => setShowFilters(!showFilters)}
              >
                Filters
              </Button>
              {(selectedCategory || selectedDifficulty || searchQuery) && (
                <Button variant="text" onClick={handleClearFilters}>
                  Clear All
                </Button>
              )}
            </Box>
          </Grid>
        </Grid>

        {/* Filter Options */}
        {showFilters && (
          <Box sx={{ mt: 2, p: 2, bgcolor: 'grey.50', borderRadius: 1 }}>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth size="small">
                  <InputLabel>Category</InputLabel>
                  <Select
                    value={selectedCategory}
                    label="Category"
                    onChange={handleCategoryChange}
                  >
                    <MenuItem value="">All Categories</MenuItem>
                    {categories.map((category) => (
                      <MenuItem key={category} value={category}>
                        {category.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth size="small">
                  <InputLabel>Difficulty</InputLabel>
                  <Select
                    value={selectedDifficulty}
                    label="Difficulty"
                    onChange={handleDifficultyChange}
                  >
                    <MenuItem value="">All Levels</MenuItem>
                    <MenuItem value="beginner">Beginner</MenuItem>
                    <MenuItem value="intermediate">Intermediate</MenuItem>
                    <MenuItem value="advanced">Advanced</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
            </Grid>
          </Box>
        )}
      </Box>

      {/* Search Results Info */}
      {searchQuery && (
        <Box sx={{ mb: 3 }}>
          <Typography variant="body2" color="text.secondary">
            Showing {filteredResources.length} results for "{searchQuery}"
          </Typography>
        </Box>
      )}

      {/* Resources Grid */}
      <Grid container spacing={3}>
        {filteredResources.map((resource) => (
          <Grid item xs={12} sm={6} md={4} key={resource.id}>
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
              {resource.thumbnailUrl && (
                <CardMedia
                  component="img"
                  height="140"
                  image={resource.thumbnailUrl}
                  alt={resource.title}
                />
              )}
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 1 }}>
                  <Typography variant="h6" sx={{ fontWeight: 600, flex: 1, mr: 1 }}>
                    {resource.title}
                  </Typography>
                  <Tooltip title="Bookmark">
                    <IconButton
                      size="small"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleBookmark(resource.id);
                      }}
                    >
                      <BookmarkBorder />
                    </IconButton>
                  </Tooltip>
                </Box>

                <Typography variant="body2" color="text.secondary" sx={{ mb: 2, minHeight: '3em' }}>
                  {resource.description}
                </Typography>

                <Box sx={{ display: 'flex', gap: 1, mb: 2, flexWrap: 'wrap' }}>
                  <Chip
                    label={resource.category.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                    size="small"
                    color={getCategoryColor(resource.category) as any}
                  />
                  <Chip
                    label={resource.difficultyLevel}
                    size="small"
                    color={getDifficultyColor(resource.difficultyLevel) as any}
                  />
                </Box>

                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <Rating value={resource.rating} readOnly size="small" />
                    <Typography variant="body2" sx={{ ml: 0.5 }}>
                      ({resource.ratingCount})
                    </Typography>
                  </Box>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <AccessTime sx={{ fontSize: 16, mr: 0.5 }} />
                    <Typography variant="body2">
                      {resource.durationMinutes} min
                    </Typography>
                  </Box>
                </Box>

                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <Person sx={{ fontSize: 16, mr: 0.5 }} />
                    <Typography variant="body2" color="text.secondary">
                      {resource.author}
                    </Typography>
                  </Box>
                  <Button variant="outlined" size="small">
                    View Details
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* No Results */}
      {filteredResources.length === 0 && (
        <Box sx={{ textAlign: 'center', py: 8 }}>
          <Typography variant="h6" color="text.secondary" sx={{ mb: 2 }}>
            No resources found
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
            Try adjusting your search terms or filters
          </Typography>
          <Button variant="outlined" onClick={handleClearFilters}>
            Clear Filters
          </Button>
        </Box>
      )}
    </Box>
  );
};

export default Resources;
