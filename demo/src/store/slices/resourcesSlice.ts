import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { mockResources, preloadedSearch } from '../../mock-data/index';

export interface Resource {
  id: string;
  title: string;
  description: string;
  category: string;
  difficultyLevel: 'beginner' | 'intermediate' | 'advanced';
  durationMinutes: number;
  tags: string[];
  author: string;
  contentUrl: string;
  thumbnailUrl?: string;
  isActive: boolean;
  viewCount: number;
  rating: number;
  ratingCount: number;
  createdAt: string;
}

export interface ResourcesState {
  resources: Resource[];
  currentResource: Resource | null;
  filteredResources: Resource[];
  categories: string[];
  searchQuery: string;
  selectedCategory: string;
  selectedDifficulty: string;
  isLoading: boolean;
  error: string | null;
  searchResults: any[];
  isSearching: boolean;
}

const initialState: ResourcesState = {
  resources: [],
  currentResource: null,
  filteredResources: [],
  categories: [],
  searchQuery: '',
  selectedCategory: '',
  selectedDifficulty: '',
  isLoading: false,
  error: null,
  searchResults: [],
  isSearching: false,
};

// Mock async thunks
export const fetchResources = createAsyncThunk(
  'resources/fetchResources',
  async (_, { rejectWithValue }) => {
    try {
      await new Promise(resolve => setTimeout(resolve, 800));
      
      const resources: Resource[] = mockResources.map(resource => ({
        id: resource.id,
        title: resource.title,
        description: resource.description,
        category: resource.category,
        difficultyLevel: resource.difficulty_level,
        durationMinutes: resource.duration_minutes,
        tags: resource.tags,
        author: resource.author,
        contentUrl: resource.content_url,
        thumbnailUrl: resource.thumbnail_url,
        isActive: resource.is_active,
        viewCount: resource.view_count,
        rating: resource.rating,
        ratingCount: resource.rating_count,
        createdAt: resource.created_at,
      }));
      
      return resources;
    } catch (error: any) {
      return rejectWithValue('Failed to fetch resources');
    }
  }
);

export const fetchResourceById = createAsyncThunk(
  'resources/fetchResourceById',
  async (resourceId: string, { rejectWithValue }) => {
    try {
      await new Promise(resolve => setTimeout(resolve, 600));
      
      const resource = mockResources.find(r => r.id === resourceId);
      if (!resource) {
        return rejectWithValue('Resource not found');
      }
      
      return {
        id: resource.id,
        title: resource.title,
        description: resource.description,
        category: resource.category,
        difficultyLevel: resource.difficulty_level,
        durationMinutes: resource.duration_minutes,
        tags: resource.tags,
        author: resource.author,
        contentUrl: resource.content_url,
        thumbnailUrl: resource.thumbnail_url,
        isActive: resource.is_active,
        viewCount: resource.view_count,
        rating: resource.rating,
        ratingCount: resource.rating_count,
        createdAt: resource.created_at,
      };
    } catch (error: any) {
      return rejectWithValue('Failed to fetch resource');
    }
  }
);

export const searchResources = createAsyncThunk(
  'resources/searchResources',
  async (query: string, { rejectWithValue }) => {
    try {
      await new Promise(resolve => setTimeout(resolve, 500));
      
      // Simulate search functionality
      const results = mockResources
        .filter(resource => 
          resource.title.toLowerCase().includes(query.toLowerCase()) ||
          resource.description.toLowerCase().includes(query.toLowerCase()) ||
          resource.tags.some(tag => tag.toLowerCase().includes(query.toLowerCase()))
        )
        .map(resource => ({
          id: resource.id,
          title: resource.title,
          description: resource.description,
          category: resource.category,
          rating: resource.rating,
          duration: `${resource.duration_minutes} min`,
        }));
      
      return results;
    } catch (error: any) {
      return rejectWithValue('Failed to search resources');
    }
  }
);

const resourcesSlice = createSlice({
  name: 'resources',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    setCurrentResource: (state, action: PayloadAction<Resource | null>) => {
      state.currentResource = action.payload;
    },
    setSearchQuery: (state, action: PayloadAction<string>) => {
      state.searchQuery = action.payload;
    },
    setSelectedCategory: (state, action: PayloadAction<string>) => {
      state.selectedCategory = action.payload;
    },
    setSelectedDifficulty: (state, action: PayloadAction<string>) => {
      state.selectedDifficulty = action.payload;
    },
    filterResources: (state) => {
      let filtered = state.resources;
      
      if (state.selectedCategory) {
        filtered = filtered.filter(resource => resource.category === state.selectedCategory);
      }
      
      if (state.selectedDifficulty) {
        filtered = filtered.filter(resource => resource.difficultyLevel === state.selectedDifficulty);
      }
      
      if (state.searchQuery) {
        filtered = filtered.filter(resource =>
          resource.title.toLowerCase().includes(state.searchQuery.toLowerCase()) ||
          resource.description.toLowerCase().includes(state.searchQuery.toLowerCase()) ||
          resource.tags.some(tag => tag.toLowerCase().includes(state.searchQuery.toLowerCase()))
        );
      }
      
      state.filteredResources = filtered;
    },
    clearFilters: (state) => {
      state.searchQuery = '';
      state.selectedCategory = '';
      state.selectedDifficulty = '';
      state.filteredResources = state.resources;
    },
    setPreloadedSearch: (state) => {
      state.searchQuery = preloadedSearch.query;
      state.searchResults = preloadedSearch.results;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch Resources
      .addCase(fetchResources.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchResources.fulfilled, (state, action) => {
        state.isLoading = false;
        state.resources = action.payload;
        state.filteredResources = action.payload;
        
        // Extract unique categories
        const categories = [...new Set(action.payload.map(resource => resource.category))];
        state.categories = categories;
      })
      .addCase(fetchResources.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      // Fetch Resource by ID
      .addCase(fetchResourceById.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchResourceById.fulfilled, (state, action) => {
        state.isLoading = false;
        state.currentResource = action.payload;
      })
      .addCase(fetchResourceById.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      // Search Resources
      .addCase(searchResources.pending, (state) => {
        state.isSearching = true;
        state.error = null;
      })
      .addCase(searchResources.fulfilled, (state, action) => {
        state.isSearching = false;
        state.searchResults = action.payload;
      })
      .addCase(searchResources.rejected, (state, action) => {
        state.isSearching = false;
        state.error = action.payload as string;
      });
  },
});

export const {
  clearError,
  setCurrentResource,
  setSearchQuery,
  setSelectedCategory,
  setSelectedDifficulty,
  filterResources,
  clearFilters,
  setPreloadedSearch,
} = resourcesSlice.actions;

export default resourcesSlice.reducer;
