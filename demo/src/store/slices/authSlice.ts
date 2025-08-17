import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { mockUsers } from '../../mock-data';

export interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  department: string;
  position: string;
  roles: string[];
  teams: string[];
  consentGiven: boolean;
  consentDate?: string;
  isActive: boolean;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

const initialState: AuthState = {
  user: null,
  token: localStorage.getItem('token'),
  isAuthenticated: false,
  isLoading: false,
  error: null,
};

// Mock async thunks that simulate API calls
export const login = createAsyncThunk(
  'auth/login',
  async (credentials: { email: string; password: string }, { rejectWithValue }) => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Find user in mock data
    const mockUser = mockUsers.find(user => user.email === credentials.email);
    
    if (mockUser && credentials.password === 'password') {
      const user: User = {
        id: mockUser.id,
        email: mockUser.email,
        firstName: mockUser.first_name,
        lastName: mockUser.last_name,
        department: mockUser.department,
        position: mockUser.position,
        roles: [mockUser.role],
        teams: ['Engineering Team'],
        consentGiven: true,
        consentDate: '2024-01-01',
        isActive: mockUser.is_active,
      };
      
      const token = 'mock-jwt-token-' + Date.now();
      localStorage.setItem('token', token);
      
      return { user, token };
    } else {
      return rejectWithValue('Invalid credentials');
    }
  }
);

export const logout = createAsyncThunk(
  'auth/logout',
  async (_, { rejectWithValue }) => {
    try {
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 500));
      localStorage.removeItem('token');
      return null;
    } catch (error: any) {
      localStorage.removeItem('token');
      return rejectWithValue('Logout failed');
    }
  }
);

export const fetchUserProfile = createAsyncThunk(
  'auth/fetchUserProfile',
  async (_, { rejectWithValue }) => {
    try {
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 800));
      
      // Return first mock user as default
      const mockUser = mockUsers[0];
      const user: User = {
        id: mockUser.id,
        email: mockUser.email,
        firstName: mockUser.first_name,
        lastName: mockUser.last_name,
        department: mockUser.department,
        position: mockUser.position,
        roles: [mockUser.role],
        teams: ['Engineering Team'],
        consentGiven: true,
        consentDate: '2024-01-01',
        isActive: mockUser.is_active,
      };
      
      return user;
    } catch (error: any) {
      return rejectWithValue('Failed to fetch profile');
    }
  }
);

export const updateConsent = createAsyncThunk(
  'auth/updateConsent',
  async (consentGiven: boolean, { rejectWithValue, getState }) => {
    try {
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 600));
      
      const state = getState() as any;
      const currentUser = state.auth.user;
      
      if (currentUser) {
        return {
          ...currentUser,
          consentGiven,
          consentDate: new Date().toISOString(),
        };
      }
      
      return rejectWithValue('No user found');
    } catch (error: any) {
      return rejectWithValue('Failed to update consent');
    }
  }
);

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    setToken: (state, action: PayloadAction<string>) => {
      state.token = action.payload;
      state.isAuthenticated = true;
    },
    clearAuth: (state) => {
      state.user = null;
      state.token = null;
      state.isAuthenticated = false;
      state.error = null;
    },
    // Demo-specific action to auto-login
    demoLogin: (state) => {
      const mockUser = mockUsers[0];
      const user: User = {
        id: mockUser.id,
        email: mockUser.email,
        firstName: mockUser.first_name,
        lastName: mockUser.last_name,
        department: mockUser.department,
        position: mockUser.position,
        roles: [mockUser.role],
        teams: ['Engineering Team'],
        consentGiven: true,
        consentDate: '2024-01-01',
        isActive: mockUser.is_active,
      };
      
      state.user = user;
      state.token = 'demo-token';
      state.isAuthenticated = true;
      state.isLoading = false;
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Login
      .addCase(login.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(login.fulfilled, (state, action) => {
        state.isLoading = false;
        state.isAuthenticated = true;
        state.user = action.payload.user;
        state.token = action.payload.token;
      })
      .addCase(login.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      // Logout
      .addCase(logout.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(logout.fulfilled, (state) => {
        state.isLoading = false;
        state.user = null;
        state.token = null;
        state.isAuthenticated = false;
      })
      .addCase(logout.rejected, (state, action) => {
        state.isLoading = false;
        state.user = null;
        state.token = null;
        state.isAuthenticated = false;
        state.error = action.payload as string;
      })
      // Fetch Profile
      .addCase(fetchUserProfile.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchUserProfile.fulfilled, (state, action) => {
        state.isLoading = false;
        state.user = action.payload;
        state.isAuthenticated = true;
      })
      .addCase(fetchUserProfile.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
        state.isAuthenticated = false;
      })
      // Update Consent
      .addCase(updateConsent.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(updateConsent.fulfilled, (state, action) => {
        state.isLoading = false;
        state.user = action.payload;
      })
      .addCase(updateConsent.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });
  },
});

export const { clearError, setToken, clearAuth, demoLogin } = authSlice.actions;
export default authSlice.reducer;
