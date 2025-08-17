import React, { useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { Box, CssBaseline } from '@mui/material';
import { RootState } from './store';
import { demoLogin } from './store/slices/authSlice';
import { fetchWellnessHistory, fetchConversations } from './store/slices/wellnessSlice';
import { fetchOrganizationalHealth, fetchTeamAnalytics, fetchRiskAssessment } from './store/slices/analyticsSlice';
import { fetchResources, setPreloadedSearch } from './store/slices/resourcesSlice';
import { addNotification } from './store/slices/uiSlice';

// Layout Components
import Header from './components/Layout/Header';
import Sidebar from './components/Layout/Sidebar';
import LoadingSpinner from './components/Common/LoadingSpinner';
import NotificationSystem from './components/Common/NotificationSystem';

// Pages
import Dashboard from './pages/Dashboard/Dashboard';
import WellnessCheckIn from './pages/Wellness/WellnessCheckIn';
import WellnessChat from './pages/Wellness/WellnessChat';
import WellnessHistory from './pages/Wellness/WellnessHistory';
import Resources from './pages/Resources/Resources';
import ResourceDetail from './pages/Resources/ResourceDetail';
import Analytics from './pages/Analytics/Analytics';
import RiskAssessment from './pages/Analytics/RiskAssessment';
import OrganizationalHealth from './pages/Analytics/OrganizationalHealth';
import TeamAnalytics from './pages/Analytics/TeamAnalytics';
import Profile from './pages/Profile/Profile';
import Settings from './pages/Settings/Settings';
import Compliance from './pages/Compliance/Compliance';

// Auth Pages
import Login from './pages/Auth/Login';
import Register from './pages/Auth/Register';
import ForgotPassword from './pages/Auth/ForgotPassword';
import ResetPassword from './pages/Auth/ResetPassword';

const App: React.FC = () => {
  const dispatch = useDispatch();
  const { isAuthenticated, isLoading } = useSelector((state: RootState) => state.auth);
  const { sidebarOpen } = useSelector((state: RootState) => state.ui);

  useEffect(() => {
    // Auto-login for demo
    if (!isAuthenticated && !isLoading) {
      dispatch(demoLogin());
      
      // Add welcome notification
      dispatch(addNotification({
        message: 'Welcome to the Enterprise Employee Wellness AI platform! This is a demo version with realistic mock data.',
        type: 'info',
        duration: 5000,
      }));
    }
  }, [dispatch, isAuthenticated, isLoading]);

  useEffect(() => {
    // Load initial data when authenticated
    if (isAuthenticated) {
      dispatch(fetchWellnessHistory());
      dispatch(fetchConversations());
      dispatch(fetchOrganizationalHealth());
      dispatch(fetchTeamAnalytics('1'));
      dispatch(fetchRiskAssessment());
      dispatch(fetchResources());
      dispatch(setPreloadedSearch());
    }
  }, [dispatch, isAuthenticated]);

  if (isLoading) {
    return <LoadingSpinner />;
  }

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <NotificationSystem />
      
      {isAuthenticated && (
        <>
          <Header />
          <Sidebar />
        </>
      )}
      
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: `calc(100% - ${sidebarOpen ? 240 : 0}px)` },
          ml: { sm: `${sidebarOpen ? 240 : 0}px` },
          transition: 'margin 0.2s ease-in-out',
          mt: isAuthenticated ? 8 : 0,
        }}
      >
        <Routes>
          {/* Auth Routes */}
          <Route path="/login" element={!isAuthenticated ? <Login /> : <Navigate to="/" replace />} />
          <Route path="/register" element={!isAuthenticated ? <Register /> : <Navigate to="/" replace />} />
          <Route path="/forgot-password" element={!isAuthenticated ? <ForgotPassword /> : <Navigate to="/" replace />} />
          <Route path="/reset-password" element={!isAuthenticated ? <ResetPassword /> : <Navigate to="/" replace />} />
          
          {/* Protected Routes */}
          <Route path="/" element={isAuthenticated ? <Dashboard /> : <Navigate to="/login" replace />} />
          <Route path="/wellness/check-in" element={isAuthenticated ? <WellnessCheckIn /> : <Navigate to="/login" replace />} />
          <Route path="/wellness/chat" element={isAuthenticated ? <WellnessChat /> : <Navigate to="/login" replace />} />
          <Route path="/wellness/history" element={isAuthenticated ? <WellnessHistory /> : <Navigate to="/login" replace />} />
          <Route path="/resources" element={isAuthenticated ? <Resources /> : <Navigate to="/login" replace />} />
          <Route path="/resources/:id" element={isAuthenticated ? <ResourceDetail /> : <Navigate to="/login" replace />} />
          <Route path="/analytics" element={isAuthenticated ? <Analytics /> : <Navigate to="/login" replace />} />
          <Route path="/analytics/risk-assessment" element={isAuthenticated ? <RiskAssessment /> : <Navigate to="/login" replace />} />
          <Route path="/analytics/organizational-health" element={isAuthenticated ? <OrganizationalHealth /> : <Navigate to="/login" replace />} />
          <Route path="/analytics/team-analytics" element={isAuthenticated ? <TeamAnalytics /> : <Navigate to="/login" replace />} />
          <Route path="/profile" element={isAuthenticated ? <Profile /> : <Navigate to="/login" replace />} />
          <Route path="/settings" element={isAuthenticated ? <Settings /> : <Navigate to="/login" replace />} />
          <Route path="/compliance" element={isAuthenticated ? <Compliance /> : <Navigate to="/login" replace />} />
          
          {/* Catch all route */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Box>
    </Box>
  );
};

export default App;
