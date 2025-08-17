import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Alert,
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
  Warning,
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
} from '@mui/icons-material';
import { useDispatch, useSelector } from 'react-redux';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell, AreaChart, Area, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';

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
    id={`risk-tabpanel-${index}`}
    aria-labelledby={`risk-tab-${index}`}
    {...other}
  >
    {value === index && <Box sx={{ pt: 3 }}>{children}</Box>}
  </div>
);

const RiskAssessment: React.FC = () => {
  const dispatch = useDispatch();
  const { user } = useSelector((state: RootState) => state.auth);
  
  const [tabValue, setTabValue] = useState(0);
  const [showInterventionDialog, setShowInterventionDialog] = useState(false);
  const [selectedRisk, setSelectedRisk] = useState<any>(null);
  const [showFilters, setShowFilters] = useState(false);
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [refreshInterval, setRefreshInterval] = useState(30);
  const [selectedTimeframe, setSelectedTimeframe] = useState('3months');
  const [riskThreshold, setRiskThreshold] = useState(70);
  const [showAdvancedMetrics, setShowAdvancedMetrics] = useState(false);
  const [selectedDepartments, setSelectedDepartments] = useState<string[]>([]);
  const [comparisonMode, setComparisonMode] = useState(false);

  // Risk assessment data
  const [riskData, setRiskData] = useState({
    overallRisk: 'medium',
    riskScore: 65,
    lastAssessment: '2024-01-25',
    trends: {
      stress: 'increasing',
      burnout: 'stable',
      engagement: 'decreasing',
      satisfaction: 'stable',
    },
    riskFactors: [
      {
        id: 1,
        factor: 'High Workload',
        riskLevel: 'high',
        score: 85,
        trend: 'increasing',
        impact: 'High',
        description: 'Consistently high workload over the past 3 months',
        recommendations: [
          'Consider workload redistribution',
          'Implement time management training',
          'Review project priorities'
        ]
      },
      {
        id: 2,
        factor: 'Work-Life Balance',
        riskLevel: 'medium',
        score: 65,
        trend: 'stable',
        impact: 'Medium',
        description: 'Moderate work-life balance concerns',
        recommendations: [
          'Encourage boundary setting',
          'Promote flexible work arrangements',
          'Provide stress management resources'
        ]
      },
      {
        id: 3,
        factor: 'Team Dynamics',
        riskLevel: 'low',
        score: 35,
        trend: 'improving',
        impact: 'Low',
        description: 'Positive team dynamics with minor concerns',
        recommendations: [
          'Continue team building activities',
          'Maintain open communication channels',
          'Address any emerging conflicts promptly'
        ]
      }
    ],
    interventions: [
      {
        id: 1,
        type: 'Immediate',
        title: 'Workload Assessment',
        description: 'Conduct individual workload assessment with manager',
        priority: 'High',
        assignedTo: 'Manager',
        dueDate: '2024-02-01',
        status: 'pending'
      },
      {
        id: 2,
        type: 'Short-term',
        title: 'Stress Management Workshop',
        description: 'Attend stress management and resilience workshop',
        priority: 'Medium',
        assignedTo: 'Employee',
        dueDate: '2024-02-15',
        status: 'scheduled'
      },
      {
        id: 3,
        type: 'Long-term',
        title: 'Career Development Plan',
        description: 'Develop career development and growth plan',
        priority: 'Medium',
        assignedTo: 'HR',
        dueDate: '2024-03-01',
        status: 'planned'
      }
    ]
  });

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleInterventionClick = (intervention: any) => {
    setSelectedRisk(intervention);
    setShowInterventionDialog(true);
  };

  const getRiskColor = (level: string) => {
    switch (level) {
      case 'high': return 'error';
      case 'medium': return 'warning';
      case 'low': return 'success';
      default: return 'default';
    }
  };

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'increasing': return <TrendingUp color="error" />;
      case 'decreasing': return <TrendingDown color="success" />;
      case 'stable': return <CheckCircle color="info" />;
      case 'improving': return <TrendingUp color="success" />;
      default: return <Info color="info" />;
    }
  };

  const getTrendLabel = (trend: string) => {
    switch (trend) {
      case 'increasing': return 'Increasing Risk';
      case 'decreasing': return 'Decreasing Risk';
      case 'stable': return 'Stable';
      case 'improving': return 'Improving';
      default: return 'Unknown';
    }
  };

  // Enhanced chart data
  const riskTrendData = [
    { month: 'Oct', stress: 45, burnout: 30, engagement: 75, satisfaction: 70, productivity: 82, absenteeism: 3 },
    { month: 'Nov', stress: 55, burnout: 35, engagement: 70, satisfaction: 68, productivity: 78, absenteeism: 5 },
    { month: 'Dec', stress: 65, burnout: 40, engagement: 65, satisfaction: 65, productivity: 72, absenteeism: 7 },
    { month: 'Jan', stress: 75, burnout: 45, engagement: 60, satisfaction: 62, productivity: 68, absenteeism: 9 },
  ];

  const riskDistributionData = [
    { name: 'Low Risk', value: 45, color: '#4caf50' },
    { name: 'Medium Risk', value: 35, color: '#ff9800' },
    { name: 'High Risk', value: 20, color: '#f44336' },
  ];

  const departmentComparisonData = [
    { department: 'Engineering', stress: 72, burnout: 38, engagement: 58, satisfaction: 61 },
    { department: 'Sales', stress: 68, burnout: 42, engagement: 62, satisfaction: 59 },
    { department: 'Marketing', stress: 65, burnout: 35, engagement: 68, satisfaction: 65 },
    { department: 'HR', stress: 58, burnout: 28, engagement: 75, satisfaction: 72 },
    { department: 'Finance', stress: 62, burnout: 32, engagement: 70, satisfaction: 68 },
  ];

  const wellnessFactorsData = [
    { factor: 'Physical Health', score: 75, impact: 'High' },
    { factor: 'Mental Health', score: 65, impact: 'High' },
    { factor: 'Social Support', score: 80, impact: 'Medium' },
    { factor: 'Work Environment', score: 70, impact: 'High' },
    { factor: 'Financial Security', score: 85, impact: 'Medium' },
    { factor: 'Career Growth', score: 60, impact: 'High' },
  ];

  const interventionEffectivenessData = [
    { intervention: 'Stress Management', effectiveness: 85, participants: 45, cost: 2500 },
    { intervention: 'Flexible Hours', effectiveness: 78, participants: 120, cost: 1500 },
    { intervention: 'Mental Health Support', effectiveness: 92, participants: 28, cost: 5000 },
    { intervention: 'Team Building', effectiveness: 72, participants: 85, cost: 3000 },
    { intervention: 'Wellness Programs', effectiveness: 68, participants: 95, cost: 2000 },
  ];

  return (
    <Box sx={{ p: 3, maxWidth: 1400, mx: 'auto' }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" sx={{ fontWeight: 600, color: 'primary.main' }}>
          Risk Assessment & Burnout Prevention
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

      {/* Enhanced Control Panel */}
      <Accordion expanded={showFilters} onChange={() => setShowFilters(!showFilters)} sx={{ mb: 3 }}>
        <AccordionSummary expandIcon={<ExpandMore />}>
          <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center' }}>
            <FilterList sx={{ mr: 1 }} />
            Filters & Settings
          </Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Grid container spacing={3}>
            <Grid item xs={12} md={3}>
              <FormControl fullWidth>
                <InputLabel>Timeframe</InputLabel>
                <Select
                  value={selectedTimeframe}
                  onChange={(e) => setSelectedTimeframe(e.target.value)}
                  label="Timeframe"
                >
                  <MenuItem value="1week">Last Week</MenuItem>
                  <MenuItem value="1month">Last Month</MenuItem>
                  <MenuItem value="3months">Last 3 Months</MenuItem>
                  <MenuItem value="6months">Last 6 Months</MenuItem>
                  <MenuItem value="1year">Last Year</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12} md={3}>
              <FormControl fullWidth>
                <InputLabel>Departments</InputLabel>
                <Select
                  multiple
                  value={selectedDepartments}
                  onChange={(e) => setSelectedDepartments(e.target.value as string[])}
                  label="Departments"
                >
                  <MenuItem value="engineering">Engineering</MenuItem>
                  <MenuItem value="sales">Sales</MenuItem>
                  <MenuItem value="marketing">Marketing</MenuItem>
                  <MenuItem value="hr">HR</MenuItem>
                  <MenuItem value="finance">Finance</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12} md={3}>
              <Typography variant="body2" gutterBottom>
                Risk Threshold: {riskThreshold}%
              </Typography>
              <Slider
                value={riskThreshold}
                onChange={(e, value) => setRiskThreshold(value as number)}
                min={0}
                max={100}
                valueLabelDisplay="auto"
              />
            </Grid>
            
            <Grid item xs={12} md={3}>
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
                <FormControlLabel
                  control={
                    <Switch
                      checked={comparisonMode}
                      onChange={(e) => setComparisonMode(e.target.checked)}
                    />
                  }
                  label="Comparison Mode"
                />
              </Stack>
            </Grid>
          </Grid>
        </AccordionDetails>
      </Accordion>

      {/* Risk Overview */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Assessment sx={{ mr: 1, color: 'primary.main' }} />
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Overall Risk Level
                </Typography>
              </Box>
              
              <Box sx={{ textAlign: 'center', mb: 2 }}>
                <Typography variant="h3" sx={{ fontWeight: 700, color: `${getRiskColor(riskData.overallRisk)}.main` }}>
                  {riskData.riskScore}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Risk Score
                </Typography>
              </Box>
              
              <Chip
                label={riskData.overallRisk.toUpperCase()}
                color={getRiskColor(riskData.overallRisk) as any}
                sx={{ fontWeight: 600 }}
              />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Timeline sx={{ mr: 1, color: 'primary.main' }} />
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Risk Trends
                </Typography>
              </Box>
              
              <List dense>
                {Object.entries(riskData.trends).map(([key, trend]) => (
                  <ListItem key={key}>
                    <ListItemIcon>
                      {getTrendIcon(trend)}
                    </ListItemIcon>
                    <ListItemText
                      primary={key.charAt(0).toUpperCase() + key.slice(1)}
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
                <Notifications sx={{ mr: 1, color: 'primary.main' }} />
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Recent Alerts
                </Typography>
              </Box>
              
              <Alert severity="warning" sx={{ mb: 2 }}>
                High workload detected - intervention recommended
              </Alert>
              
              <Alert severity="info" sx={{ mb: 2 }}>
                Stress levels trending upward
              </Alert>
              
              <Button
                variant="outlined"
                size="small"
                fullWidth
              >
                View All Alerts
              </Button>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Tabs */}
      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={tabValue} onChange={handleTabChange} aria-label="risk assessment tabs">
          <Tab label="Risk Factors" />
          <Tab label="Interventions" />
          <Tab label="Trends" />
          <Tab label="Recommendations" />
          <Tab label="Advanced Analytics" />
          <Tab label="Department Comparison" />
        </Tabs>
      </Box>

      {/* Risk Factors Tab */}
      <TabPanel value={tabValue} index={0}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  Identified Risk Factors
                </Typography>
                
                <TableContainer component={Paper}>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Risk Factor</TableCell>
                        <TableCell>Risk Level</TableCell>
                        <TableCell>Score</TableCell>
                        <TableCell>Trend</TableCell>
                        <TableCell>Impact</TableCell>
                        <TableCell>Actions</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {riskData.riskFactors.map((factor) => (
                        <TableRow key={factor.id}>
                          <TableCell>
                            <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                              {factor.factor}
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                              {factor.description}
                            </Typography>
                          </TableCell>
                          <TableCell>
                            <Chip
                              label={factor.riskLevel}
                              color={getRiskColor(factor.riskLevel) as any}
                              size="small"
                            />
                          </TableCell>
                          <TableCell>
                            <Box sx={{ display: 'flex', alignItems: 'center' }}>
                              <Box sx={{ width: '100%', mr: 1 }}>
                                <LinearProgress
                                  variant="determinate"
                                  value={factor.score}
                                  color={getRiskColor(factor.riskLevel) as any}
                                  sx={{ height: 8, borderRadius: 4 }}
                                />
                              </Box>
                              <Typography variant="body2">
                                {factor.score}
                              </Typography>
                            </Box>
                          </TableCell>
                          <TableCell>
                            <Box sx={{ display: 'flex', alignItems: 'center' }}>
                              {getTrendIcon(factor.trend)}
                              <Typography variant="body2" sx={{ ml: 1 }}>
                                {getTrendLabel(factor.trend)}
                              </Typography>
                            </Box>
                          </TableCell>
                          <TableCell>
                            <Chip
                              label={factor.impact}
                              size="small"
                              variant="outlined"
                            />
                          </TableCell>
                          <TableCell>
                            <Button
                              variant="outlined"
                              size="small"
                              onClick={() => {
                                setSelectedRisk(factor);
                                setShowInterventionDialog(true);
                              }}
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

      {/* Interventions Tab */}
      <TabPanel value={tabValue} index={1}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  Recommended Interventions
                </Typography>
                
                <TableContainer component={Paper}>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Intervention</TableCell>
                        <TableCell>Type</TableCell>
                        <TableCell>Priority</TableCell>
                        <TableCell>Assigned To</TableCell>
                        <TableCell>Due Date</TableCell>
                        <TableCell>Status</TableCell>
                        <TableCell>Actions</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {riskData.interventions.map((intervention) => (
                        <TableRow key={intervention.id}>
                          <TableCell>
                            <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                              {intervention.title}
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                              {intervention.description}
                            </Typography>
                          </TableCell>
                          <TableCell>
                            <Chip
                              label={intervention.type}
                              size="small"
                              variant="outlined"
                            />
                          </TableCell>
                          <TableCell>
                            <Chip
                              label={intervention.priority}
                              color={intervention.priority === 'High' ? 'error' : 'warning'}
                              size="small"
                            />
                          </TableCell>
                          <TableCell>{intervention.assignedTo}</TableCell>
                          <TableCell>{new Date(intervention.dueDate).toLocaleDateString()}</TableCell>
                          <TableCell>
                            <Chip
                              label={intervention.status}
                              color={intervention.status === 'completed' ? 'success' : 'default'}
                              size="small"
                            />
                          </TableCell>
                          <TableCell>
                            <Button
                              variant="outlined"
                              size="small"
                              onClick={() => handleInterventionClick(intervention)}
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

      {/* Trends Tab */}
      <TabPanel value={tabValue} index={2}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={8}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  Risk Trends Over Time
                </Typography>
                
                <ResponsiveContainer width="100%" height={400}>
                  <LineChart data={riskTrendData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis domain={[0, 100]} />
                    <Tooltip />
                    <Line type="monotone" dataKey="stress" stroke="#f44336" strokeWidth={2} name="Stress" />
                    <Line type="monotone" dataKey="burnout" stroke="#ff9800" strokeWidth={2} name="Burnout" />
                    <Line type="monotone" dataKey="engagement" stroke="#4caf50" strokeWidth={2} name="Engagement" />
                    <Line type="monotone" dataKey="satisfaction" stroke="#2196f3" strokeWidth={2} name="Satisfaction" />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  Risk Distribution
                </Typography>
                
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={riskDistributionData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {riskDistributionData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Recommendations Tab */}
      <TabPanel value={tabValue} index={3}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  Immediate Actions
                </Typography>
                
                <List>
                  {riskData.riskFactors
                    .filter(factor => factor.riskLevel === 'high')
                    .flatMap(factor => factor.recommendations)
                    .slice(0, 5)
                    .map((recommendation, index) => (
                      <ListItem key={index}>
                        <ListItemIcon>
                          <Warning color="error" />
                        </ListItemIcon>
                        <ListItemText primary={recommendation} />
                      </ListItem>
                    ))}
                </List>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  Long-term Strategies
                </Typography>
                
                <List>
                  <ListItem>
                    <ListItemIcon>
                      <Psychology color="primary" />
                    </ListItemIcon>
                    <ListItemText
                      primary="Implement Regular Wellness Check-ins"
                      secondary="Monthly wellness assessments for early intervention"
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <Group color="primary" />
                    </ListItemIcon>
                    <ListItemText
                      primary="Enhance Team Support Systems"
                      secondary="Peer support programs and mentorship"
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <Schedule color="primary" />
                    </ListItemIcon>
                    <ListItemText
                      primary="Flexible Work Arrangements"
                      secondary="Remote work options and flexible hours"
                    />
                  </ListItem>
                </List>
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
                  Wellness Factors Radar Chart
                </Typography>
                
                <ResponsiveContainer width="100%" height={300}>
                  <RadarChart data={wellnessFactorsData}>
                    <PolarGrid />
                    <PolarAngleAxis dataKey="factor" />
                    <PolarRadiusAxis domain={[0, 100]} />
                    <Radar
                      name="Wellness Score"
                      dataKey="score"
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
                  Intervention Effectiveness
                </Typography>
                
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={interventionEffectivenessData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="intervention" angle={-45} textAnchor="end" height={80} />
                    <YAxis domain={[0, 100]} />
                    <RechartsTooltip />
                    <Bar dataKey="effectiveness" fill="#8884d8" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  Productivity vs Wellness Correlation
                </Typography>
                
                <ResponsiveContainer width="100%" height={400}>
                  <AreaChart data={riskTrendData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis yAxisId="left" domain={[0, 100]} />
                    <YAxis yAxisId="right" orientation="right" domain={[0, 100]} />
                    <RechartsTooltip />
                    <Area
                      yAxisId="left"
                      type="monotone"
                      dataKey="productivity"
                      stroke="#4caf50"
                      fill="#4caf50"
                      fillOpacity={0.3}
                      name="Productivity"
                    />
                    <Area
                      yAxisId="right"
                      type="monotone"
                      dataKey="stress"
                      stroke="#f44336"
                      fill="#f44336"
                      fillOpacity={0.3}
                      name="Stress Level"
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Department Comparison Tab */}
      <TabPanel value={tabValue} index={5}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  Department Wellness Comparison
                </Typography>
                
                <TableContainer component={Paper}>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Department</TableCell>
                        <TableCell>Stress Level</TableCell>
                        <TableCell>Burnout Risk</TableCell>
                        <TableCell>Engagement</TableCell>
                        <TableCell>Satisfaction</TableCell>
                        <TableCell>Overall Score</TableCell>
                        <TableCell>Actions</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {departmentComparisonData.map((dept) => {
                        const overallScore = Math.round((dept.stress + dept.burnout + dept.engagement + dept.satisfaction) / 4);
                        return (
                          <TableRow key={dept.department}>
                            <TableCell>
                              <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                                {dept.department}
                              </Typography>
                            </TableCell>
                            <TableCell>
                              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                <Box sx={{ width: '100%', mr: 1 }}>
                                  <LinearProgress
                                    variant="determinate"
                                    value={dept.stress}
                                    color={dept.stress > 70 ? 'error' : dept.stress > 50 ? 'warning' : 'success'}
                                    sx={{ height: 8, borderRadius: 4 }}
                                  />
                                </Box>
                                <Typography variant="body2">{dept.stress}%</Typography>
                              </Box>
                            </TableCell>
                            <TableCell>
                              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                <Box sx={{ width: '100%', mr: 1 }}>
                                  <LinearProgress
                                    variant="determinate"
                                    value={dept.burnout}
                                    color={dept.burnout > 40 ? 'error' : dept.burnout > 25 ? 'warning' : 'success'}
                                    sx={{ height: 8, borderRadius: 4 }}
                                  />
                                </Box>
                                <Typography variant="body2">{dept.burnout}%</Typography>
                              </Box>
                            </TableCell>
                            <TableCell>
                              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                <Box sx={{ width: '100%', mr: 1 }}>
                                  <LinearProgress
                                    variant="determinate"
                                    value={dept.engagement}
                                    color={dept.engagement > 70 ? 'success' : dept.engagement > 50 ? 'warning' : 'error'}
                                    sx={{ height: 8, borderRadius: 4 }}
                                  />
                                </Box>
                                <Typography variant="body2">{dept.engagement}%</Typography>
                              </Box>
                            </TableCell>
                            <TableCell>
                              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                <Box sx={{ width: '100%', mr: 1 }}>
                                  <LinearProgress
                                    variant="determinate"
                                    value={dept.satisfaction}
                                    color={dept.satisfaction > 70 ? 'success' : dept.satisfaction > 50 ? 'warning' : 'error'}
                                    sx={{ height: 8, borderRadius: 4 }}
                                  />
                                </Box>
                                <Typography variant="body2">{dept.satisfaction}%</Typography>
                              </Box>
                            </TableCell>
                            <TableCell>
                              <Chip
                                label={`${overallScore}/100`}
                                color={overallScore > 70 ? 'success' : overallScore > 50 ? 'warning' : 'error'}
                                sx={{ fontWeight: 600 }}
                              />
                            </TableCell>
                            <TableCell>
                              <Button
                                variant="outlined"
                                size="small"
                                onClick={() => {
                                  setSelectedRisk({ ...dept, type: 'department' });
                                  setShowInterventionDialog(true);
                                }}
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

      {/* Intervention Dialog */}
      <Dialog
        open={showInterventionDialog}
        onClose={() => setShowInterventionDialog(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          {selectedRisk?.title || 'Risk Factor Details'}
        </DialogTitle>
        <DialogContent>
          {selectedRisk && (
            <Box>
              <Typography variant="body1" sx={{ mb: 2 }}>
                {selectedRisk.description}
              </Typography>
              
              {selectedRisk.recommendations && (
                <Box sx={{ mb: 2 }}>
                  <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1 }}>
                    Recommendations:
                  </Typography>
                  <List dense>
                    {selectedRisk.recommendations.map((rec: string, index: number) => (
                      <ListItem key={index}>
                        <ListItemIcon>
                          <CheckCircle color="primary" />
                        </ListItemIcon>
                        <ListItemText primary={rec} />
                      </ListItem>
                    ))}
                  </List>
                </Box>
              )}
              
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <TextField
                    fullWidth
                    label="Status"
                    defaultValue={selectedRisk.status || 'Pending'}
                    select
                  >
                    <MenuItem value="pending">Pending</MenuItem>
                    <MenuItem value="in-progress">In Progress</MenuItem>
                    <MenuItem value="completed">Completed</MenuItem>
                  </TextField>
                </Grid>
                <Grid item xs={6}>
                  <TextField
                    fullWidth
                    label="Priority"
                    defaultValue={selectedRisk.priority || 'Medium'}
                    select
                  >
                    <MenuItem value="low">Low</MenuItem>
                    <MenuItem value="medium">Medium</MenuItem>
                    <MenuItem value="high">High</MenuItem>
                  </TextField>
                </Grid>
              </Grid>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowInterventionDialog(false)}>Cancel</Button>
          <Button variant="contained" onClick={() => setShowInterventionDialog(false)}>
            Save Changes
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default RiskAssessment;
