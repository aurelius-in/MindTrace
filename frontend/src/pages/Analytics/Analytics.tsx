import React, { useState, useEffect, useMemo } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Tabs,
  Tab,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  Button,
  IconButton,
  Tooltip,
  Alert,
  LinearProgress,
  Paper,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Avatar,
  Badge,
  Switch,
  FormControlLabel,
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  TrendingFlat,
  Refresh,
  Download,
  FilterList,
  Settings,
  Warning,
  CheckCircle,
  Error,
  Info,
  Analytics as AnalyticsIcon,
  Group,
  Business,
  Psychology,
  LocalHospital,
  FitnessCenter,
  EmojiEmotions,
  Work,
  Schedule,
  Star,
  Speed,
  Assessment,
  Timeline,
  PieChart as PieChartIcon,
  BarChart as BarChartIcon,
  ShowChart,
  BubbleChart,
  ScatterPlot,
} from '@mui/icons-material';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  AreaChart,
  Area,
  ScatterChart,
  Scatter,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  ComposedChart,
  Legend,
} from 'recharts';
import { useDispatch, useSelector } from 'react-redux';
import { format, subDays, startOfDay, endOfDay, parseISO } from 'date-fns';

import { RootState } from '../../store';
import { fetchOrganizationalHealth, fetchTeamAnalytics, fetchRiskAssessments } from '../../store/slices/analyticsSlice';
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
    id={`analytics-tabpanel-${index}`}
    aria-labelledby={`analytics-tab-${index}`}
    {...other}
  >
    {value === index && <Box sx={{ pt: 3 }}>{children}</Box>}
  </div>
);

