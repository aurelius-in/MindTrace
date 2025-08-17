import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { mockWellnessEntries, mockConversations } from '../../mock-data';

export interface WellnessEntry {
  id: string;
  userId: string;
  entryType: 'comprehensive' | 'quick_mood';
  value: number;
  description: string;
  moodScore: number;
  stressScore: number;
  energyScore: number;
  sleepHours: number;
  sleepQuality: number;
  workLifeBalance: number;
  socialSupport: number;
  physicalActivity: number;
  nutritionQuality: number;
  productivityLevel: number;
  tags: string[];
  factors: Record<string, any>;
  recommendations: string[];
  riskIndicators: string[];
  isAnonymous: boolean;
  createdAt: string;
}

export interface Conversation {
  id: string;
  userId: string;
  messages: Array<{
    id: string;
    role: 'user' | 'assistant';
    content: string;
    timestamp: string;
    metadata?: Record<string, any>;
  }>;
  summary?: string;
  createdAt: string;
  updatedAt: string;
}

export interface WellnessState {
  entries: WellnessEntry[];
  conversations: Conversation[];
  currentEntry: WellnessEntry | null;
  currentConversation: Conversation | null;
  isLoading: boolean;
  error: string | null;
  analytics: {
    averageMood: number;
    averageStress: number;
    averageEnergy: number;
    trend: 'improving' | 'stable' | 'declining';
  };
}

const initialState: WellnessState = {
  entries: [],
  conversations: [],
  currentEntry: null,
  currentConversation: null,
  isLoading: false,
  error: null,
  analytics: {
    averageMood: 0,
    averageStress: 0,
    averageEnergy: 0,
    trend: 'stable',
  },
};

// Mock async thunks
export const fetchWellnessHistory = createAsyncThunk(
  'wellness/fetchHistory',
  async (_, { rejectWithValue }) => {
    try {
      await new Promise(resolve => setTimeout(resolve, 800));
      
      const entries: WellnessEntry[] = mockWellnessEntries.map(entry => ({
        id: entry.id,
        userId: entry.user_id,
        entryType: entry.entry_type,
        value: entry.value,
        description: entry.description,
        moodScore: entry.mood_score,
        stressScore: entry.stress_score,
        energyScore: entry.energy_score,
        sleepHours: entry.sleep_hours,
        sleepQuality: entry.sleep_quality,
        workLifeBalance: entry.work_life_balance,
        socialSupport: entry.social_support,
        physicalActivity: entry.physical_activity,
        nutritionQuality: entry.nutrition_quality,
        productivityLevel: entry.productivity_level,
        tags: entry.tags,
        factors: entry.factors,
        recommendations: entry.recommendations,
        riskIndicators: entry.risk_indicators,
        isAnonymous: entry.is_anonymous,
        createdAt: entry.created_at,
      }));
      
      return entries;
    } catch (error: any) {
      return rejectWithValue('Failed to fetch wellness history');
    }
  }
);

export const submitWellnessCheckIn = createAsyncThunk(
  'wellness/submitCheckIn',
  async (entry: Partial<WellnessEntry>, { rejectWithValue }) => {
    try {
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const newEntry: WellnessEntry = {
        id: Date.now().toString(),
        userId: '1', // Demo user ID
        entryType: entry.entryType || 'comprehensive',
        value: entry.value || 7.0,
        description: entry.description || '',
        moodScore: entry.moodScore || 7.0,
        stressScore: entry.stressScore || 5.0,
        energyScore: entry.energyScore || 7.0,
        sleepHours: entry.sleepHours || 7.0,
        sleepQuality: entry.sleepQuality || 7.0,
        workLifeBalance: entry.workLifeBalance || 7.0,
        socialSupport: entry.socialSupport || 7.0,
        physicalActivity: entry.physicalActivity || 6.0,
        nutritionQuality: entry.nutritionQuality || 7.0,
        productivityLevel: entry.productivityLevel || 7.0,
        tags: entry.tags || [],
        factors: entry.factors || {},
        recommendations: entry.recommendations || [],
        riskIndicators: entry.riskIndicators || [],
        isAnonymous: entry.isAnonymous || false,
        createdAt: new Date().toISOString(),
      };
      
      return newEntry;
    } catch (error: any) {
      return rejectWithValue('Failed to submit wellness check-in');
    }
  }
);

