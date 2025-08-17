import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { resourcesAPI } from '../../services/api';

export interface WellnessResource {
  id: string;
  title: string;
  description: string;
  content: string;
  resourceType: string;
  category: string;
  tags: string[];
  difficultyLevel: string;
  durationMinutes?: number;
  url?: string;
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface ResourceInteraction {
  id: string;
  resourceId: string;
  interactionType: 'view' | 'like' | 'share' | 'complete';
  rating?: number;
  feedback?: string;
  createdAt: string;
}

export interface ResourcesState {
  resources: WellnessResource[];
  interactions: ResourceInteraction[];
  favorites: string[];
  recentlyViewed: string[];
  isLoading: boolean;
  error: string | null;
  selectedCategory: string | null;
  searchQuery: string;
}

const initialState: ResourcesState = {
  resources: [],
  interactions: [],
  favorites: [],
  recentlyViewed: [],
  isLoading: false,
  error: null,
  selectedCategory: null,
  searchQuery: '',
};

// Async thunks
export const fetchResources = createAsyncThunk(
  'resources/fetchResources',
  async (filters?: { category?: string; search?: string }, { rejectWithValue }) => {
    try {
      const response = await resourcesAPI.getResources(filters);
      return response;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch resources');
    }
  }
);

export const fetchResourceDetails = createAsyncThunk(
  'resources/fetchResourceDetails',
  async (resourceId: string, { rejectWithValue }) => {
    try {
      const response = await resourcesAPI.getResourceDetails(resourceId);
      return response;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch resource details');
    }
  }
);

export const recordInteraction = createAsyncThunk(
  'resources/recordInteraction',
  async (interaction: Omit<ResourceInteraction, 'id' | 'createdAt'>, { rejectWithValue }) => {
    try {
      const response = await resourcesAPI.recordInteraction(interaction);
      return response;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to record interaction');
    }
  }
);

export const fetchInteractions = createAsyncThunk(
  'resources/fetchInteractions',
  async (_, { rejectWithValue }) => {
    try {
      const response = await resourcesAPI.getInteractions();
      return response;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch interactions');
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
    setSelectedCategory: (state, action: PayloadAction<string | null>) => {
      state.selectedCategory = action.payload;
    },
    setSearchQuery: (state, action: PayloadAction<string>) => {
      state.searchQuery = action.payload;
    },
    addToFavorites: (state, action: PayloadAction<string>) => {
      if (!state.favorites.includes(action.payload)) {
        state.favorites.push(action.payload);
      }
    },
    removeFromFavorites: (state, action: PayloadAction<string>) => {
      state.favorites = state.favorites.filter(id => id !== action.payload);
    },
    addToRecentlyViewed: (state, action: PayloadAction<string>) => {
      const resourceId = action.payload;
      state.recentlyViewed = state.recentlyViewed.filter(id => id !== resourceId);
      state.recentlyViewed.unshift(resourceId);
      // Keep only last 10
      if (state.recentlyViewed.length > 10) {
        state.recentlyViewed = state.recentlyViewed.slice(0, 10);
      }
    },
    clearRecentlyViewed: (state) => {
      state.recentlyViewed = [];
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
      })
      .addCase(fetchResources.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      // Fetch Resource Details
      .addCase(fetchResourceDetails.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchResourceDetails.fulfilled, (state, action) => {
        state.isLoading = false;
        // Update the resource in the list or add it
        const index = state.resources.findIndex(r => r.id === action.payload.id);
        if (index !== -1) {
          state.resources[index] = action.payload;
        } else {
          state.resources.push(action.payload);
        }
      })
      .addCase(fetchResourceDetails.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      // Record Interaction
      .addCase(recordInteraction.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(recordInteraction.fulfilled, (state, action) => {
        state.isLoading = false;
        state.interactions.unshift(action.payload);
      })
      .addCase(recordInteraction.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      // Fetch Interactions
      .addCase(fetchInteractions.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchInteractions.fulfilled, (state, action) => {
        state.isLoading = false;
        state.interactions = action.payload;
      })
      .addCase(fetchInteractions.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });
  },
});

export const {
  clearError,
  setSelectedCategory,
  setSearchQuery,
  addToFavorites,
  removeFromFavorites,
  addToRecentlyViewed,
  clearRecentlyViewed,
} = resourcesSlice.actions;

export default resourcesSlice.reducer;
