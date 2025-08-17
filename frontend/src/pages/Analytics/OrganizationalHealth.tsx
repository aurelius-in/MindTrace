import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Chip,
  Button,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  LinearProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Tabs,
  Tab,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Switch,
  FormControlLabel,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Badge,
  Tooltip,
  IconButton,
  Divider,
  Avatar,
  Stack,
  Rating,
  Slider,
  Autocomplete,
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  CheckCircle,
  Error,
  Info,
  Assessment,
  Psychology,
  LocalHospital,
  Schedule,
  Person,
  Group,
  Timeline,
  Notifications,
  Visibility,
  Edit,
  ExpandMore,
  FilterList,
  Refresh,
  Download,
  Share,
  Settings,
  Add,
  Remove,
  Star,
  StarBorder,
  TrendingFlat,
  Speed,
  Timer,
  EmojiEvents,
  PsychologyAlt,
  HealthAndSafety,
  Work,
  School,
  FamilyRestroom,
  SportsEsports,
  Restaurant,
  Hotel,
  Business,
  CorporateFare,
  People,
  Leaderboard,
  Analytics,
  Insights,
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  TrendingFlat as TrendingFlatIcon,
} from '@mui/icons-material';
import { useDispatch, useSelector } from 'react-redux';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell, AreaChart, Area, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ComposedChart } from 'recharts';

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
    id={`org-health-tabpanel-${index}`}
    aria-labelledby={`org-health-tab-${index}`}
    {...other}
  >
    {value === index && <Box sx={{ pt: 3 }}>{children}</Box>}
  </div>
);

