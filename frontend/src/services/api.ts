import axios, { AxiosInstance, AxiosResponse } from 'axios';

// Create axios instance with base configuration
const api: AxiosInstance = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle auth errors
api.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Authentication API
export const authAPI = {
  login: async (credentials: { email: string; password: string }) => {
    const response = await api.post('/auth/login', credentials);
    return response.data;
  },

  logout: async () => {
    const response = await api.post('/auth/logout');
    return response.data;
  },

  getProfile: async () => {
    const response = await api.get('/auth/profile');
    return response.data;
  },

  updateConsent: async (consentGiven: boolean) => {
    const response = await api.put('/auth/consent', { consent_given: consentGiven });
    return response.data;
  },

  refreshToken: async () => {
    const response = await api.post('/auth/refresh');
    return response.data;
  },
};

// Wellness API
export const wellnessAPI = {
  getEntries: async () => {
    const response = await api.get('/wellness/entries');
    return response.data;
  },

  createEntry: async (entry: any) => {
    const response = await api.post('/wellness/entries', entry);
    return response.data;
  },

  sendConversation: async (message: string) => {
    const response = await api.post('/conversation', { message });
    return response.data;
  },

  getConversations: async () => {
    const response = await api.get('/conversations');
    return response.data;
  },

  getRecommendations: async (needs: string) => {
    const response = await api.post('/recommendations', { needs });
    return response.data;
  },

  trackMood: async (moodData: { value: number; description?: string }) => {
    const response = await api.post('/wellness/mood', moodData);
    return response.data;
  },

  getWellnessInsights: async (userId: string) => {
    const response = await api.get(`/wellness/insights/${userId}`);
    return response.data;
  },
};

// Analytics API
export const analyticsAPI = {
  getOrganizationalHealth: async (timeframe: string) => {
    const response = await api.get(`/analytics/organizational-health?timeframe=${timeframe}`);
    return response.data;
  },

  getTeamAnalytics: async (timeframe: string) => {
    const response = await api.get(`/analytics/team?timeframe=${timeframe}`);
    return response.data;
  },

  getRiskAssessments: async (filters: { teamId?: string; riskType?: string; timeframe?: string }) => {
    const params = new URLSearchParams();
    if (filters.teamId) params.append('team_id', filters.teamId);
    if (filters.riskType) params.append('risk_type', filters.riskType);
    if (filters.timeframe) params.append('timeframe', filters.timeframe);
    
    const response = await api.get(`/analytics/risk-assessments?${params.toString()}`);
    return response.data;
  },

  generateReport: async (reportConfig: { type: string; timeframe: string; filters: Record<string, any> }) => {
    const response = await api.post('/analytics/reports', reportConfig);
    return response.data;
  },

  getMetrics: async (metricNames: string[]) => {
    const params = new URLSearchParams();
    metricNames.forEach(name => params.append('metrics', name));
    const response = await api.get(`/analytics/metrics?${params.toString()}`);
    return response.data;
  },

  getSystemHealth: async () => {
    const response = await api.get('/health');
    return response.data;
  },
};

// Resources API
export const resourcesAPI = {
  getResources: async (filters?: { category?: string; search?: string }) => {
    const params = new URLSearchParams();
    if (filters?.category) params.append('category', filters.category);
    if (filters?.search) params.append('search', filters.search);
    
    const response = await api.get(`/resources?${params.toString()}`);
    return response.data;
  },

  getResourceDetails: async (resourceId: string) => {
    const response = await api.get(`/resources/${resourceId}`);
    return response.data;
  },

  recordInteraction: async (interaction: any) => {
    const response = await api.post('/resources/interactions', interaction);
    return response.data;
  },

  getInteractions: async () => {
    const response = await api.get('/resources/interactions');
    return response.data;
  },

  getResourceCategories: async () => {
    const response = await api.get('/resources/categories');
    return response.data;
  },
};

// Risk Assessment API
export const riskAPI = {
  assessRisk: async (content: string, contentType: string = 'conversation') => {
    const response = await api.post('/risk/assess', { content, content_type: contentType });
    return response.data;
  },

  getRiskProfile: async (userId: string) => {
    const response = await api.get(`/risk/profile/${userId}`);
    return response.data;
  },

  getRiskTrends: async (timeframe: string) => {
    const response = await api.get(`/risk/trends?timeframe=${timeframe}`);
    return response.data;
  },
};

// Compliance API
export const complianceAPI = {
  auditCompliance: async (systemData: any) => {
    const response = await api.post('/compliance/audit', systemData);
    return response.data;
  },

  getAuditLog: async (startDate?: string, endDate?: string) => {
    const params = new URLSearchParams();
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);
    
    const response = await api.get(`/compliance/audit-log?${params.toString()}`);
    return response.data;
  },

  getPrivacyViolations: async () => {
    const response = await api.get('/compliance/privacy-violations');
    return response.data;
  },
};

// System API
export const systemAPI = {
  getSystemMetrics: async () => {
    const response = await api.get('/system/metrics');
    return response.data;
  },

  getAgentMetrics: async () => {
    const response = await api.get('/system/agent-metrics');
    return response.data;
  },

  getWorkflowStats: async () => {
    const response = await api.get('/system/workflow-stats');
    return response.data;
  },
};

export default api;
