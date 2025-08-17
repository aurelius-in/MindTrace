import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Avatar,
  Button,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Switch,
  FormControlLabel,
  Chip,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Alert,
  Tabs,
  Tab,
  Paper,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  Person,
  Settings,
  Security,
  Notifications,
  PrivacyTip,
  Edit,
  Save,
  Cancel,
  Visibility,
  VisibilityOff,
  Email,
  Phone,
  LocationOn,
  Work,
  Psychology,
  Favorite,
  History,
  Assessment,
} from '@mui/icons-material';
import { useDispatch, useSelector } from 'react-redux';
import { format } from 'date-fns';

import { RootState } from '../../store';
import { updateUserProfile, updatePrivacySettings } from '../../store/slices/authSlice';
import { addNotification } from '../../store/slices/uiSlice';
import LoadingSpinner from '../../components/Common/LoadingSpinner';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

const TabPanel: React.FC<TabPanelProps> = ({ children, value, index, ...other }) => (
  <div
    role="tabpanel"
    hidden={value !== index}
    id={`profile-tabpanel-${index}`}
    aria-labelledby={`profile-tab-${index}`}
    {...other}
  >
    {value === index && <Box sx={{ pt: 3 }}>{children}</Box>}
  </div>
);

const Profile: React.FC = () => {
  const dispatch = useDispatch();
  const { user, isLoading } = useSelector((state: RootState) => state.auth);
  
  const [tabValue, setTabValue] = useState(0);
  const [isEditing, setIsEditing] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  
  // Profile form state
  const [profileData, setProfileData] = useState({
    firstName: user?.firstName || '',
    lastName: user?.lastName || '',
    email: user?.email || '',
    phone: user?.phone || '',
    department: user?.department || '',
    position: user?.position || '',
    location: user?.location || '',
    bio: user?.bio || '',
  });

  // Privacy settings state
  const [privacySettings, setPrivacySettings] = useState({
    dataSharing: user?.privacySettings?.dataSharing || false,
    analyticsParticipation: user?.privacySettings?.analyticsParticipation || true,
    wellnessTracking: user?.privacySettings?.wellnessTracking || true,
    notifications: user?.privacySettings?.notifications || true,
    emergencyContact: user?.privacySettings?.emergencyContact || false,
  });

  // Wellness preferences state
  const [wellnessPreferences, setWellnessPreferences] = useState({
    checkInFrequency: user?.wellnessPreferences?.checkInFrequency || 'daily',
    preferredResources: user?.wellnessPreferences?.preferredResources || [],
    communicationStyle: user?.wellnessPreferences?.communicationStyle || 'supportive',
    focusAreas: user?.wellnessPreferences?.focusAreas || [],
  });

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleProfileChange = (field: string, value: string) => {
    setProfileData(prev => ({
      ...prev,
      [field]: value,
    }));
  };

  const handlePrivacyChange = (field: string, value: boolean) => {
    setPrivacySettings(prev => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleWellnessChange = (field: string, value: any) => {
    setWellnessPreferences(prev => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleSaveProfile = async () => {
    try {
      await dispatch(updateUserProfile({
        ...profileData,
        privacySettings,
        wellnessPreferences,
      }));
      
      setIsEditing(false);
      dispatch(addNotification({
        type: 'success',
        title: 'Profile Updated',
        message: 'Your profile has been updated successfully.',
      }));
    } catch (error) {
      dispatch(addNotification({
        type: 'error',
        title: 'Update Failed',
        message: 'Failed to update profile. Please try again.',
      }));
    }
  };

  const handleCancelEdit = () => {
    setProfileData({
      firstName: user?.firstName || '',
      lastName: user?.lastName || '',
      email: user?.email || '',
      phone: user?.phone || '',
      department: user?.department || '',
      position: user?.position || '',
      location: user?.location || '',
      bio: user?.bio || '',
    });
    setIsEditing(false);
  };

  const focusAreas = [
    'Stress Management',
    'Work-Life Balance',
    'Mental Health',
    'Physical Wellness',
    'Social Connections',
    'Career Development',
    'Financial Wellness',
    'Sleep Quality',
  ];

  const resourceTypes = [
    'Meditation',
    'Exercise',
    'CBT Techniques',
    'Mindfulness',
    'Nutrition',
    'Sleep Hygiene',
    'Social Skills',
    'Time Management',
  ];

  if (isLoading) {
    return <LoadingSpinner message="Loading profile..." />;
  }

  return (
    <Box sx={{ p: 3, maxWidth: 1200, mx: 'auto' }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" sx={{ fontWeight: 600, color: 'primary.main' }}>
          Profile & Settings
        </Typography>
        
        {!isEditing ? (
          <Button
            variant="outlined"
            startIcon={<Edit />}
            onClick={() => setIsEditing(true)}
          >
            Edit Profile
          </Button>
        ) : (
          <Box sx={{ display: 'flex', gap: 1 }}>
            <Button
              variant="contained"
              startIcon={<Save />}
              onClick={handleSaveProfile}
            >
              Save Changes
            </Button>
            <Button
              variant="outlined"
              startIcon={<Cancel />}
              onClick={handleCancelEdit}
            >
              Cancel
            </Button>
          </Box>
        )}
      </Box>

      {/* Profile Header */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={3} alignItems="center">
            <Grid item>
              <Avatar
                sx={{
                  width: 80,
                  height: 80,
                  bgcolor: 'primary.main',
                  fontSize: '2rem',
                }}
              >
                {user?.firstName?.[0]}{user?.lastName?.[0]}
              </Avatar>
            </Grid>
            <Grid item xs>
              <Typography variant="h5" sx={{ fontWeight: 600 }}>
                {user?.firstName} {user?.lastName}
              </Typography>
              <Typography variant="body1" color="text.secondary">
                {user?.position} • {user?.department}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Member since {user?.createdAt ? format(new Date(user.createdAt), 'MMMM yyyy') : 'N/A'}
              </Typography>
            </Grid>
            <Grid item>
              <Chip
                label={user?.role || 'Employee'}
                color="primary"
                variant="outlined"
              />
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Tabs */}
      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={tabValue} onChange={handleTabChange} aria-label="profile tabs">
          <Tab label="Personal Info" icon={<Person />} />
          <Tab label="Wellness Preferences" icon={<Psychology />} />
          <Tab label="Privacy & Security" icon={<Security />} />
          <Tab label="Activity History" icon={<History />} />
        </Tabs>
      </Box>

      {/* Personal Info Tab */}
      <TabPanel value={tabValue} index={0}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={8}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  Personal Information
                </Typography>
                
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      label="First Name"
                      value={profileData.firstName}
                      onChange={(e) => handleProfileChange('firstName', e.target.value)}
                      disabled={!isEditing}
                      InputProps={{
                        startAdornment: <Person sx={{ mr: 1, color: 'text.secondary' }} />,
                      }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      label="Last Name"
                      value={profileData.lastName}
                      onChange={(e) => handleProfileChange('lastName', e.target.value)}
                      disabled={!isEditing}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      label="Email"
                      type="email"
                      value={profileData.email}
                      onChange={(e) => handleProfileChange('email', e.target.value)}
                      disabled={!isEditing}
                      InputProps={{
                        startAdornment: <Email sx={{ mr: 1, color: 'text.secondary' }} />,
                      }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      label="Phone"
                      value={profileData.phone}
                      onChange={(e) => handleProfileChange('phone', e.target.value)}
                      disabled={!isEditing}
                      InputProps={{
                        startAdornment: <Phone sx={{ mr: 1, color: 'text.secondary' }} />,
                      }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      label="Department"
                      value={profileData.department}
                      onChange={(e) => handleProfileChange('department', e.target.value)}
                      disabled={!isEditing}
                      InputProps={{
                        startAdornment: <Work sx={{ mr: 1, color: 'text.secondary' }} />,
                      }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      label="Position"
                      value={profileData.position}
                      onChange={(e) => handleProfileChange('position', e.target.value)}
                      disabled={!isEditing}
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      label="Location"
                      value={profileData.location}
                      onChange={(e) => handleProfileChange('location', e.target.value)}
                      disabled={!isEditing}
                      InputProps={{
                        startAdornment: <LocationOn sx={{ mr: 1, color: 'text.secondary' }} />,
                      }}
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      label="Bio"
                      multiline
                      rows={3}
                      value={profileData.bio}
                      onChange={(e) => handleProfileChange('bio', e.target.value)}
                      disabled={!isEditing}
                      placeholder="Tell us about yourself..."
                    />
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  Account Statistics
                </Typography>
                
                <List>
                  <ListItem>
                    <ListItemIcon>
                      <Assessment />
                    </ListItemIcon>
                    <ListItemText
                      primary="Wellness Check-ins"
                      secondary={`${user?.stats?.checkIns || 0} completed`}
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <Favorite />
                    </ListItemIcon>
                    <ListItemText
                      primary="Resources Accessed"
                      secondary={`${user?.stats?.resourcesAccessed || 0} resources`}
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <History />
                    </ListItemIcon>
                    <ListItemText
                      primary="Conversations"
                      secondary={`${user?.stats?.conversations || 0} sessions`}
                    />
                  </ListItem>
                </List>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Wellness Preferences Tab */}
      <TabPanel value={tabValue} index={1}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  Wellness Preferences
                </Typography>
                
                <FormControl fullWidth sx={{ mb: 2 }}>
                  <InputLabel>Check-in Frequency</InputLabel>
                  <Select
                    value={wellnessPreferences.checkInFrequency}
                    onChange={(e) => handleWellnessChange('checkInFrequency', e.target.value)}
                    disabled={!isEditing}
                    label="Check-in Frequency"
                  >
                    <MenuItem value="daily">Daily</MenuItem>
                    <MenuItem value="weekly">Weekly</MenuItem>
                    <MenuItem value="biweekly">Bi-weekly</MenuItem>
                    <MenuItem value="monthly">Monthly</MenuItem>
                  </Select>
                </FormControl>

                <FormControl fullWidth sx={{ mb: 2 }}>
                  <InputLabel>Communication Style</InputLabel>
                  <Select
                    value={wellnessPreferences.communicationStyle}
                    onChange={(e) => handleWellnessChange('communicationStyle', e.target.value)}
                    disabled={!isEditing}
                    label="Communication Style"
                  >
                    <MenuItem value="supportive">Supportive & Encouraging</MenuItem>
                    <MenuItem value="direct">Direct & Practical</MenuItem>
                    <MenuItem value="analytical">Analytical & Data-driven</MenuItem>
                    <MenuItem value="casual">Casual & Friendly</MenuItem>
                  </Select>
                </FormControl>

                <Typography variant="subtitle2" sx={{ mb: 1 }}>
                  Focus Areas
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
                  {focusAreas.map((area) => (
                    <Chip
                      key={area}
                      label={area}
                      variant={wellnessPreferences.focusAreas.includes(area) ? 'filled' : 'outlined'}
                      color={wellnessPreferences.focusAreas.includes(area) ? 'primary' : 'default'}
                      onClick={() => {
                        if (isEditing) {
                          const newAreas = wellnessPreferences.focusAreas.includes(area)
                            ? wellnessPreferences.focusAreas.filter(a => a !== area)
                            : [...wellnessPreferences.focusAreas, area];
                          handleWellnessChange('focusAreas', newAreas);
                        }
                      }}
                      sx={{ cursor: isEditing ? 'pointer' : 'default' }}
                    />
                  ))}
                </Box>

                <Typography variant="subtitle2" sx={{ mb: 1 }}>
                  Preferred Resource Types
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {resourceTypes.map((type) => (
                    <Chip
                      key={type}
                      label={type}
                      variant={wellnessPreferences.preferredResources.includes(type) ? 'filled' : 'outlined'}
                      color={wellnessPreferences.preferredResources.includes(type) ? 'primary' : 'default'}
                      onClick={() => {
                        if (isEditing) {
                          const newResources = wellnessPreferences.preferredResources.includes(type)
                            ? wellnessPreferences.preferredResources.filter(r => r !== type)
                            : [...wellnessPreferences.preferredResources, type];
                          handleWellnessChange('preferredResources', newResources);
                        }
                      }}
                      sx={{ cursor: isEditing ? 'pointer' : 'default' }}
                    />
                  ))}
                </Box>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  Privacy & Data Settings
                </Typography>
                
                <FormControlLabel
                  control={
                    <Switch
                      checked={privacySettings.wellnessTracking}
                      onChange={(e) => handlePrivacyChange('wellnessTracking', e.target.checked)}
                      disabled={!isEditing}
                    />
                  }
                  label="Enable Wellness Tracking"
                />
                
                <FormControlLabel
                  control={
                    <Switch
                      checked={privacySettings.analyticsParticipation}
                      onChange={(e) => handlePrivacyChange('analyticsParticipation', e.target.checked)}
                      disabled={!isEditing}
                    />
                  }
                  label="Participate in Analytics"
                />
                
                <FormControlLabel
                  control={
                    <Switch
                      checked={privacySettings.notifications}
                      onChange={(e) => handlePrivacyChange('notifications', e.target.checked)}
                      disabled={!isEditing}
                    />
                  }
                  label="Receive Notifications"
                />
                
                <FormControlLabel
                  control={
                    <Switch
                      checked={privacySettings.emergencyContact}
                      onChange={(e) => handlePrivacyChange('emergencyContact', e.target.checked)}
                      disabled={!isEditing}
                    />
                  }
                  label="Allow Emergency Contact"
                />
                
                <Divider sx={{ my: 2 }} />
                
                <Alert severity="info" sx={{ mb: 2 }}>
                  Your data is protected and anonymized. We never share personal information without your explicit consent.
                </Alert>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Privacy & Security Tab */}
      <TabPanel value={tabValue} index={2}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  Security Settings
                </Typography>
                
                <TextField
                  fullWidth
                  label="Current Password"
                  type={showPassword ? 'text' : 'password'}
                  sx={{ mb: 2 }}
                  InputProps={{
                    endAdornment: (
                      <IconButton
                        onClick={() => setShowPassword(!showPassword)}
                        edge="end"
                      >
                        {showPassword ? <VisibilityOff /> : <Visibility />}
                      </IconButton>
                    ),
                  }}
                />
                
                <TextField
                  fullWidth
                  label="New Password"
                  type="password"
                  sx={{ mb: 2 }}
                />
                
                <TextField
                  fullWidth
                  label="Confirm New Password"
                  type="password"
                  sx={{ mb: 2 }}
                />
                
                <Button
                  variant="contained"
                  color="primary"
                  fullWidth
                >
                  Update Password
                </Button>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  Data & Privacy
                </Typography>
                
                <List>
                  <ListItem>
                    <ListItemIcon>
                      <PrivacyTip />
                    </ListItemIcon>
                    <ListItemText
                      primary="Data Export"
                      secondary="Download your personal data"
                    />
                    <Button variant="outlined" size="small">
                      Export
                    </Button>
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <Security />
                    </ListItemIcon>
                    <ListItemText
                      primary="Account Deletion"
                      secondary="Permanently delete your account"
                    />
                    <Button variant="outlined" color="error" size="small">
                      Delete
                    </Button>
                  </ListItem>
                </List>
                
                <Alert severity="warning" sx={{ mt: 2 }}>
                  Account deletion is permanent and cannot be undone.
                </Alert>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Activity History Tab */}
      <TabPanel value={tabValue} index={3}>
        <Card>
          <CardContent>
            <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
              Recent Activity
            </Typography>
            
            <List>
              {user?.activityHistory?.map((activity, index) => (
                <ListItem key={index}>
                  <ListItemIcon>
                    {activity.type === 'checkin' && <Assessment />}
                    {activity.type === 'resource' && <Favorite />}
                    {activity.type === 'conversation' && <Psychology />}
                  </ListItemIcon>
                  <ListItemText
                    primary={activity.description}
                    secondary={activity.timestamp ? format(new Date(activity.timestamp), 'MMM dd, yyyy HH:mm') : 'N/A'}
                  />
                </ListItem>
              )) || (
                <ListItem>
                  <ListItemText
                    primary="No recent activity"
                    secondary="Your wellness activities will appear here"
                  />
                </ListItem>
              )}
            </List>
          </CardContent>
        </Card>
      </TabPanel>
    </Box>
  );
};

export default Profile;
