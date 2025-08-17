import React from 'react';
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Divider,
  Box,
  Typography,
  Collapse,
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  Favorite as WellnessIcon,
  Chat as ChatIcon,
  History as HistoryIcon,
  LibraryBooks as ResourcesIcon,
  Analytics as AnalyticsIcon,
  Group as TeamIcon,
  Business as OrgIcon,
  Security as RiskIcon,
  Policy as ComplianceIcon,
  Settings as SettingsIcon,
  ExpandLess,
  ExpandMore,
  CheckCircle as CheckInIcon,
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { RootState } from '../../store';

interface SidebarProps {
  open: boolean;
}

const Sidebar: React.FC<SidebarProps> = ({ open }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const { user } = useSelector((state: RootState) => state.auth);
  const [analyticsOpen, setAnalyticsOpen] = React.useState(false);

  const handleAnalyticsToggle = () => {
    setAnalyticsOpen(!analyticsOpen);
  };

  const isActive = (path: string) => {
    return location.pathname === path || location.pathname.startsWith(path + '/');
  };

  const hasRole = (roles: string[]) => {
    return user?.roles.some(role => roles.includes(role)) || false;
  };

  const menuItems = [
    {
      text: 'Dashboard',
      icon: <DashboardIcon />,
      path: '/dashboard',
      roles: ['employee', 'manager', 'hr', 'admin'],
    },
    {
      text: 'Wellness',
      icon: <WellnessIcon />,
      path: '/wellness/check-in',
      roles: ['employee', 'manager', 'hr', 'admin'],
    },
    {
      text: 'Wellness Chat',
      icon: <ChatIcon />,
      path: '/wellness/chat',
      roles: ['employee', 'manager', 'hr', 'admin'],
    },
    {
      text: 'Wellness History',
      icon: <HistoryIcon />,
      path: '/wellness/history',
      roles: ['employee', 'manager', 'hr', 'admin'],
    },
    {
      text: 'Resources',
      icon: <ResourcesIcon />,
      path: '/resources',
      roles: ['employee', 'manager', 'hr', 'admin'],
    },
  ];

  const analyticsItems = [
    {
      text: 'Analytics Overview',
      icon: <AnalyticsIcon />,
      path: '/analytics',
      roles: ['manager', 'hr', 'admin'],
    },
    {
      text: 'Team Analytics',
      icon: <TeamIcon />,
      path: '/analytics/team',
      roles: ['manager', 'hr', 'admin'],
    },
    {
      text: 'Organizational Health',
      icon: <OrgIcon />,
      path: '/analytics/organizational-health',
      roles: ['hr', 'admin'],
    },
    {
      text: 'Risk Assessment',
      icon: <RiskIcon />,
      path: '/analytics/risk-assessment',
      roles: ['hr', 'admin'],
    },
  ];

  const adminItems = [
    {
      text: 'Compliance',
      icon: <ComplianceIcon />,
      path: '/compliance',
      roles: ['hr', 'admin'],
    },
    {
      text: 'Settings',
      icon: <SettingsIcon />,
      path: '/settings',
      roles: ['admin'],
    },
  ];

  const drawerWidth = open ? 240 : 64;

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: drawerWidth,
          boxSizing: 'border-box',
          backgroundColor: '#f8f9fa',
          borderRight: '1px solid #e0e0e0',
          transition: 'width 0.3s ease',
          overflowX: 'hidden',
        },
      }}
    >
      <Box sx={{ overflow: 'auto', mt: 8 }}>
        <List>
          {/* Main Menu Items */}
          {menuItems.map((item) => {
            if (!hasRole(item.roles)) return null;
            
            return (
              <ListItem key={item.text} disablePadding>
                <ListItemButton
                  onClick={() => navigate(item.path)}
                  selected={isActive(item.path)}
                  sx={{
                    minHeight: 48,
                    justifyContent: open ? 'initial' : 'center',
                    px: 2.5,
                    '&.Mui-selected': {
                      backgroundColor: 'primary.light',
                      color: 'primary.main',
                      '&:hover': {
                        backgroundColor: 'primary.light',
                      },
                    },
                  }}
                >
                  <ListItemIcon
                    sx={{
                      minWidth: 0,
                      mr: open ? 3 : 'auto',
                      justifyContent: 'center',
                      color: isActive(item.path) ? 'primary.main' : 'inherit',
                    }}
                  >
                    {item.icon}
                  </ListItemIcon>
                  {open && (
                    <ListItemText
                      primary={item.text}
                      sx={{
                        '& .MuiListItemText-primary': {
                          fontWeight: isActive(item.path) ? 600 : 400,
                        },
                      }}
                    />
                  )}
                </ListItemButton>
              </ListItem>
            );
          })}

          {/* Analytics Section */}
          {hasRole(['manager', 'hr', 'admin']) && (
            <>
              <Divider sx={{ my: 1 }} />
              {open && (
                <Box sx={{ px: 2, py: 1 }}>
                  <Typography variant="caption" color="text.secondary" sx={{ fontWeight: 600 }}>
                    ANALYTICS
                  </Typography>
                </Box>
              )}
              
              <ListItem disablePadding>
                <ListItemButton
                  onClick={handleAnalyticsToggle}
                  sx={{
                    minHeight: 48,
                    justifyContent: open ? 'initial' : 'center',
                    px: 2.5,
                  }}
                >
                  <ListItemIcon
                    sx={{
                      minWidth: 0,
                      mr: open ? 3 : 'auto',
                      justifyContent: 'center',
                    }}
                  >
                    <AnalyticsIcon />
                  </ListItemIcon>
                  {open && (
                    <>
                      <ListItemText primary="Analytics" />
                      {analyticsOpen ? <ExpandLess /> : <ExpandMore />}
                    </>
                  )}
                </ListItemButton>
              </ListItem>

              <Collapse in={analyticsOpen && open} timeout="auto" unmountOnExit>
                <List component="div" disablePadding>
                  {analyticsItems.map((item) => {
                    if (!hasRole(item.roles)) return null;
                    
                    return (
                      <ListItem key={item.text} disablePadding>
                        <ListItemButton
                          onClick={() => navigate(item.path)}
                          selected={isActive(item.path)}
                          sx={{
                            pl: 4,
                            minHeight: 48,
                            '&.Mui-selected': {
                              backgroundColor: 'primary.light',
                              color: 'primary.main',
                              '&:hover': {
                                backgroundColor: 'primary.light',
                              },
                            },
                          }}
                        >
                          <ListItemIcon
                            sx={{
                              minWidth: 0,
                              mr: 3,
                              justifyContent: 'center',
                              color: isActive(item.path) ? 'primary.main' : 'inherit',
                            }}
                          >
                            {item.icon}
                          </ListItemIcon>
                          <ListItemText
                            primary={item.text}
                            sx={{
                              '& .MuiListItemText-primary': {
                                fontWeight: isActive(item.path) ? 600 : 400,
                                fontSize: '0.875rem',
                              },
                            }}
                          />
                        </ListItemButton>
                      </ListItem>
                    );
                  })}
                </List>
              </Collapse>
            </>
          )}

          {/* Admin Section */}
          {hasRole(['hr', 'admin']) && (
            <>
              <Divider sx={{ my: 1 }} />
              {open && (
                <Box sx={{ px: 2, py: 1 }}>
                  <Typography variant="caption" color="text.secondary" sx={{ fontWeight: 600 }}>
                    ADMINISTRATION
                  </Typography>
                </Box>
              )}
              
              {adminItems.map((item) => {
                if (!hasRole(item.roles)) return null;
                
                return (
                  <ListItem key={item.text} disablePadding>
                    <ListItemButton
                      onClick={() => navigate(item.path)}
                      selected={isActive(item.path)}
                      sx={{
                        minHeight: 48,
                        justifyContent: open ? 'initial' : 'center',
                        px: 2.5,
                        '&.Mui-selected': {
                          backgroundColor: 'primary.light',
                          color: 'primary.main',
                          '&:hover': {
                            backgroundColor: 'primary.light',
                          },
                        },
                      }}
                    >
                      <ListItemIcon
                        sx={{
                          minWidth: 0,
                          mr: open ? 3 : 'auto',
                          justifyContent: 'center',
                          color: isActive(item.path) ? 'primary.main' : 'inherit',
                        }}
                      >
                        {item.icon}
                      </ListItemIcon>
                      {open && (
                        <ListItemText
                          primary={item.text}
                          sx={{
                            '& .MuiListItemText-primary': {
                              fontWeight: isActive(item.path) ? 600 : 400,
                            },
                          }}
                        />
                      )}
                    </ListItemButton>
                  </ListItem>
                );
              })}
            </>
          )}
        </List>
      </Box>
    </Drawer>
  );
};

export default Sidebar;