const Analytics: React.FC = () => {
  const dispatch = useDispatch();
  const { user } = useSelector((state: RootState) => state.auth);
  const { organizationalHealth, teamAnalytics, riskAssessments, isLoading } = useSelector((state: RootState) => state.analytics);
  
  const [tabValue, setTabValue] = useState(0);
  const [timeframe, setTimeframe] = useState('30d');
  const [selectedTeam, setSelectedTeam] = useState('all');
  const [refreshInterval, setRefreshInterval] = useState(30000); // 30 seconds
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [showAdvancedMetrics, setShowAdvancedMetrics] = useState(false);

  const timeframes = [
    { value: '7d', label: 'Last 7 Days' },
    { value: '30d', label: 'Last 30 Days' },
    { value: '90d', label: 'Last 90 Days' },
    { value: '6m', label: 'Last 6 Months' },
    { value: '1y', label: 'Last Year' },
  ];

  const teams = [
    { id: 'all', name: 'All Teams', color: '#1976d2' },
    { id: 'engineering', name: 'Engineering', color: '#2196f3' },
    { id: 'marketing', name: 'Marketing', color: '#4caf50' },
    { id: 'sales', name: 'Sales', color: '#ff9800' },
    { id: 'hr', name: 'Human Resources', color: '#9c27b0' },
    { id: 'finance', name: 'Finance', color: '#f44336' },
  ];

  useEffect(() => {
    loadAnalyticsData();
  }, [timeframe, selectedTeam]);

  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (autoRefresh && refreshInterval > 0) {
      interval = setInterval(() => {
        loadAnalyticsData();
      }, refreshInterval);
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [autoRefresh, refreshInterval]);

  const loadAnalyticsData = async () => {
    setIsRefreshing(true);
    try {
      await Promise.all([
        dispatch(fetchOrganizationalHealth(timeframe)),
        dispatch(fetchTeamAnalytics(timeframe)),
        dispatch(fetchRiskAssessments({ timeframe })),
      ]);
    } catch (error) {
      dispatch(addNotification({
        type: 'error',
        title: 'Data Load Failed',
        message: 'Failed to load analytics data.',
      }));
    } finally {
      setIsRefreshing(false);
    }
  };

  // Generate mock data for demonstration
  const generateMockData = useMemo(() => {
    const days = timeframe === '7d' ? 7 : timeframe === '30d' ? 30 : timeframe === '90d' ? 90 : 180;
    const data = [];
    
    for (let i = days - 1; i >= 0; i--) {
      const date = subDays(new Date(), i);
      data.push({
        date: format(date, 'MMM dd'),
        wellnessScore: Math.round(70 + Math.random() * 20),
        stressLevel: Math.round(30 + Math.random() * 40),
        engagement: Math.round(60 + Math.random() * 30),
        productivity: Math.round(75 + Math.random() * 20),
        burnoutRisk: Math.round(10 + Math.random() * 30),
        workLifeBalance: Math.round(50 + Math.random() * 40),
        teamCollaboration: Math.round(65 + Math.random() * 25),
        checkIns: Math.round(20 + Math.random() * 30),
        conversations: Math.round(5 + Math.random() * 15),
        resourcesAccessed: Math.round(10 + Math.random() * 20),
      });
    }
    
    return data;
  }, [timeframe]);

  const generateTeamData = useMemo(() => {
    return teams.filter(team => team.id !== 'all').map(team => ({
      name: team.name,
      wellnessScore: Math.round(60 + Math.random() * 30),
      stressLevel: Math.round(25 + Math.random() * 45),
      engagement: Math.round(55 + Math.random() * 35),
      burnoutRisk: Math.round(8 + Math.random() * 32),
      memberCount: Math.round(8 + Math.random() * 12),
      avgCheckIns: Math.round(15 + Math.random() * 25),
      avgConversations: Math.round(3 + Math.random() * 12),
      color: team.color,
    }));
  }, []);

  const generateRiskData = useMemo(() => {
    const riskTypes = ['Burnout', 'Stress', 'Anxiety', 'Depression', 'Work-Life Imbalance'];
    return riskTypes.map(type => ({
      type,
      count: Math.round(5 + Math.random() * 20),
      severity: Math.round(1 + Math.random() * 4),
      trend: Math.random() > 0.5 ? 'increasing' : 'decreasing',
      color: `hsl(${Math.random() * 360}, 70%, 50%)`,
    }));
  }, []);

  const generateWellnessDistribution = useMemo(() => {
    return [
      { name: 'Excellent', value: 25, color: '#4caf50' },
      { name: 'Good', value: 35, color: '#8bc34a' },
      { name: 'Fair', value: 25, color: '#ffc107' },
      { name: 'Poor', value: 10, color: '#ff9800' },
      { name: 'Critical', value: 5, color: '#f44336' },
    ];
  }, []);

  const generateMetrics = useMemo(() => {
    return [
      {
        name: 'Overall Wellness Score',
        value: 78,
        unit: '/100',
        trend: 'up',
        change: 5.2,
        icon: <EmojiEmotions />,
        color: 'success.main',
      },
      {
        name: 'Average Stress Level',
        value: 42,
        unit: '/100',
        trend: 'down',
        change: -3.1,
        icon: <Psychology />,
        color: 'warning.main',
      },
      {
        name: 'Engagement Score',
        value: 73,
        unit: '/100',
        trend: 'up',
        change: 2.8,
        icon: <Group />,
        color: 'primary.main',
      },
      {
        name: 'Burnout Risk',
        value: 18,
        unit: '%',
        trend: 'down',
        change: -2.5,
        icon: <Warning />,
        color: 'error.main',
      },
      {
        name: 'Work-Life Balance',
        value: 68,
        unit: '/100',
        trend: 'up',
        change: 4.1,
        icon: <Work />,
        color: 'info.main',
      },
      {
        name: 'Team Collaboration',
        value: 81,
        unit: '/100',
        trend: 'stable',
        change: 0.3,
        icon: <Business />,
        color: 'secondary.main',
      },
    ];
  }, []);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleRefresh = () => {
    loadAnalyticsData();
  };

  const handleExport = () => {
    // Simulate data export
    dispatch(addNotification({
      type: 'success',
      title: 'Export Complete',
      message: 'Analytics data has been exported successfully.',
    }));
  };

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'up':
        return <TrendingUp color="success" />;
      case 'down':
        return <TrendingDown color="error" />;
      default:
        return <TrendingFlat color="action" />;
    }
  };

  const getTrendColor = (trend: string) => {
    switch (trend) {
      case 'up':
        return 'success.main';
      case 'down':
        return 'error.main';
      default:
        return 'text.secondary';
    }
  };

  if (isLoading) {
    return <LoadingSpinner message="Loading analytics data..." />;
  }

  return (
    <Box sx={{ p: 3, maxWidth: 1600, mx: 'auto' }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" sx={{ fontWeight: 600, color: 'primary.main' }}>
          Analytics Dashboard
        </Typography>
        
        <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
          <FormControlLabel
            control={
              <Switch
                checked={autoRefresh}
                onChange={(e) => setAutoRefresh(e.target.checked)}
                size="small"
              />
            }
            label="Auto Refresh"
          />
          
          <FormControl size="small" sx={{ minWidth: 120 }}>
            <InputLabel>Refresh Interval</InputLabel>
            <Select
              value={refreshInterval}
              onChange={(e) => setRefreshInterval(e.target.value as number)}
              label="Refresh Interval"
              disabled={!autoRefresh}
            >
              <MenuItem value={15000}>15 seconds</MenuItem>
              <MenuItem value={30000}>30 seconds</MenuItem>
              <MenuItem value={60000}>1 minute</MenuItem>
              <MenuItem value={300000}>5 minutes</MenuItem>
            </Select>
          </FormControl>
          
          <Button
            variant="outlined"
            startIcon={<Refresh />}
            onClick={handleRefresh}
            disabled={isRefreshing}
          >
            Refresh
          </Button>
          
          <Button
            variant="outlined"
            startIcon={<Download />}
            onClick={handleExport}
          >
            Export
          </Button>
        </Box>
      </Box>

      {/* Filters */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={3} alignItems="center">
            <Grid item xs={12} md={4}>
              <FormControl fullWidth>
                <InputLabel>Timeframe</InputLabel>
                <Select
                  value={timeframe}
                  onChange={(e) => setTimeframe(e.target.value)}
                  label="Timeframe"
                >
                  {timeframes.map((tf) => (
                    <MenuItem key={tf.value} value={tf.value}>
                      {tf.label}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12} md={4}>
              <FormControl fullWidth>
                <InputLabel>Team</InputLabel>
                <Select
                  value={selectedTeam}
                  onChange={(e) => setSelectedTeam(e.target.value)}
                  label="Team"
                >
                  {teams.map((team) => (
                    <MenuItem key={team.id} value={team.id}>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <Box
                          sx={{
                            width: 12,
                            height: 12,
                            borderRadius: '50%',
                            backgroundColor: team.color,
                            mr: 1,
                          }}
                        />
                        {team.name}
                      </Box>
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12} md={4}>
              <FormControlLabel
                control={
                  <Switch
                    checked={showAdvancedMetrics}
                    onChange={(e) => setShowAdvancedMetrics(e.target.checked)}
                  />
                }
                label="Show Advanced Metrics"
              />
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Key Metrics */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        {generateMetrics.map((metric) => (
          <Grid item xs={12} sm={6} md={4} lg={2} key={metric.name}>
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Avatar sx={{ bgcolor: metric.color, mr: 1 }}>
                    {metric.icon}
                  </Avatar>
                  <Typography variant="h6" sx={{ fontWeight: 600 }}>
                    {metric.value}{metric.unit}
                  </Typography>
                </Box>
                
                <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                  {metric.name}
                </Typography>
                
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  {getTrendIcon(metric.trend)}
                  <Typography
                    variant="body2"
                    sx={{ ml: 0.5, color: getTrendColor(metric.trend) }}
                  >
                    {metric.change > 0 ? '+' : ''}{metric.change}%
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Tabs */}
      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={tabValue} onChange={handleTabChange} aria-label="analytics tabs">
          <Tab label="Overview" />
          <Tab label="Team Analytics" />
          <Tab label="Trends" />
          <Tab label="Risk Assessment" />
          <Tab label="Predictive Insights" />
        </Tabs>
      </Box>

      {/* Overview Tab */}
      <TabPanel value={tabValue} index={0}>
        <Grid container spacing={3}>
          {/* Wellness Trends Chart */}
          <Grid item xs={12} lg={8}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                  Wellness Trends Over Time
                </Typography>
                
                <ResponsiveContainer width="100%" height={400}>
                  <ComposedChart data={generateMockData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <RechartsTooltip />
                    <Legend />
                    <Line
                      type="monotone"
                      dataKey="wellnessScore"
                      stroke="#4caf50"
                      strokeWidth={3}
                      name="Wellness Score"
                    />
                    <Line
                      type="monotone"
                      dataKey="stressLevel"
                      stroke="#ff9800"
                      strokeWidth={2}
                      name="Stress Level"
                    />
                    <Line
                      type="monotone"
                      dataKey="engagement"
                      stroke="#2196f3"
                      strokeWidth={2}
                      name="Engagement"
                    />
                  </ComposedChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>

          {/* Wellness Distribution */}
          <Grid item xs={12} lg={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                  Wellness Distribution
                </Typography>
                
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={generateWellnessDistribution}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {generateWellnessDistribution.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <RechartsTooltip />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>

          {/* Activity Metrics */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                  Activity Metrics
                </Typography>
                
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={generateMockData.slice(-7)}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <RechartsTooltip />
                    <Bar dataKey="checkIns" fill="#2196f3" name="Check-ins" />
                    <Bar dataKey="conversations" fill="#4caf50" name="Conversations" />
                    <Bar dataKey="resourcesAccessed" fill="#ff9800" name="Resources" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>

          {/* Performance Radar */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                  Performance Overview
                </Typography>
                
                <ResponsiveContainer width="100%" height={300}>
                  <RadarChart data={[
                    {
                      metric: 'Wellness',
                      value: 78,
                      fullMark: 100,
                    },
                    {
                      metric: 'Productivity',
                      value: 85,
                      fullMark: 100,
                    },
                    {
                      metric: 'Collaboration',
                      value: 81,
                      fullMark: 100,
                    },
                    {
                      metric: 'Work-Life Balance',
                      value: 68,
                      fullMark: 100,
                    },
                    {
                      metric: 'Engagement',
                      value: 73,
                      fullMark: 100,
                    },
                  ]}>
                    <PolarGrid />
                    <PolarAngleAxis dataKey="metric" />
                    <PolarRadiusAxis angle={90} domain={[0, 100]} />
                    <Radar
                      name="Current"
                      dataKey="value"
                      stroke="#2196f3"
                      fill="#2196f3"
                      fillOpacity={0.3}
                    />
                    <RechartsTooltip />
                  </RadarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Team Analytics Tab */}
      <TabPanel value={tabValue} index={1}>
        <Grid container spacing={3}>
          {/* Team Comparison */}
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                  Team Wellness Comparison
                </Typography>
                
                <ResponsiveContainer width="100%" height={400}>
                  <BarChart data={generateTeamData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <RechartsTooltip />
                    <Legend />
                    <Bar dataKey="wellnessScore" fill="#4caf50" name="Wellness Score" />
                    <Bar dataKey="engagement" fill="#2196f3" name="Engagement" />
                    <Bar dataKey="burnoutRisk" fill="#f44336" name="Burnout Risk" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>

          {/* Team Details */}
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                  Team Details
                </Typography>
                
                <Grid container spacing={2}>
                  {generateTeamData.map((team) => (
                    <Grid item xs={12} md={6} lg={4} key={team.name}>
                      <Paper sx={{ p: 2, border: `2px solid ${team.color}` }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                          <Avatar sx={{ bgcolor: team.color, mr: 2 }}>
                            <Group />
                          </Avatar>
                          <Box>
                            <Typography variant="h6" sx={{ fontWeight: 600 }}>
                              {team.name}
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                              {team.memberCount} members
                            </Typography>
                          </Box>
                        </Box>
                        
                        <Grid container spacing={1}>
                          <Grid item xs={6}>
                            <Typography variant="body2" color="text.secondary">
                              Wellness Score
                            </Typography>
                            <Typography variant="h6" color="success.main">
                              {team.wellnessScore}/100
                            </Typography>
                          </Grid>
                          <Grid item xs={6}>
                            <Typography variant="body2" color="text.secondary">
                              Burnout Risk
                            </Typography>
                            <Typography variant="h6" color="error.main">
                              {team.burnoutRisk}%
                            </Typography>
                          </Grid>
                          <Grid item xs={6}>
                            <Typography variant="body2" color="text.secondary">
                              Engagement
                            </Typography>
                            <Typography variant="h6" color="primary.main">
                              {team.engagement}/100
                            </Typography>
                          </Grid>
                          <Grid item xs={6}>
                            <Typography variant="body2" color="text.secondary">
                              Avg Check-ins
                            </Typography>
                            <Typography variant="h6">
                              {team.avgCheckIns}/week
                            </Typography>
                          </Grid>
                        </Grid>
                      </Paper>
                    </Grid>
                  ))}
                </Grid>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Trends Tab */}
      <TabPanel value={tabValue} index={2}>
        <Grid container spacing={3}>
          {/* Detailed Trends */}
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                  Detailed Wellness Trends
                </Typography>
                
                <ResponsiveContainer width="100%" height={500}>
                  <AreaChart data={generateMockData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <RechartsTooltip />
                    <Legend />
                    <Area
                      type="monotone"
                      dataKey="wellnessScore"
                      stackId="1"
                      stroke="#4caf50"
                      fill="#4caf50"
                      fillOpacity={0.6}
                      name="Wellness Score"
                    />
                    <Area
                      type="monotone"
                      dataKey="productivity"
                      stackId="1"
                      stroke="#2196f3"
                      fill="#2196f3"
                      fillOpacity={0.6}
                      name="Productivity"
                    />
                    <Area
                      type="monotone"
                      dataKey="workLifeBalance"
                      stackId="1"
                      stroke="#ff9800"
                      fill="#ff9800"
                      fillOpacity={0.6}
                      name="Work-Life Balance"
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>

          {/* Correlation Analysis */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                  Stress vs. Productivity Correlation
                </Typography>
                
                <ResponsiveContainer width="100%" height={300}>
                  <ScatterChart data={generateMockData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="number" dataKey="stressLevel" name="Stress Level" />
                    <YAxis type="number" dataKey="productivity" name="Productivity" />
                    <RechartsTooltip cursor={{ strokeDasharray: '3 3' }} />
                    <Scatter name="Data Points" data={generateMockData} fill="#8884d8" />
                  </ScatterChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>

          {/* Trend Analysis */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                  Trend Analysis
                </Typography>
                
                <List>
                  <ListItem>
                    <ListItemIcon>
                      <TrendingUp color="success" />
                    </ListItemIcon>
                    <ListItemText
                      primary="Wellness Score"
                      secondary="Improving by 5.2% over the last 30 days"
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <TrendingDown color="error" />
                    </ListItemIcon>
                    <ListItemText
                      primary="Stress Levels"
                      secondary="Decreasing by 3.1% over the last 30 days"
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <TrendingUp color="success" />
                    </ListItemIcon>
                    <ListItemText
                      primary="Engagement"
                      secondary="Improving by 2.8% over the last 30 days"
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <TrendingDown color="success" />
                    </ListItemIcon>
                    <ListItemText
                      primary="Burnout Risk"
                      secondary="Decreasing by 2.5% over the last 30 days"
                    />
                  </ListItem>
                </List>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Risk Assessment Tab */}
      <TabPanel value={tabValue} index={3}>
        <Grid container spacing={3}>
          {/* Risk Overview */}
          <Grid item xs={12} md={8}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                  Risk Assessment Overview
                </Typography>
                
                <ResponsiveContainer width="100%" height={400}>
                  <BarChart data={generateRiskData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="type" />
                    <YAxis />
                    <RechartsTooltip />
                    <Bar dataKey="count" fill="#f44336" name="Risk Count" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>

          {/* Risk Details */}
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                  Risk Details
                </Typography>
                
                <List>
                  {generateRiskData.map((risk) => (
                    <ListItem key={risk.type}>
                      <ListItemIcon>
                        <Warning color="error" />
                      </ListItemIcon>
                      <ListItemText
                        primary={risk.type}
                        secondary={`${risk.count} cases, Severity: ${risk.severity}/5`}
                      />
                      <Chip
                        label={risk.trend}
                        color={risk.trend === 'increasing' ? 'error' : 'success'}
                        size="small"
                      />
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </Card>
          </Grid>

          {/* Risk Trends */}
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                  Risk Trends Over Time
                </Typography>
                
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={generateMockData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <RechartsTooltip />
                    <Legend />
                    <Line
                      type="monotone"
                      dataKey="burnoutRisk"
                      stroke="#f44336"
                      strokeWidth={3}
                      name="Burnout Risk"
                    />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Predictive Insights Tab */}
      <TabPanel value={tabValue} index={4}>
        <Grid container spacing={3}>
          {/* Predictive Models */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                  Predictive Insights
                </Typography>
                
                <Alert severity="info" sx={{ mb: 2 }}>
                  Based on current trends and patterns, here are our predictions for the next 30 days:
                </Alert>
                
                <List>
                  <ListItem>
                    <ListItemIcon>
                      <TrendingUp color="success" />
                    </ListItemIcon>
                    <ListItemText
                      primary="Wellness Score"
                      secondary="Predicted to improve by 3-5% in the next 30 days"
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <TrendingDown color="success" />
                    </ListItemIcon>
                    <ListItemText
                      primary="Stress Levels"
                      secondary="Predicted to decrease by 2-4% in the next 30 days"
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <Warning color="warning" />
                    </ListItemIcon>
                    <ListItemText
                      primary="Burnout Risk"
                      secondary="Predicted to remain stable with slight decrease"
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <TrendingUp color="success" />
                    </ListItemIcon>
                    <ListItemText
                      primary="Engagement"
                      secondary="Predicted to improve by 2-3% in the next 30 days"
                    />
                  </ListItem>
                </List>
              </CardContent>
            </Card>
          </Grid>

          {/* Recommendations */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                  AI-Generated Recommendations
                </Typography>
                
                <List>
                  <ListItem>
                    <ListItemIcon>
                      <Star color="primary" />
                    </ListItemIcon>
                    <ListItemText
                      primary="Increase Wellness Check-ins"
                      secondary="Encourage more frequent check-ins to improve trend tracking"
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <Star color="primary" />
                    </ListItemIcon>
                    <ListItemText
                      primary="Focus on High-Risk Teams"
                      secondary="Engineering team shows elevated stress levels"
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <Star color="primary" />
                    </ListItemIcon>
                    <ListItemText
                      primary="Enhance Resource Accessibility"
                      secondary="Increase promotion of wellness resources"
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <Star color="primary" />
                    </ListItemIcon>
                    <ListItemText
                      primary="Implement Stress Management Programs"
                      secondary="Targeted programs for stress reduction"
                    />
                  </ListItem>
                </List>
              </CardContent>
            </Card>
          </Grid>

          {/* Confidence Metrics */}
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                  Model Confidence Metrics
                </Typography>
                
                <Grid container spacing={2}>
                  <Grid item xs={12} md={3}>
                    <Box sx={{ textAlign: 'center' }}>
                      <Typography variant="h4" color="success.main" sx={{ fontWeight: 600 }}>
                        87%
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Prediction Accuracy
                      </Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={12} md={3}>
                    <Box sx={{ textAlign: 'center' }}>
                      <Typography variant="h4" color="primary.main" sx={{ fontWeight: 600 }}>
                        92%
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Data Quality Score
                      </Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={12} md={3}>
                    <Box sx={{ textAlign: 'center' }}>
                      <Typography variant="h4" color="warning.main" sx={{ fontWeight: 600 }}>
                        78%
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Model Confidence
                      </Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={12} md={3}>
                    <Box sx={{ textAlign: 'center' }}>
                      <Typography variant="h4" color="info.main" sx={{ fontWeight: 600 }}>
                        95%
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        System Reliability
                      </Typography>
                    </Box>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>
    </Box>
  );
};

export default Analytics;
