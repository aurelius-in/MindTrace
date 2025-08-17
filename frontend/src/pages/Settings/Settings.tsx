import React, { useState } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Switch,
  FormControlLabel,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Button,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Alert,
  Tabs,
  Tab,
  Slider,
  Chip,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from '@mui/material';
import {
  Settings,
  Notifications,
  Security,
  Palette,
  Language,
  Accessibility,
  Storage,
  Speed,
  DataUsage,
  ExpandMore,
  Brightness4,
  Brightness7,
  VolumeUp,
  VolumeOff,
  Email,
  Phone,
  Chat,
  Warning,
  Info,
  CheckCircle,
} from '@mui/icons-material';
import { useDispatch, useSelector } from 'react-redux';

import { RootState } from '../../store';
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
    id={`settings-tabpanel-${index}`}
    aria-labelledby={`settings-tab-${index}`}
    {...other}
  >
    {value === index && <Box sx={{ pt: 3 }}>{children}</Box>}
  </div>
);

const Settings: React.FC = () => {
  const dispatch = useDispatch();
  const { user } = useSelector((state: RootState) => state.auth);
  
  const [tabValue, setTabValue] = useState(0);
  
  // Application settings
  const [appSettings, setAppSettings] = useState({
    theme: 'light',
    language: 'en',
    fontSize: 14,
    autoSave: true,
    animations: true,
    soundEffects: false,
    accessibilityMode: false,
  });

  // Notification settings
  const [notificationSettings, setNotificationSettings] = useState({
    emailNotifications: true,
    pushNotifications: true,
    smsNotifications: false,
    wellnessReminders: true,
    resourceRecommendations: true,
    weeklyReports: true,
    emergencyAlerts: true,
    marketingEmails: false,
  });

  // Privacy settings
  const [privacySettings, setPrivacySettings] = useState({
    dataCollection: true,
    analyticsSharing: true,
    thirdPartySharing: false,
    locationTracking: false,
    personalizedAds: false,
    dataRetention: '1year',
  });

  // Performance settings
  const [performanceSettings, setPerformanceSettings] = useState({
    cacheSize: 100,
    autoRefresh: true,
    backgroundSync: true,
    dataCompression: true,
    imageOptimization: true,
  });

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleAppSettingChange = (field: string, value: any) => {
    setAppSettings(prev => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleNotificationChange = (field: string, value: boolean) => {
    setNotificationSettings(prev => ({
      ...prev,
      [field]: value,
    }));
  };

  const handlePrivacyChange = (field: string, value: any) => {
    setPrivacySettings(prev => ({
      ...prev,
      [field]: value,
    }));
  };

  const handlePerformanceChange = (field: string, value: any) => {
    setPerformanceSettings(prev => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleSaveSettings = () => {
    // Simulate saving settings
    dispatch(addNotification({
      type: 'success',
      title: 'Settings Saved',
      message: 'Your settings have been updated successfully.',
    }));
  };

  const handleResetSettings = () => {
    // Reset to defaults
    setAppSettings({
      theme: 'light',
      language: 'en',
      fontSize: 14,
      autoSave: true,
      animations: true,
      soundEffects: false,
      accessibilityMode: false,
    });
    
    setNotificationSettings({
      emailNotifications: true,
      pushNotifications: true,
      smsNotifications: false,
      wellnessReminders: true,
      resourceRecommendations: true,
      weeklyReports: true,
      emergencyAlerts: true,
      marketingEmails: false,
    });
    
    dispatch(addNotification({
      type: 'info',
      title: 'Settings Reset',
      message: 'Settings have been reset to default values.',
    }));
  };

  return (
    <Box sx={{ p: 3, maxWidth: 1200, mx: 'auto' }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" sx={{ fontWeight: 600, color: 'primary.main' }}>
          Application Settings
        </Typography>
        
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button
            variant="outlined"
            onClick={handleResetSettings}
          >
            Reset to Defaults
          </Button>
          <Button
            variant="contained"
            onClick={handleSaveSettings}
          >
            Save Settings
          </Button>
        </Box>
      </Box>

      {/* Tabs */}
      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={tabValue} onChange={handleTabChange} aria-label="settings tabs">
          <Tab label="General" icon={<Settings />} />
          <Tab label="Notifications" icon={<Notifications />} />
          <Tab label="Privacy" icon={<Security />} />
          <Tab label="Performance" icon={<Speed />} />
        </Tabs>
      </Box>

      {/* General Settings Tab */}
      <TabPanel value={tabValue} index={0}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  Appearance & Interface
                </Typography>
                
                <FormControl fullWidth sx={{ mb: 2 }}>
                  <InputLabel>Theme</InputLabel>
                  <Select
                    value={appSettings.theme}
                    onChange={(e) => handleAppSettingChange('theme', e.target.value)}
                    label="Theme"
                  >
                    <MenuItem value="light">
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <Brightness7 sx={{ mr: 1 }} />
                        Light
                      </Box>
                    </MenuItem>
                    <MenuItem value="dark">
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <Brightness4 sx={{ mr: 1 }} />
                        Dark
                      </Box>
                    </MenuItem>
                    <MenuItem value="auto">Auto (System)</MenuItem>
                  </Select>
                </FormControl>

                <FormControl fullWidth sx={{ mb: 2 }}>
                  <InputLabel>Language</InputLabel>
                  <Select
                    value={appSettings.language}
                    onChange={(e) => handleAppSettingChange('language', e.target.value)}
                    label="Language"
                  >
                    <MenuItem value="en">English</MenuItem>
                    <MenuItem value="es">Español</MenuItem>
                    <MenuItem value="fr">Français</MenuItem>
                    <MenuItem value="de">Deutsch</MenuItem>
                    <MenuItem value="zh">中文</MenuItem>
                    <MenuItem value="ja">日本語</MenuItem>
                  </Select>
                </FormControl>

                <Typography variant="subtitle2" sx={{ mb: 1 }}>
                  Font Size: {appSettings.fontSize}px
                </Typography>
                <Slider
                  value={appSettings.fontSize}
                  onChange={(_, value) => handleAppSettingChange('fontSize', value)}
                  min={12}
                  max={20}
                  step={1}
                  marks
                  valueLabelDisplay="auto"
                  sx={{ mb: 3 }}
                />

                <FormControlLabel
                  control={
                    <Switch
                      checked={appSettings.animations}
                      onChange={(e) => handleAppSettingChange('animations', e.target.checked)}
                    />
                  }
                  label="Enable Animations"
                />
                
                <FormControlLabel
                  control={
                    <Switch
                      checked={appSettings.soundEffects}
                      onChange={(e) => handleAppSettingChange('soundEffects', e.target.checked)}
                    />
                  }
                  label="Sound Effects"
                />
                
                <FormControlLabel
                  control={
                    <Switch
                      checked={appSettings.accessibilityMode}
                      onChange={(e) => handleAppSettingChange('accessibilityMode', e.target.checked)}
                    />
                  }
                  label="Accessibility Mode"
                />
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  Application Behavior
                </Typography>
                
                <FormControlLabel
                  control={
                    <Switch
                      checked={appSettings.autoSave}
                      onChange={(e) => handleAppSettingChange('autoSave', e.target.checked)}
                    />
                  }
                  label="Auto-save Progress"
                />
                
                <Divider sx={{ my: 2 }} />
                
                <Typography variant="subtitle2" sx={{ mb: 2 }}>
                  Quick Actions
                </Typography>
                
                <List dense>
                  <ListItem>
                    <ListItemIcon>
                      <Storage />
                    </ListItemIcon>
                    <ListItemText
                      primary="Clear Cache"
                      secondary="Free up storage space"
                    />
                    <Button variant="outlined" size="small">
                      Clear
                    </Button>
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <DataUsage />
                    </ListItemIcon>
                    <ListItemText
                      primary="Data Usage"
                      secondary="View data consumption"
                    />
                    <Button variant="outlined" size="small">
                      View
                    </Button>
                  </ListItem>
                </List>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Notifications Tab */}
      <TabPanel value={tabValue} index={1}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  Notification Channels
                </Typography>
                
                <FormControlLabel
                  control={
                    <Switch
                      checked={notificationSettings.emailNotifications}
                      onChange={(e) => handleNotificationChange('emailNotifications', e.target.checked)}
                    />
                  }
                  label={
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <Email sx={{ mr: 1 }} />
                      Email Notifications
                    </Box>
                  }
                />
                
                <FormControlLabel
                  control={
                    <Switch
                      checked={notificationSettings.pushNotifications}
                      onChange={(e) => handleNotificationChange('pushNotifications', e.target.checked)}
                    />
                  }
                  label={
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <Notifications sx={{ mr: 1 }} />
                      Push Notifications
                    </Box>
                  }
                />
                
                <FormControlLabel
                  control={
                    <Switch
                      checked={notificationSettings.smsNotifications}
                      onChange={(e) => handleNotificationChange('smsNotifications', e.target.checked)}
                    />
                  }
                  label={
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <Phone sx={{ mr: 1 }} />
                      SMS Notifications
                    </Box>
                  }
                />
                
                <FormControlLabel
                  control={
                    <Switch
                      checked={notificationSettings.chatNotifications}
                      onChange={(e) => handleNotificationChange('chatNotifications', e.target.checked)}
                    />
                  }
                  label={
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <Chat sx={{ mr: 1 }} />
                      Chat Notifications
                    </Box>
                  }
                />
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  Notification Types
                </Typography>
                
                <FormControlLabel
                  control={
                    <Switch
                      checked={notificationSettings.wellnessReminders}
                      onChange={(e) => handleNotificationChange('wellnessReminders', e.target.checked)}
                    />
                  }
                  label="Wellness Check-in Reminders"
                />
                
                <FormControlLabel
                  control={
                    <Switch
                      checked={notificationSettings.resourceRecommendations}
                      onChange={(e) => handleNotificationChange('resourceRecommendations', e.target.checked)}
                    />
                  }
                  label="Resource Recommendations"
                />
                
                <FormControlLabel
                  control={
                    <Switch
                      checked={notificationSettings.weeklyReports}
                      onChange={(e) => handleNotificationChange('weeklyReports', e.target.checked)}
                    />
                  }
                  label="Weekly Wellness Reports"
                />
                
                <FormControlLabel
                  control={
                    <Switch
                      checked={notificationSettings.emergencyAlerts}
                      onChange={(e) => handleNotificationChange('emergencyAlerts', e.target.checked)}
                    />
                  }
                  label="Emergency Alerts"
                />
                
                <FormControlLabel
                  control={
                    <Switch
                      checked={notificationSettings.marketingEmails}
                      onChange={(e) => handleNotificationChange('marketingEmails', e.target.checked)}
                    />
                  }
                  label="Marketing Communications"
                />
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  Notification Schedule
                </Typography>
                
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6} md={3}>
                    <FormControl fullWidth>
                      <InputLabel>Wellness Reminders</InputLabel>
                      <Select
                        value="daily"
                        label="Wellness Reminders"
                      >
                        <MenuItem value="daily">Daily</MenuItem>
                        <MenuItem value="weekly">Weekly</MenuItem>
                        <MenuItem value="biweekly">Bi-weekly</MenuItem>
                        <MenuItem value="monthly">Monthly</MenuItem>
                      </Select>
                    </FormControl>
                  </Grid>
                  <Grid item xs={12} sm={6} md={3}>
                    <FormControl fullWidth>
                      <InputLabel>Report Frequency</InputLabel>
                      <Select
                        value="weekly"
                        label="Report Frequency"
                      >
                        <MenuItem value="daily">Daily</MenuItem>
                        <MenuItem value="weekly">Weekly</MenuItem>
                        <MenuItem value="monthly">Monthly</MenuItem>
                      </Select>
                    </FormControl>
                  </Grid>
                  <Grid item xs={12} sm={6} md={3}>
                    <TextField
                      fullWidth
                      label="Quiet Hours Start"
                      type="time"
                      defaultValue="22:00"
                    />
                  </Grid>
                  <Grid item xs={12} sm={6} md={3}>
                    <TextField
                      fullWidth
                      label="Quiet Hours End"
                      type="time"
                      defaultValue="08:00"
                    />
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Privacy Tab */}
      <TabPanel value={tabValue} index={2}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  Data Collection & Usage
                </Typography>
                
                <FormControlLabel
                  control={
                    <Switch
                      checked={privacySettings.dataCollection}
                      onChange={(e) => handlePrivacyChange('dataCollection', e.target.checked)}
                    />
                  }
                  label="Allow Data Collection"
                />
                
                <FormControlLabel
                  control={
                    <Switch
                      checked={privacySettings.analyticsSharing}
                      onChange={(e) => handlePrivacyChange('analyticsSharing', e.target.checked)}
                    />
                  }
                  label="Share Analytics Data"
                />
                
                <FormControlLabel
                  control={
                    <Switch
                      checked={privacySettings.thirdPartySharing}
                      onChange={(e) => handlePrivacyChange('thirdPartySharing', e.target.checked)}
                    />
                  }
                  label="Third-party Data Sharing"
                />
                
                <FormControlLabel
                  control={
                    <Switch
                      checked={privacySettings.locationTracking}
                      onChange={(e) => handlePrivacyChange('locationTracking', e.target.checked)}
                    />
                  }
                  label="Location Tracking"
                />
                
                <FormControlLabel
                  control={
                    <Switch
                      checked={privacySettings.personalizedAds}
                      onChange={(e) => handlePrivacyChange('personalizedAds', e.target.checked)}
                    />
                  }
                  label="Personalized Recommendations"
                />
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  Data Retention
                </Typography>
                
                <FormControl fullWidth sx={{ mb: 2 }}>
                  <InputLabel>Data Retention Period</InputLabel>
                  <Select
                    value={privacySettings.dataRetention}
                    onChange={(e) => handlePrivacyChange('dataRetention', e.target.value)}
                    label="Data Retention Period"
                  >
                    <MenuItem value="30days">30 Days</MenuItem>
                    <MenuItem value="6months">6 Months</MenuItem>
                    <MenuItem value="1year">1 Year</MenuItem>
                    <MenuItem value="3years">3 Years</MenuItem>
                    <MenuItem value="indefinite">Indefinite</MenuItem>
                  </Select>
                </FormControl>
                
                <Alert severity="info" sx={{ mb: 2 }}>
                  Your data is encrypted and stored securely. You can request data deletion at any time.
                </Alert>
                
                <Button
                  variant="outlined"
                  color="primary"
                  fullWidth
                  sx={{ mb: 1 }}
                >
                  Download My Data
                </Button>
                
                <Button
                  variant="outlined"
                  color="error"
                  fullWidth
                >
                  Delete My Data
                </Button>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Performance Tab */}
      <TabPanel value={tabValue} index={3}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  Performance Optimization
                </Typography>
                
                <Typography variant="subtitle2" sx={{ mb: 1 }}>
                  Cache Size: {performanceSettings.cacheSize}MB
                </Typography>
                <Slider
                  value={performanceSettings.cacheSize}
                  onChange={(_, value) => handlePerformanceChange('cacheSize', value)}
                  min={50}
                  max={500}
                  step={50}
                  marks
                  valueLabelDisplay="auto"
                  sx={{ mb: 3 }}
                />
                
                <FormControlLabel
                  control={
                    <Switch
                      checked={performanceSettings.autoRefresh}
                      onChange={(e) => handlePerformanceChange('autoRefresh', e.target.checked)}
                    />
                  }
                  label="Auto-refresh Data"
                />
                
                <FormControlLabel
                  control={
                    <Switch
                      checked={performanceSettings.backgroundSync}
                      onChange={(e) => handlePerformanceChange('backgroundSync', e.target.checked)}
                    />
                  }
                  label="Background Sync"
                />
                
                <FormControlLabel
                  control={
                    <Switch
                      checked={performanceSettings.dataCompression}
                      onChange={(e) => handlePerformanceChange('dataCompression', e.target.checked)}
                    />
                  }
                  label="Data Compression"
                />
                
                <FormControlLabel
                  control={
                    <Switch
                      checked={performanceSettings.imageOptimization}
                      onChange={(e) => handlePerformanceChange('imageOptimization', e.target.checked)}
                    />
                  }
                  label="Image Optimization"
                />
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  System Status
                </Typography>
                
                <List>
                  <ListItem>
                    <ListItemIcon>
                      <CheckCircle color="success" />
                    </ListItemIcon>
                    <ListItemText
                      primary="Database Connection"
                      secondary="Connected and responsive"
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <CheckCircle color="success" />
                    </ListItemIcon>
                    <ListItemText
                      primary="AI Services"
                      secondary="All agents operational"
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <CheckCircle color="success" />
                    </ListItemIcon>
                    <ListItemText
                      primary="Analytics Engine"
                      secondary="Processing data normally"
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <Info color="info" />
                    </ListItemIcon>
                    <ListItemText
                      primary="Cache Status"
                      secondary={`${performanceSettings.cacheSize}MB allocated`}
                    />
                  </ListItem>
                </List>
                
                <Divider sx={{ my: 2 }} />
                
                <Button
                  variant="outlined"
                  fullWidth
                  sx={{ mb: 1 }}
                >
                  Run System Diagnostics
                </Button>
                
                <Button
                  variant="outlined"
                  fullWidth
                >
                  Clear All Caches
                </Button>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>
    </Box>
  );
};

export default Settings;
