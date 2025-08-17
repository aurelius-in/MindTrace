import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { mockAnalytics } from '../../mock-data/index';

export interface AnalyticsState {
  organizationalHealth: {
    overallScore: number;
    trend: 'improving' | 'stable' | 'declining';
    departments: Array<{
      name: string;
      score: number;
      trend: string;
      employeeCount: number;
    }>;
    kpis: Array<{
      name: string;
      value: number;
      target: number;
      status: 'good' | 'warning' | 'critical';
    }>;
  };
  teamAnalytics: {
    teamId: string;
    teamName: string;
    wellnessScore: number;
    engagementScore: number;
    productivityScore: number;
    collaborationScore: number;
    members: Array<{
      userId: string;
      name: string;
      role: string;
      wellnessScore: number;
      participationRate: number;
    }>;
    trends: Array<{
      date: string;
      wellnessScore: number;
      engagementScore: number;
    }>;
  };
  riskAssessment: {
    overallRiskLevel: 'low' | 'medium' | 'high';
    riskFactors: Array<{
      factor: string;
      severity: 'low' | 'medium' | 'high';
      impact: number;
      recommendations: string[];
    }>;
    trends: Array<{
      date: string;
      riskLevel: string;
      riskScore: number;
    }>;
  };
  isLoading: boolean;
  error: string | null;
}

const initialState: AnalyticsState = {
  organizationalHealth: {
    overallScore: 0,
    trend: 'stable',
    departments: [],
    kpis: [],
  },
  teamAnalytics: {
    teamId: '',
    teamName: '',
    wellnessScore: 0,
    engagementScore: 0,
    productivityScore: 0,
    collaborationScore: 0,
    members: [],
    trends: [],
  },
  riskAssessment: {
    overallRiskLevel: 'low',
    riskFactors: [],
    trends: [],
  },
  isLoading: false,
  error: null,
};

// Mock async thunks
export const fetchOrganizationalHealth = createAsyncThunk(
  'analytics/fetchOrganizationalHealth',
  async (_, { rejectWithValue }) => {
    try {
      await new Promise(resolve => setTimeout(resolve, 1000));
      return mockAnalytics.organizational_health;
    } catch (error: any) {
      return rejectWithValue('Failed to fetch organizational health data');
    }
  }
);

export const fetchTeamAnalytics = createAsyncThunk(
  'analytics/fetchTeamAnalytics',
  async (teamId: string, { rejectWithValue }) => {
    try {
      await new Promise(resolve => setTimeout(resolve, 800));
      return mockAnalytics.team_analytics;
    } catch (error: any) {
      return rejectWithValue('Failed to fetch team analytics');
    }
  }
);

export const fetchRiskAssessment = createAsyncThunk(
  'analytics/fetchRiskAssessment',
  async (_, { rejectWithValue }) => {
    try {
      await new Promise(resolve => setTimeout(resolve, 900));
      return mockAnalytics.risk_assessment;
    } catch (error: any) {
      return rejectWithValue('Failed to fetch risk assessment');
    }
  }
);

const analyticsSlice = createSlice({
  name: 'analytics',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    updateOrganizationalHealth: (state, action: PayloadAction<Partial<AnalyticsState['organizationalHealth']>>) => {
      state.organizationalHealth = { ...state.organizationalHealth, ...action.payload };
    },
    updateTeamAnalytics: (state, action: PayloadAction<Partial<AnalyticsState['teamAnalytics']>>) => {
      state.teamAnalytics = { ...state.teamAnalytics, ...action.payload };
    },
    updateRiskAssessment: (state, action: PayloadAction<Partial<AnalyticsState['riskAssessment']>>) => {
      state.riskAssessment = { ...state.riskAssessment, ...action.payload };
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch Organizational Health
      .addCase(fetchOrganizationalHealth.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchOrganizationalHealth.fulfilled, (state, action) => {
        state.isLoading = false;
        state.organizationalHealth = action.payload;
      })
      .addCase(fetchOrganizationalHealth.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      // Fetch Team Analytics
      .addCase(fetchTeamAnalytics.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchTeamAnalytics.fulfilled, (state, action) => {
        state.isLoading = false;
        state.teamAnalytics = action.payload;
      })
      .addCase(fetchTeamAnalytics.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      // Fetch Risk Assessment
      .addCase(fetchRiskAssessment.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchRiskAssessment.fulfilled, (state, action) => {
        state.isLoading = false;
        state.riskAssessment = action.payload;
      })
      .addCase(fetchRiskAssessment.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });
  },
});

export const { clearError, updateOrganizationalHealth, updateTeamAnalytics, updateRiskAssessment } = analyticsSlice.actions;
export default analyticsSlice.reducer;
