import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { wellnessAPI } from '../../services/api';

export interface WellnessEntry {
  id: string;
  entryType: 'mood' | 'stress' | 'energy' | 'sleep_quality' | 'activity';
  value: number;
  description?: string;
  tags?: string[];
  metadata?: Record<string, any>;
  createdAt: string;
}

export interface Conversation {
  id: string;
  sessionId: string;
  message: string;
  response: string;
  sentimentScore?: number;
  riskLevel?: number;
  riskIndicators?: string[];
  agentType: string;
  workflowType?: string;
  metadata?: Record<string, any>;
  createdAt: string;
}

export interface WellnessRecommendation {
  id: string;
  title: string;
  description: string;
  resourceType: string;
  category: string;
  difficultyLevel: string;
  durationMinutes?: number;
  url?: string;
  tags: string[];
  confidence: number;
}

export interface WellnessState {
  entries: WellnessEntry[];
  conversations: Conversation[];
  recommendations: WellnessRecommendation[];
  currentMood: number | null;
  currentStress: number | null;
  isLoading: boolean;
  error: string | null;
  lastCheckIn: string | null;
}

const initialState: WellnessState = {
  entries: [],
  conversations: [],
  recommendations: [],
  currentMood: null,
  currentStress: null,
  isLoading: false,
  error: null,
  lastCheckIn: null,
};

// Async thunks
export const fetchWellnessEntries = createAsyncThunk(
  'wellness/fetchEntries',
  async (_, { rejectWithValue }) => {
    try {
      const response = await wellnessAPI.getEntries();
      return response;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch entries');
    }
  }
);

export const createWellnessEntry = createAsyncThunk(
  'wellness/createEntry',
  async (entry: Omit<WellnessEntry, 'id' | 'createdAt'>, { rejectWithValue }) => {
    try {
      const response = await wellnessAPI.createEntry(entry);
      return response;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to create entry');
    }
  }
);

export const sendConversation = createAsyncThunk(
  'wellness/sendConversation',
  async (message: string, { rejectWithValue }) => {
    try {
      const response = await wellnessAPI.sendConversation(message);
      return response;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to send conversation');
    }
  }
);

export const fetchConversations = createAsyncThunk(
  'wellness/fetchConversations',
  async (_, { rejectWithValue }) => {
    try {
      const response = await wellnessAPI.getConversations();
      return response;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch conversations');
    }
  }
);

export const getRecommendations = createAsyncThunk(
  'wellness/getRecommendations',
  async (needs: string, { rejectWithValue }) => {
    try {
      const response = await wellnessAPI.getRecommendations(needs);
      return response;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to get recommendations');
    }
  }
);

export const trackMood = createAsyncThunk(
  'wellness/trackMood',
  async (moodData: { value: number; description?: string }, { rejectWithValue }) => {
    try {
      const response = await wellnessAPI.trackMood(moodData);
      return response;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to track mood');
    }
  }
);

const wellnessSlice = createSlice({
  name: 'wellness',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    setCurrentMood: (state, action: PayloadAction<number>) => {
      state.currentMood = action.payload;
    },
    setCurrentStress: (state, action: PayloadAction<number>) => {
      state.currentStress = action.payload;
    },
    addEntry: (state, action: PayloadAction<WellnessEntry>) => {
      state.entries.unshift(action.payload);
    },
    addConversation: (state, action: PayloadAction<Conversation>) => {
      state.conversations.unshift(action.payload);
    },
    clearRecommendations: (state) => {
      state.recommendations = [];
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch Entries
      .addCase(fetchWellnessEntries.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchWellnessEntries.fulfilled, (state, action) => {
        state.isLoading = false;
        state.entries = action.payload;
      })
      .addCase(fetchWellnessEntries.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      // Create Entry
      .addCase(createWellnessEntry.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(createWellnessEntry.fulfilled, (state, action) => {
        state.isLoading = false;
        state.entries.unshift(action.payload);
        state.lastCheckIn = new Date().toISOString();
      })
      .addCase(createWellnessEntry.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      // Send Conversation
      .addCase(sendConversation.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(sendConversation.fulfilled, (state, action) => {
        state.isLoading = false;
        state.conversations.unshift(action.payload);
      })
      .addCase(sendConversation.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      // Fetch Conversations
      .addCase(fetchConversations.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchConversations.fulfilled, (state, action) => {
        state.isLoading = false;
        state.conversations = action.payload;
      })
      .addCase(fetchConversations.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      // Get Recommendations
      .addCase(getRecommendations.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(getRecommendations.fulfilled, (state, action) => {
        state.isLoading = false;
        state.recommendations = action.payload;
      })
      .addCase(getRecommendations.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      // Track Mood
      .addCase(trackMood.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(trackMood.fulfilled, (state, action) => {
        state.isLoading = false;
        state.currentMood = action.payload.value;
        state.entries.unshift(action.payload);
      })
      .addCase(trackMood.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });
  },
});

export const {
  clearError,
  setCurrentMood,
  setCurrentStress,
  addEntry,
  addConversation,
  clearRecommendations,
} = wellnessSlice.actions;

export default wellnessSlice.reducer;
