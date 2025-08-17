import React, { useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { Box, CssBaseline, ThemeProvider, createTheme } from '@mui/material';

import { RootState } from './store';
import { fetchUserProfile } from './store/slices/authSlice';
import { addNotification } from './store/slices/uiSlice';

// Layout Components
import Layout from './components/Layout/Layout';
import Sidebar from './components/Layout/Sidebar';
import Header from './components/Layout/Header';

// Page Components
import Dashboard from './pages/Dashboard/Dashboard';
import WellnessCheckIn from './pages/Wellness/WellnessCheckIn';
import WellnessChat from './pages/Wellness/WellnessChat';
import WellnessHistory from './pages/Wellness/WellnessHistory';
import Resources from './pages/Resources/Resources';
import ResourceDetail from './pages/Resources/ResourceDetail';
import Analytics from './pages/Analytics/Analytics';
import TeamAnalytics from './pages/Analytics/TeamAnalytics';
import OrganizationalHealth from './pages/Analytics/OrganizationalHealth';
import RiskAssessment from './pages/Analytics/RiskAssessment';
import Compliance from './pages/Compliance/Compliance';
import Settings from './pages/Settings/Settings';
import Login from './pages/Auth/Login';
import Register from './pages/Auth/Register';
import ForgotPassword from './pages/Auth/ForgotPassword';
import ResetPassword from './pages/Auth/ResetPassword';
import Profile from './pages/Profile/Profile';

// Components
import NotificationSystem from './components/Common/NotificationSystem';
import LoadingSpinner from './components/Common/LoadingSpinner';

// Create a dark theme based on the demo styling
const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#e74c3c',
      light: '#ff6b6b',
      dark: '#c0392b',
    },
    secondary: {
      main: '#3498db',
      light: '#5dade2',
      dark: '#2980b9',
    },
    background: {
      default: '#2c3e50',
      paper: '#34495e',
    },
    text: {
      primary: '#ffffff',
      secondary: '#bdc3c7',
    },
    success: {
      main: '#27ae60',
      light: '#2ecc71',
      dark: '#229954',
    },
    warning: {
      main: '#f39c12',
      light: '#f1c40f',
      dark: '#e67e22',
    },
    error: {
      main: '#e74c3c',
      light: '#ff6b6b',
      dark: '#c0392b',
    },
  },
  typography: {
    h1: {
      fontSize: '2.5rem',
      fontWeight: 600,
      color: '#ffffff',
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 600,
      color: '#ffffff',
    },
    h3: {
      fontSize: '1.75rem',
      fontWeight: 600,
      color: '#ffffff',
    },
    h4: {
      fontSize: '1.5rem',
      fontWeight: 600,
      color: '#ffffff',
    },
    h5: {
      fontSize: '1.25rem',
      fontWeight: 600,
      color: '#ffffff',
    },
    h6: {
      fontSize: '1.1rem',
      fontWeight: 600,
      color: '#ffffff',
    },
    body1: {
      fontSize: '1rem',
      color: '#bdc3c7',
    },
    body2: {
      fontSize: '0.9rem',
      color: '#bdc3c7',
    },
  },
  components: {
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundColor: '#34495e',
          color: '#ffffff',
          borderRadius: 12,
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          backgroundColor: '#34495e',
          color: '#ffffff',
          borderRadius: 12,
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
          fontWeight: 600,
        },
        contained: {
          backgroundColor: '#e74c3c',
          '&:hover': {
            backgroundColor: '#c0392b',
          },
        },
        outlined: {
          borderColor: '#bdc3c7',
          color: '#bdc3c7',
          '&:hover': {
            borderColor: '#ffffff',
            backgroundColor: 'rgba(255,255,255,0.1)',
          },
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: '#1a252f',
        },
      },
    },
    MuiDrawer: {
      styleOverrides: {
        paper: {
          backgroundColor: '#1a252f',
          color: '#ffffff',
        },
      },
    },
  },
});

// Protected Route Component
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated, isLoading } = useSelector((state: RootState) => state.auth);

  if (isLoading) {
    return <LoadingSpinner />;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
};

// Role-based Route Component
const RoleRoute: React.FC<{ 
  children: React.ReactNode; 
  allowedRoles: string[];
}> = ({ children, allowedRoles }) => {
  const { user } = useSelector((state: RootState) => state.auth);

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  const hasRequiredRole = user.roles.some(role => allowedRoles.includes(role));
  
  if (!hasRequiredRole) {
    return <Navigate to="/dashboard" replace />;
  }

  return <>{children}</>;
};

