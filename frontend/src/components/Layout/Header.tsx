import React, { useState } from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Box,
  Avatar,
  Menu,
  MenuItem,
  Badge,
  Tooltip,
  Divider,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Notifications as NotificationsIcon,
  AccountCircle,
  Settings,
  Logout,
  Person,
} from '@mui/icons-material';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';

import { RootState } from '../../store';
import { toggleSidebar } from '../../store/slices/uiSlice';
import { logout } from '../../store/slices/authSlice';

const Header: React.FC = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { user } = useSelector((state: RootState) => state.auth);
  const { sidebarOpen } = useSelector((state: RootState) => state.ui);

  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [notificationAnchorEl, setNotificationAnchorEl] = useState<null | HTMLElement>(null);

  const handleProfileMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleNotificationMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setNotificationAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
    setNotificationAnchorEl(null);
  };

  const handleLogout = () => {
    dispatch(logout());
    handleMenuClose();
    navigate('/login');
  };

  const handleProfile = () => {
    navigate('/profile');
    handleMenuClose();
  };

  const handleSettings = () => {
    navigate('/settings');
    handleMenuClose();
  };

  const getInitials = (firstName: string, lastName: string) => {
    return `${firstName.charAt(0)}${lastName.charAt(0)}`.toUpperCase();
  };

  const getRoleDisplayName = (roles: string[]) => {
    if (roles.includes('admin')) return 'Administrator';
    if (roles.includes('hr')) return 'HR Professional';
    if (roles.includes('manager')) return 'Manager';
    return 'Employee';
  };

  return (
    <AppBar
      position="sticky"
      sx={{
        zIndex: (theme) => theme.zIndex.drawer + 1,
        backgroundColor: '#1a252f',
        color: 'white',
        boxShadow: '0 2px 8px rgba(0,0,0,0.3)',
      }}
    >
      <Toolbar>
        {/* Menu Toggle Button */}
        <IconButton
          edge="start"
          color="inherit"
          aria-label="menu"
          onClick={() => dispatch(toggleSidebar())}
          sx={{ mr: 2 }}
        >
          <MenuIcon />
        </IconButton>

        {/* App Title */}
        <Typography
          variant="h6"
          component="div"
          sx={{ flexGrow: 1, fontWeight: 600, color: 'white' }}
        >
          🌟 Wellness Journey
        </Typography>

        {/* Right Side Actions */}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          {/* Notifications */}
          <Tooltip title="Notifications">
            <IconButton
              color="inherit"
              onClick={handleNotificationMenuOpen}
              sx={{ position: 'relative' }}
            >
              <Badge badgeContent={3} color="error">
                <NotificationsIcon />
              </Badge>
            </IconButton>
          </Tooltip>

          {/* User Profile */}
          <Tooltip title="Account settings">
            <IconButton
              onClick={handleProfileMenuOpen}
              sx={{ ml: 1 }}
            >
              <Box
                sx={{
                  width: 40,
                  height: 40,
                  borderRadius: '50%',
                  backgroundImage: 'url(https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=40&h=40&fit=crop&crop=face)',
                  backgroundSize: 'cover',
                  backgroundPosition: 'center',
                  border: '2px solid #ffffff'
                }}
              />
            </IconButton>
          </Tooltip>
        </Box>

        {/* Profile Menu */}
        <Menu
          anchorEl={anchorEl}
          open={Boolean(anchorEl)}
          onClose={handleMenuClose}
          PaperProps={{
            sx: {
              mt: 1,
              minWidth: 200,
              bgcolor: '#34495e',
              color: 'white',
              boxShadow: '0 4px 12px rgba(0,0,0,0.3)',
              '& .MuiMenuItem-root': {
                color: 'white',
                '&:hover': {
                  bgcolor: '#2c3e50',
                },
              },
            },
          }}
        >
          {user && (
            <>
              <MenuItem disabled>
                <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
                  <Typography variant="subtitle2" sx={{ fontWeight: 600, color: 'white' }}>
                    {user.firstName} {user.lastName}
                  </Typography>
                  <Typography variant="caption" sx={{ color: '#bdc3c7' }}>
                    {getRoleDisplayName(user.roles)}
                  </Typography>
                  <Typography variant="caption" sx={{ color: '#bdc3c7' }}>
                    {user.email}
                  </Typography>
                </Box>
              </MenuItem>
              <Divider sx={{ bgcolor: '#2c3e50' }} />
            </>
          )}

          <MenuItem onClick={handleProfile}>
            <Person sx={{ mr: 2 }} />
            Profile
          </MenuItem>

          <MenuItem onClick={handleSettings}>
            <Settings sx={{ mr: 2 }} />
            Settings
          </MenuItem>

          <Divider sx={{ bgcolor: '#2c3e50' }} />

          <MenuItem onClick={handleLogout}>
            <Logout sx={{ mr: 2 }} />
            Logout
          </MenuItem>
        </Menu>

        {/* Notifications Menu */}
        <Menu
          anchorEl={notificationAnchorEl}
          open={Boolean(notificationAnchorEl)}
          onClose={handleMenuClose}
          PaperProps={{
            sx: {
              mt: 1,
              minWidth: 300,
              maxHeight: 400,
              bgcolor: '#34495e',
              color: 'white',
              boxShadow: '0 4px 12px rgba(0,0,0,0.3)',
              '& .MuiMenuItem-root': {
                color: 'white',
                '&:hover': {
                  bgcolor: '#2c3e50',
                },
              },
            },
          }}
        >
          <MenuItem disabled>
            <Typography variant="subtitle2" sx={{ fontWeight: 600, color: 'white' }}>
              Notifications
            </Typography>
          </MenuItem>
          <Divider sx={{ bgcolor: '#2c3e50' }} />
          <MenuItem>
            <Typography variant="body2" sx={{ color: '#bdc3c7' }}>
              Welcome back! How are you feeling today?
            </Typography>
          </MenuItem>
          <MenuItem>
            <Typography variant="body2" sx={{ color: '#bdc3c7' }}>
              New wellness resources available
            </Typography>
          </MenuItem>
          <MenuItem>
            <Typography variant="body2" sx={{ color: '#bdc3c7' }}>
              Weekly wellness check-in reminder
            </Typography>
          </MenuItem>
        </Menu>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