export const fetchConversations = createAsyncThunk(
  'wellness/fetchConversations',
  async (_, { rejectWithValue }) => {
    try {
      await new Promise(resolve => setTimeout(resolve, 600));
      
      const conversations: Conversation[] = mockConversations.map(conv => ({
        id: conv.id,
        userId: conv.user_id,
        messages: conv.messages,
        summary: conv.summary,
        createdAt: conv.created_at,
        updatedAt: conv.updated_at,
      }));
      
      return conversations;
    } catch (error: any) {
      return rejectWithValue('Failed to fetch conversations');
    }
  }
);

export const sendMessage = createAsyncThunk(
  'wellness/sendMessage',
  async (message: { content: string; conversationId?: string }, { rejectWithValue, getState }) => {
    try {
      await new Promise(resolve => setTimeout(resolve, 1200));
      
      const state = getState() as any;
      const currentConversation = state.wellness.currentConversation;
      
      const userMessage = {
        id: Date.now().toString(),
        role: 'user' as const,
        content: message.content,
        timestamp: new Date().toISOString(),
      };
      
      // Mock AI response
      const aiResponse = {
        id: (Date.now() + 1).toString(),
        role: 'assistant' as const,
        content: `Thank you for sharing that with me. I understand how you're feeling. Here are some suggestions that might help:\n\n1. **Take a moment to breathe** - Deep breathing can help reduce stress\n2. **Consider your current situation** - What's within your control?\n3. **Reach out for support** - Don't hesitate to talk to colleagues or friends\n\nWould you like to explore any of these areas further?`,
        timestamp: new Date().toISOString(),
      };
      
      return {
        userMessage,
        aiResponse,
        conversationId: currentConversation?.id || 'new-conversation',
      };
    } catch (error: any) {
      return rejectWithValue('Failed to send message');
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
    setCurrentEntry: (state, action: PayloadAction<WellnessEntry | null>) => {
      state.currentEntry = action.payload;
    },
    setCurrentConversation: (state, action: PayloadAction<Conversation | null>) => {
      state.currentConversation = action.payload;
    },
    updateAnalytics: (state, action: PayloadAction<Partial<WellnessState['analytics']>>) => {
      state.analytics = { ...state.analytics, ...action.payload };
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch History
      .addCase(fetchWellnessHistory.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchWellnessHistory.fulfilled, (state, action) => {
        state.isLoading = false;
        state.entries = action.payload;
        
        // Calculate analytics
        if (action.payload.length > 0) {
          const avgMood = action.payload.reduce((sum, entry) => sum + entry.moodScore, 0) / action.payload.length;
          const avgStress = action.payload.reduce((sum, entry) => sum + entry.stressScore, 0) / action.payload.length;
          const avgEnergy = action.payload.reduce((sum, entry) => sum + entry.energyScore, 0) / action.payload.length;
          
          state.analytics = {
            averageMood: Math.round(avgMood * 10) / 10,
            averageStress: Math.round(avgStress * 10) / 10,
            averageEnergy: Math.round(avgEnergy * 10) / 10,
            trend: avgMood > 7 ? 'improving' : avgMood < 5 ? 'declining' : 'stable',
          };
        }
      })
      .addCase(fetchWellnessHistory.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      // Submit Check-in
      .addCase(submitWellnessCheckIn.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(submitWellnessCheckIn.fulfilled, (state, action) => {
        state.isLoading = false;
        state.entries.unshift(action.payload);
        state.currentEntry = action.payload;
      })
      .addCase(submitWellnessCheckIn.rejected, (state, action) => {
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
      // Send Message
      .addCase(sendMessage.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(sendMessage.fulfilled, (state, action) => {
        state.isLoading = false;
        
        if (state.currentConversation) {
          state.currentConversation.messages.push(action.payload.userMessage, action.payload.aiResponse);
          state.currentConversation.updatedAt = new Date().toISOString();
        } else {
          // Create new conversation
          const newConversation: Conversation = {
            id: action.payload.conversationId,
            userId: '1',
            messages: [action.payload.userMessage, action.payload.aiResponse],
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString(),
          };
          state.currentConversation = newConversation;
          state.conversations.unshift(newConversation);
        }
      })
      .addCase(sendMessage.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });
  },
});

export const { clearError, setCurrentEntry, setCurrentConversation, updateAnalytics } = wellnessSlice.actions;
export default wellnessSlice.reducer;
