import React, { useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { Box, CssBaseline } from '@mui/material';

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
import Profile from './pages/Profile/Profile';

// Components
import NotificationSystem from './components/Common/NotificationSystem';
import LoadingSpinner from './components/Common/LoadingSpinner';

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
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
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
            <Box component="main" sx={{ flexGrow: 1, p: 3, backgroundColor: 'background.default' }}>
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
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      )}
    </Box>
  );
};

export default App;
