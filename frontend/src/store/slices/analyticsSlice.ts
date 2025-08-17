import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { analyticsAPI } from '../../services/api';

export interface AnalyticsMetric {
  name: string;
  value: number;
  unit: string;
  trend: 'up' | 'down' | 'stable';
  change: number;
  timestamp: string;
}

export interface TeamAnalytics {
  teamId: string;
  teamName: string;
  wellnessScore: number;
  stressLevel: number;
  engagementScore: number;
  riskLevel: number;
  memberCount: number;
  trends: AnalyticsMetric[];
}

export interface RiskAssessment {
  id: string;
  userId: string;
  riskType: string;
  riskLevel: number;
  confidenceScore: number;
  indicators: string[];
  context: string;
  recommendations: string[];
  createdAt: string;
}

export interface OrganizationalHealth {
  overallWellnessScore: number;
  averageStressLevel: number;
  engagementScore: number;
  burnoutRisk: number;
  workLifeBalance: number;
  teamCollaboration: number;
  trends: AnalyticsMetric[];
  highRiskTeams: TeamAnalytics[];
  recommendations: string[];
}

export interface AnalyticsState {
  organizationalHealth: OrganizationalHealth | null;
  teamAnalytics: TeamAnalytics[];
  riskAssessments: RiskAssessment[];
  metrics: AnalyticsMetric[];
  selectedTimeframe: string;
  selectedTeam: string | null;
  isLoading: boolean;
  error: string | null;
}

const initialState: AnalyticsState = {
  organizationalHealth: null,
  teamAnalytics: [],
  riskAssessments: [],
  metrics: [],
  selectedTimeframe: '30d',
  selectedTeam: null,
  isLoading: false,
  error: null,
};

// Async thunks
export const fetchOrganizationalHealth = createAsyncThunk(
  'analytics/fetchOrganizationalHealth',
  async (timeframe: string, { rejectWithValue }) => {
    try {
      const response = await analyticsAPI.getOrganizationalHealth(timeframe);
      return response;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch organizational health');
    }
  }
);

export const fetchTeamAnalytics = createAsyncThunk(
  'analytics/fetchTeamAnalytics',
  async (timeframe: string, { rejectWithValue }) => {
    try {
      const response = await analyticsAPI.getTeamAnalytics(timeframe);
      return response;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch team analytics');
    }
  }
);

export const fetchRiskAssessments = createAsyncThunk(
  'analytics/fetchRiskAssessments',
  async (filters: { teamId?: string; riskType?: string; timeframe?: string }, { rejectWithValue }) => {
    try {
      const response = await analyticsAPI.getRiskAssessments(filters);
      return response;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch risk assessments');
    }
  }
);

export const generateReport = createAsyncThunk(
  'analytics/generateReport',
  async (reportConfig: { type: string; timeframe: string; filters: Record<string, any> }, { rejectWithValue }) => {
    try {
      const response = await analyticsAPI.generateReport(reportConfig);
      return response;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to generate report');
    }
  }
);

export const fetchMetrics = createAsyncThunk(
  'analytics/fetchMetrics',
  async (metricNames: string[], { rejectWithValue }) => {
    try {
      const response = await analyticsAPI.getMetrics(metricNames);
      return response;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch metrics');
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
    setTimeframe: (state, action: PayloadAction<string>) => {
      state.selectedTimeframe = action.payload;
    },
    setSelectedTeam: (state, action: PayloadAction<string | null>) => {
      state.selectedTeam = action.payload;
    },
    addRiskAssessment: (state, action: PayloadAction<RiskAssessment>) => {
      state.riskAssessments.unshift(action.payload);
    },
    updateMetric: (state, action: PayloadAction<AnalyticsMetric>) => {
      const index = state.metrics.findIndex(m => m.name === action.payload.name);
      if (index !== -1) {
        state.metrics[index] = action.payload;
      } else {
        state.metrics.push(action.payload);
      }
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
      // Fetch Risk Assessments
      .addCase(fetchRiskAssessments.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchRiskAssessments.fulfilled, (state, action) => {
        state.isLoading = false;
        state.riskAssessments = action.payload;
      })
      .addCase(fetchRiskAssessments.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      // Generate Report
      .addCase(generateReport.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(generateReport.fulfilled, (state, action) => {
        state.isLoading = false;
        // Handle report generation result
      })
      .addCase(generateReport.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      // Fetch Metrics
      .addCase(fetchMetrics.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchMetrics.fulfilled, (state, action) => {
        state.isLoading = false;
        state.metrics = action.payload;
      })
      .addCase(fetchMetrics.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });
  },
});

export const {
  clearError,
  setTimeframe,
  setSelectedTeam,
  addRiskAssessment,
  updateMetric,
} = analyticsSlice.actions;

export default analyticsSlice.reducer;