const App: React.FC = () => {
  const dispatch = useDispatch();
  const { isAuthenticated, isLoading, user } = useSelector((state: RootState) => state.auth);
  const { sidebarOpen } = useSelector((state: RootState) => state.ui);

  useEffect(() => {
    // Check if user is authenticated on app load
    const token = localStorage.getItem('token');
    if (token && !isAuthenticated && !isLoading) {
      dispatch(fetchUserProfile());
    }
  }, [dispatch, isAuthenticated, isLoading]);

  useEffect(() => {
    // Welcome notification for authenticated users
    if (isAuthenticated && user) {
      dispatch(addNotification({
        type: 'info',
        message: `Welcome back, ${user.firstName}! How are you feeling today?`,
        title: 'Welcome',
        duration: 5000,
      }));
    }
  }, [isAuthenticated, user, dispatch]);

  if (isLoading) {
    return <LoadingSpinner />;
  }

  return (
    <ThemeProvider theme={darkTheme}>
      <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: '#2c3e50' }}>
        <CssBaseline />
        
        {/* Notification System */}
        <NotificationSystem />
        
        {isAuthenticated ? (
          <>
            {/* Sidebar */}
            <Sidebar open={sidebarOpen} />
            
            {/* Main Content */}
            <Box sx={{ 
              flexGrow: 1, 
              display: 'flex', 
              flexDirection: 'column',
              marginLeft: sidebarOpen ? '240px' : '64px',
              transition: 'margin-left 0.3s ease',
            }}>
              {/* Header */}
              <Header />
              
              {/* Main Content Area */}
              <Box component="main" sx={{ 
                flexGrow: 1, 
                p: 3, 
                backgroundColor: '#2c3e50',
                minHeight: 'calc(100vh - 64px)',
              }}>
                <Routes>
                  {/* Dashboard */}
                  <Route path="/dashboard" element={
                    <ProtectedRoute>
                      <Dashboard />
                    </ProtectedRoute>
                  } />
                  
                  {/* Wellness Routes */}
                  <Route path="/wellness/check-in" element={
                    <ProtectedRoute>
                      <WellnessCheckIn />
                    </ProtectedRoute>
                  } />
                  <Route path="/wellness/chat" element={
                    <ProtectedRoute>
                      <WellnessChat />
                    </ProtectedRoute>
                  } />
                  <Route path="/wellness/history" element={
                    <ProtectedRoute>
                      <WellnessHistory />
                    </ProtectedRoute>
                  } />
                  
                  {/* Resources Routes */}
                  <Route path="/resources" element={
                    <ProtectedRoute>
                      <Resources />
                    </ProtectedRoute>
                  } />
                  <Route path="/resources/:id" element={
                    <ProtectedRoute>
                      <ResourceDetail />
                    </ProtectedRoute>
                  } />
                  
                  {/* Analytics Routes - Manager and above */}
                  <Route path="/analytics" element={
                    <ProtectedRoute>
                      <RoleRoute allowedRoles={['manager', 'hr', 'admin']}>
                        <Analytics />
                      </RoleRoute>
                    </ProtectedRoute>
                  } />
                  <Route path="/analytics/team" element={
                    <ProtectedRoute>
                      <RoleRoute allowedRoles={['manager', 'hr', 'admin']}>
                        <TeamAnalytics />
                      </RoleRoute>
                    </ProtectedRoute>
                  } />
                  <Route path="/analytics/organizational-health" element={
                    <ProtectedRoute>
                      <RoleRoute allowedRoles={['hr', 'admin']}>
                        <OrganizationalHealth />
                      </RoleRoute>
                    </ProtectedRoute>
                  } />
                  <Route path="/analytics/risk-assessment" element={
                    <ProtectedRoute>
                      <RoleRoute allowedRoles={['hr', 'admin']}>
                        <RiskAssessment />
                      </RoleRoute>
                    </ProtectedRoute>
                  } />
                  
                  {/* Compliance Routes - HR and Admin only */}
                  <Route path="/compliance" element={
                    <ProtectedRoute>
                      <RoleRoute allowedRoles={['hr', 'admin']}>
                        <Compliance />
                      </RoleRoute>
                    </ProtectedRoute>
                  } />
                  
                  {/* Settings and Profile */}
                  <Route path="/settings" element={
                    <ProtectedRoute>
                      <Settings />
                    </ProtectedRoute>
                  } />
                  <Route path="/profile" element={
                    <ProtectedRoute>
                      <Profile />
                    </ProtectedRoute>
                  } />
                  
                  {/* Default redirect */}
                  <Route path="/" element={<Navigate to="/dashboard" replace />} />
                  <Route path="*" element={<Navigate to="/dashboard" replace />} />
                </Routes>
              </Box>
            </Box>
          </>
        ) : (
          /* Authentication Routes */
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/forgot-password" element={<ForgotPassword />} />
            <Route path="/reset-password" element={<ResetPassword />} />
            <Route path="*" element={<Navigate to="/login" replace />} />
          </Routes>
        )}
      </Box>
    </ThemeProvider>
  );
};

export default App;