const OrganizationalHealth: React.FC = () => {
  const dispatch = useDispatch();
  const { user } = useSelector((state: RootState) => state.auth);
  
  const [tabValue, setTabValue] = useState(0);
  const [showFilters, setShowFilters] = useState(false);
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [selectedTimeframe, setSelectedTimeframe] = useState('3months');
  const [showAdvancedMetrics, setShowAdvancedMetrics] = useState(false);

  // Organizational health data
  const [orgHealthData, setOrgHealthData] = useState({
    overallScore: 78,
    lastUpdated: '2024-01-25',
    trends: {
      employeeSatisfaction: 'improving',
      retention: 'stable',
      productivity: 'improving',
      innovation: 'stable',
      collaboration: 'improving',
      workLifeBalance: 'stable',
    },
    kpis: [
      {
        id: 1,
        name: 'Employee Satisfaction',
        value: 82,
        target: 85,
        trend: 'improving',
        category: 'Engagement',
        description: 'Overall employee satisfaction score based on surveys and feedback',
        impact: 'High'
      },
      {
        id: 2,
        name: 'Retention Rate',
        value: 94,
        target: 90,
        trend: 'stable',
        category: 'Retention',
        description: 'Percentage of employees retained over the past 12 months',
        impact: 'High'
      },
      {
        id: 3,
        name: 'Productivity Index',
        value: 87,
        target: 85,
        trend: 'improving',
        category: 'Performance',
        description: 'Overall productivity score based on output and efficiency metrics',
        impact: 'High'
      },
      {
        id: 4,
        name: 'Innovation Score',
        value: 75,
        target: 80,
        trend: 'stable',
        category: 'Innovation',
        description: 'Innovation and creativity metrics across teams',
        impact: 'Medium'
      },
      {
        id: 5,
        name: 'Collaboration Index',
        value: 79,
        target: 85,
        trend: 'improving',
        category: 'Culture',
        description: 'Cross-team collaboration and communication effectiveness',
        impact: 'Medium'
      },
      {
        id: 6,
        name: 'Work-Life Balance',
        value: 73,
        target: 80,
        trend: 'stable',
        category: 'Wellness',
        description: 'Employee work-life balance satisfaction score',
        impact: 'High'
      }
    ],
    departments: [
      {
        name: 'Engineering',
        satisfaction: 85,
        retention: 96,
        productivity: 90,
        innovation: 88,
        collaboration: 82,
        workLifeBalance: 75
      },
      {
        name: 'Sales',
        satisfaction: 78,
        retention: 92,
        productivity: 85,
        innovation: 70,
        collaboration: 75,
        workLifeBalance: 70
      },
      {
        name: 'Marketing',
        satisfaction: 80,
        retention: 94,
        productivity: 88,
        innovation: 85,
        collaboration: 88,
        workLifeBalance: 78
      },
      {
        name: 'HR',
        satisfaction: 88,
        retention: 98,
        productivity: 82,
        innovation: 75,
        collaboration: 90,
        workLifeBalance: 85
      },
      {
        name: 'Finance',
        satisfaction: 75,
        retention: 90,
        productivity: 92,
        innovation: 65,
        collaboration: 70,
        workLifeBalance: 72
      }
    ],
    initiatives: [
      {
        id: 1,
        name: 'Employee Wellness Program',
        status: 'active',
        impact: 'high',
        progress: 85,
        description: 'Comprehensive wellness program including mental health support',
        participants: 450,
        satisfaction: 92
      },
      {
        id: 2,
        name: 'Flexible Work Arrangements',
        status: 'active',
        impact: 'high',
        progress: 95,
        description: 'Remote work and flexible hours implementation',
        participants: 380,
        satisfaction: 88
      },
      {
        id: 3,
        name: 'Professional Development',
        status: 'active',
        impact: 'medium',
        progress: 70,
        description: 'Training and career development opportunities',
        participants: 320,
        satisfaction: 85
      },
      {
        id: 4,
        name: 'Team Building Activities',
        status: 'active',
        impact: 'medium',
        progress: 60,
        description: 'Regular team building and social events',
        participants: 280,
        satisfaction: 78
      }
    ]
  });

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'improving': return <TrendingUpIcon color="success" />;
      case 'declining': return <TrendingDownIcon color="error" />;
      case 'stable': return <TrendingFlatIcon color="info" />;
      default: return <Info color="info" />;
    }
  };

  const getTrendLabel = (trend: string) => {
    switch (trend) {
      case 'improving': return 'Improving';
      case 'declining': return 'Declining';
      case 'stable': return 'Stable';
      default: return 'Unknown';
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 85) return 'success';
    if (score >= 70) return 'warning';
    return 'error';
  };

  // Chart data
  const orgHealthTrendData = [
    { month: 'Oct', satisfaction: 78, retention: 92, productivity: 82, innovation: 72, collaboration: 75, workLifeBalance: 70 },
    { month: 'Nov', satisfaction: 79, retention: 93, productivity: 84, innovation: 73, collaboration: 76, workLifeBalance: 71 },
    { month: 'Dec', satisfaction: 80, retention: 93, productivity: 85, innovation: 74, collaboration: 77, workLifeBalance: 72 },
    { month: 'Jan', satisfaction: 82, retention: 94, productivity: 87, innovation: 75, collaboration: 79, workLifeBalance: 73 },
  ];

  const kpiRadarData = [
    { metric: 'Satisfaction', value: 82, fullMark: 100 },
    { metric: 'Retention', value: 94, fullMark: 100 },
    { metric: 'Productivity', value: 87, fullMark: 100 },
    { metric: 'Innovation', value: 75, fullMark: 100 },
    { metric: 'Collaboration', value: 79, fullMark: 100 },
    { metric: 'Work-Life Balance', value: 73, fullMark: 100 },
  ];

  const departmentComparisonData = orgHealthData.departments.map(dept => ({
    department: dept.name,
    overall: Math.round((dept.satisfaction + dept.retention + dept.productivity + dept.innovation + dept.collaboration + dept.workLifeBalance) / 6),
    satisfaction: dept.satisfaction,
    retention: dept.retention,
    productivity: dept.productivity,
  }));

  return (
    <Box sx={{ p: 3, maxWidth: 1400, mx: 'auto' }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" sx={{ fontWeight: 600, color: 'primary.main' }}>
          Organizational Health Dashboard
        </Typography>
        
        <Stack direction="row" spacing={2}>
          <Tooltip title="Refresh Data">
            <IconButton onClick={() => dispatch(addNotification({ message: 'Data refreshed', type: 'success' }))}>
              <Refresh />
            </IconButton>
          </Tooltip>
          
          <Tooltip title="Export Report">
            <IconButton onClick={() => dispatch(addNotification({ message: 'Report exported', type: 'success' }))}>
              <Download />
            </IconButton>
          </Tooltip>
          
          <Tooltip title="Share Dashboard">
            <IconButton onClick={() => dispatch(addNotification({ message: 'Dashboard shared', type: 'success' }))}>
              <Share />
            </IconButton>
          </Tooltip>
          
          <Tooltip title="Settings">
            <IconButton onClick={() => setShowFilters(!showFilters)}>
              <Settings />
            </IconButton>
          </Tooltip>
        </Stack>
      </Box>

      {/* Control Panel */}
      <Accordion expanded={showFilters} onChange={() => setShowFilters(!showFilters)} sx={{ mb: 3 }}>
        <AccordionSummary expandIcon={<ExpandMore />}>
          <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center' }}>
            <FilterList sx={{ mr: 1 }} />
            Filters & Settings
          </Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Grid container spacing={3}>
            <Grid item xs={12} md={4}>
              <FormControl fullWidth>
                <InputLabel>Timeframe</InputLabel>
                <Select
                  value={selectedTimeframe}
                  onChange={(e) => setSelectedTimeframe(e.target.value)}
                  label="Timeframe"
                >
                  <MenuItem value="1month">Last Month</MenuItem>
                  <MenuItem value="3months">Last 3 Months</MenuItem>
                  <MenuItem value="6months">Last 6 Months</MenuItem>
                  <MenuItem value="1year">Last Year</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12} md={4}>
              <Stack spacing={2}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={autoRefresh}
                      onChange={(e) => setAutoRefresh(e.target.checked)}
                    />
                  }
                  label="Auto Refresh"
                />
                <FormControlLabel
                  control={
                    <Switch
                      checked={showAdvancedMetrics}
                      onChange={(e) => setShowAdvancedMetrics(e.target.checked)}
                    />
                  }
                  label="Advanced Metrics"
                />
              </Stack>
            </Grid>
            
            <Grid item xs={12} md={4}>
              <Typography variant="body2" gutterBottom>
                Last Updated: {new Date(orgHealthData.lastUpdated).toLocaleDateString()}
              </Typography>
              <Button
                variant="outlined"
                size="small"
                onClick={() => dispatch(addNotification({ message: 'Data updated', type: 'success' }))}
              >
                Update Now
              </Button>
            </Grid>
          </Grid>
        </AccordionDetails>
      </Accordion>

      {/* Overall Health Score */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Business sx={{ mr: 1, color: 'primary.main' }} />
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Overall Health Score
                </Typography>
              </Box>
              
              <Box sx={{ textAlign: 'center', mb: 2 }}>
                <Typography variant="h3" sx={{ fontWeight: 700, color: `${getScoreColor(orgHealthData.overallScore)}.main` }}>
                  {orgHealthData.overallScore}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  out of 100
                </Typography>
              </Box>
              
              <Chip
                label={orgHealthData.overallScore >= 85 ? 'Excellent' : orgHealthData.overallScore >= 70 ? 'Good' : 'Needs Improvement'}
                color={getScoreColor(orgHealthData.overallScore) as any}
                sx={{ fontWeight: 600 }}
              />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <TrendingUp sx={{ mr: 1, color: 'primary.main' }} />
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Key Trends
                </Typography>
              </Box>
              
              <List dense>
                {Object.entries(orgHealthData.trends).map(([key, trend]) => (
                  <ListItem key={key}>
                    <ListItemIcon>
                      {getTrendIcon(trend)}
                    </ListItemIcon>
                    <ListItemText
                      primary={key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}
                      secondary={getTrendLabel(trend)}
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <EmojiEvents sx={{ mr: 1, color: 'primary.main' }} />
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Top Performers
                </Typography>
              </Box>
              
              <List dense>
                <ListItem>
                  <ListItemIcon>
                    <Star color="warning" />
                  </ListItemIcon>
                  <ListItemText
                    primary="Engineering"
                    secondary="Health Score: 86"
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <Star color="warning" />
                  </ListItemIcon>
                  <ListItemText
                    primary="HR"
                    secondary="Health Score: 84"
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <Star color="warning" />
                  </ListItemIcon>
                  <ListItemText
                    primary="Marketing"
                    secondary="Health Score: 82"
                  />
                </ListItem>
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Tabs */}
      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={tabValue} onChange={handleTabChange} aria-label="organizational health tabs">
          <Tab label="KPIs & Metrics" />
          <Tab label="Department Analysis" />
          <Tab label="Trends & Insights" />
          <Tab label="Initiatives" />
          <Tab label="Advanced Analytics" />
        </Tabs>
      </Box>

      {/* KPIs & Metrics Tab */}
      <TabPanel value={tabValue} index={0}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  Key Performance Indicators
                </Typography>
                
                <TableContainer component={Paper}>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>KPI</TableCell>
                        <TableCell>Current Value</TableCell>
                        <TableCell>Target</TableCell>
                        <TableCell>Trend</TableCell>
                        <TableCell>Category</TableCell>
                        <TableCell>Impact</TableCell>
                        <TableCell>Actions</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {orgHealthData.kpis.map((kpi) => (
                        <TableRow key={kpi.id}>
                          <TableCell>
                            <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                              {kpi.name}
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                              {kpi.description}
                            </Typography>
                          </TableCell>
                          <TableCell>
                            <Box sx={{ display: 'flex', alignItems: 'center' }}>
                              <Box sx={{ width: '100%', mr: 1 }}>
                                <LinearProgress
                                  variant="determinate"
                                  value={kpi.value}
                                  color={getScoreColor(kpi.value) as any}
                                  sx={{ height: 8, borderRadius: 4 }}
                                />
                              </Box>
                              <Typography variant="body2">
                                {kpi.value}%
                              </Typography>
                            </Box>
                          </TableCell>
                          <TableCell>
                            <Typography variant="body2">
                              {kpi.target}%
                            </Typography>
                          </TableCell>
                          <TableCell>
                            <Box sx={{ display: 'flex', alignItems: 'center' }}>
                              {getTrendIcon(kpi.trend)}
                              <Typography variant="body2" sx={{ ml: 1 }}>
                                {getTrendLabel(kpi.trend)}
                              </Typography>
                            </Box>
                          </TableCell>
                          <TableCell>
                            <Chip
                              label={kpi.category}
                              size="small"
                              variant="outlined"
                            />
                          </TableCell>
                          <TableCell>
                            <Chip
                              label={kpi.impact}
                              color={kpi.impact === 'High' ? 'error' : 'warning'}
                              size="small"
                            />
                          </TableCell>
                          <TableCell>
                            <Button
                              variant="outlined"
                              size="small"
                            >
                              View Details
                            </Button>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Department Analysis Tab */}
      <TabPanel value={tabValue} index={1}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  Department Health Comparison
                </Typography>
                
                <TableContainer component={Paper}>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Department</TableCell>
                        <TableCell>Overall Score</TableCell>
                        <TableCell>Satisfaction</TableCell>
                        <TableCell>Retention</TableCell>
                        <TableCell>Productivity</TableCell>
                        <TableCell>Innovation</TableCell>
                        <TableCell>Collaboration</TableCell>
                        <TableCell>Work-Life Balance</TableCell>
                        <TableCell>Actions</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {orgHealthData.departments.map((dept) => {
                        const overallScore = Math.round((dept.satisfaction + dept.retention + dept.productivity + dept.innovation + dept.collaboration + dept.workLifeBalance) / 6);
                        return (
                          <TableRow key={dept.name}>
                            <TableCell>
                              <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                                {dept.name}
                              </Typography>
                            </TableCell>
                            <TableCell>
                              <Chip
                                label={`${overallScore}/100`}
                                color={getScoreColor(overallScore) as any}
                                sx={{ fontWeight: 600 }}
                              />
                            </TableCell>
                            <TableCell>
                              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                <Box sx={{ width: '100%', mr: 1 }}>
                                  <LinearProgress
                                    variant="determinate"
                                    value={dept.satisfaction}
                                    color={getScoreColor(dept.satisfaction) as any}
                                    sx={{ height: 8, borderRadius: 4 }}
                                  />
                                </Box>
                                <Typography variant="body2">{dept.satisfaction}%</Typography>
                              </Box>
                            </TableCell>
                            <TableCell>
                              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                <Box sx={{ width: '100%', mr: 1 }}>
                                  <LinearProgress
                                    variant="determinate"
                                    value={dept.retention}
                                    color={getScoreColor(dept.retention) as any}
                                    sx={{ height: 8, borderRadius: 4 }}
                                  />
                                </Box>
                                <Typography variant="body2">{dept.retention}%</Typography>
                              </Box>
                            </TableCell>
                            <TableCell>
                              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                <Box sx={{ width: '100%', mr: 1 }}>
                                  <LinearProgress
                                    variant="determinate"
                                    value={dept.productivity}
                                    color={getScoreColor(dept.productivity) as any}
                                    sx={{ height: 8, borderRadius: 4 }}
                                  />
                                </Box>
                                <Typography variant="body2">{dept.productivity}%</Typography>
                              </Box>
                            </TableCell>
                            <TableCell>
                              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                <Box sx={{ width: '100%', mr: 1 }}>
                                  <LinearProgress
                                    variant="determinate"
                                    value={dept.innovation}
                                    color={getScoreColor(dept.innovation) as any}
                                    sx={{ height: 8, borderRadius: 4 }}
                                  />
                                </Box>
                                <Typography variant="body2">{dept.innovation}%</Typography>
                              </Box>
                            </TableCell>
                            <TableCell>
                              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                <Box sx={{ width: '100%', mr: 1 }}>
                                  <LinearProgress
                                    variant="determinate"
                                    value={dept.collaboration}
                                    color={getScoreColor(dept.collaboration) as any}
                                    sx={{ height: 8, borderRadius: 4 }}
                                  />
                                </Box>
                                <Typography variant="body2">{dept.collaboration}%</Typography>
                              </Box>
                            </TableCell>
                            <TableCell>
                              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                <Box sx={{ width: '100%', mr: 1 }}>
                                  <LinearProgress
                                    variant="determinate"
                                    value={dept.workLifeBalance}
                                    color={getScoreColor(dept.workLifeBalance) as any}
                                    sx={{ height: 8, borderRadius: 4 }}
                                  />
                                </Box>
                                <Typography variant="body2">{dept.workLifeBalance}%</Typography>
                              </Box>
                            </TableCell>
                            <TableCell>
                              <Button
                                variant="outlined"
                                size="small"
                              >
                                View Details
                              </Button>
                            </TableCell>
                          </TableRow>
                        );
                      })}
                    </TableBody>
                  </Table>
                </TableContainer>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Trends & Insights Tab */}
      <TabPanel value={tabValue} index={2}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={8}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  Organizational Health Trends
                </Typography>
                
                <ResponsiveContainer width="100%" height={400}>
                  <LineChart data={orgHealthTrendData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis domain={[0, 100]} />
                    <RechartsTooltip />
                    <Line type="monotone" dataKey="satisfaction" stroke="#4caf50" strokeWidth={2} name="Satisfaction" />
                    <Line type="monotone" dataKey="retention" stroke="#2196f3" strokeWidth={2} name="Retention" />
                    <Line type="monotone" dataKey="productivity" stroke="#ff9800" strokeWidth={2} name="Productivity" />
                    <Line type="monotone" dataKey="innovation" stroke="#9c27b0" strokeWidth={2} name="Innovation" />
                    <Line type="monotone" dataKey="collaboration" stroke="#f44336" strokeWidth={2} name="Collaboration" />
                    <Line type="monotone" dataKey="workLifeBalance" stroke="#607d8b" strokeWidth={2} name="Work-Life Balance" />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  Health Score Distribution
                </Typography>
                
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={[
                        { name: 'Excellent (85+)', value: 35, color: '#4caf50' },
                        { name: 'Good (70-84)', value: 45, color: '#ff9800' },
                        { name: 'Needs Improvement (<70)', value: 20, color: '#f44336' },
                      ]}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {[
                        { name: 'Excellent (85+)', value: 35, color: '#4caf50' },
                        { name: 'Good (70-84)', value: 45, color: '#ff9800' },
                        { name: 'Needs Improvement (<70)', value: 20, color: '#f44336' },
                      ].map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <RechartsTooltip />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Initiatives Tab */}
      <TabPanel value={tabValue} index={3}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  Active Wellness Initiatives
                </Typography>
                
                <TableContainer component={Paper}>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Initiative</TableCell>
                        <TableCell>Status</TableCell>
                        <TableCell>Progress</TableCell>
                        <TableCell>Participants</TableCell>
                        <TableCell>Satisfaction</TableCell>
                        <TableCell>Impact</TableCell>
                        <TableCell>Actions</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {orgHealthData.initiatives.map((initiative) => (
                        <TableRow key={initiative.id}>
                          <TableCell>
                            <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                              {initiative.name}
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                              {initiative.description}
                            </Typography>
                          </TableCell>
                          <TableCell>
                            <Chip
                              label={initiative.status}
                              color={initiative.status === 'active' ? 'success' : 'default'}
                              size="small"
                            />
                          </TableCell>
                          <TableCell>
                            <Box sx={{ display: 'flex', alignItems: 'center' }}>
                              <Box sx={{ width: '100%', mr: 1 }}>
                                <LinearProgress
                                  variant="determinate"
                                  value={initiative.progress}
                                  color={getScoreColor(initiative.progress) as any}
                                  sx={{ height: 8, borderRadius: 4 }}
                                />
                              </Box>
                              <Typography variant="body2">
                                {initiative.progress}%
                              </Typography>
                            </Box>
                          </TableCell>
                          <TableCell>
                            <Typography variant="body2">
                              {initiative.participants}
                            </Typography>
                          </TableCell>
                          <TableCell>
                            <Box sx={{ display: 'flex', alignItems: 'center' }}>
                              <Rating value={initiative.satisfaction / 20} readOnly size="small" />
                              <Typography variant="body2" sx={{ ml: 1 }}>
                                {initiative.satisfaction}%
                              </Typography>
                            </Box>
                          </TableCell>
                          <TableCell>
                            <Chip
                              label={initiative.impact}
                              color={initiative.impact === 'high' ? 'error' : 'warning'}
                              size="small"
                            />
                          </TableCell>
                          <TableCell>
                            <Button
                              variant="outlined"
                              size="small"
                            >
                              Manage
                            </Button>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Advanced Analytics Tab */}
      <TabPanel value={tabValue} index={4}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  KPI Radar Chart
                </Typography>
                
                <ResponsiveContainer width="100%" height={300}>
                  <RadarChart data={kpiRadarData}>
                    <PolarGrid />
                    <PolarAngleAxis dataKey="metric" />
                    <PolarRadiusAxis domain={[0, 100]} />
                    <Radar
                      name="KPI Score"
                      dataKey="value"
                      stroke="#8884d8"
                      fill="#8884d8"
                      fillOpacity={0.6}
                    />
                    <RechartsTooltip />
                  </RadarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  Department Performance
                </Typography>
                
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={departmentComparisonData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="department" angle={-45} textAnchor="end" height={80} />
                    <YAxis domain={[0, 100]} />
                    <RechartsTooltip />
                    <Bar dataKey="overall" fill="#8884d8" name="Overall Score" />
                    <Bar dataKey="satisfaction" fill="#4caf50" name="Satisfaction" />
                    <Bar dataKey="productivity" fill="#ff9800" name="Productivity" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  Correlation Analysis
                </Typography>
                
                <ResponsiveContainer width="100%" height={400}>
                  <ComposedChart data={orgHealthTrendData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis yAxisId="left" domain={[0, 100]} />
                    <YAxis yAxisId="right" orientation="right" domain={[0, 100]} />
                    <RechartsTooltip />
                    <Area
                      yAxisId="left"
                      type="monotone"
                      dataKey="satisfaction"
                      stroke="#4caf50"
                      fill="#4caf50"
                      fillOpacity={0.3}
                      name="Satisfaction"
                    />
                    <Line
                      yAxisId="right"
                      type="monotone"
                      dataKey="productivity"
                      stroke="#ff9800"
                      strokeWidth={2}
                      name="Productivity"
                    />
                  </ComposedChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>
    </Box>
  );
};

export default OrganizationalHealth;
