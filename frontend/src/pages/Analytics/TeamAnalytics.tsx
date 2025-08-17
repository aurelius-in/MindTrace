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
  Team,
  GroupWork,
  Handshake,
  Celebration,
  Support,
  Feedback,
  Communication,
  Collaboration,
  NetworkCheck,
  SpeedDial,
  SpeedDialAction,
  SpeedDialIcon,
} from '@mui/icons-material';
import { useDispatch, useSelector } from 'react-redux';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell, AreaChart, Area, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ComposedChart, ScatterChart, Scatter } from 'recharts';

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
    id={`team-analytics-tabpanel-${index}`}
    aria-labelledby={`team-analytics-tab-${index}`}
    {...other}
  >
    {value === index && <Box sx={{ pt: 3 }}>{children}</Box>}
  </div>
);

const TeamAnalytics: React.FC = () => {
  const dispatch = useDispatch();
  const { user } = useSelector((state: RootState) => state.auth);
  
  const [tabValue, setTabValue] = useState(0);
  const [showFilters, setShowFilters] = useState(false);
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [selectedTimeframe, setSelectedTimeframe] = useState('3months');
  const [selectedTeam, setSelectedTeam] = useState('all');
  const [showAdvancedMetrics, setShowAdvancedMetrics] = useState(false);

  // Team analytics data
  const [teamAnalyticsData, setTeamAnalyticsData] = useState({
    overallTeamScore: 82,
    lastUpdated: '2024-01-25',
    totalTeams: 12,
    activeTeams: 11,
    trends: {
      collaboration: 'improving',
      communication: 'stable',
      productivity: 'improving',
      satisfaction: 'improving',
      innovation: 'stable',
      support: 'improving',
    },
    teams: [
      {
        id: 1,
        name: 'Engineering Team Alpha',
        lead: 'Sarah Johnson',
        members: 8,
        wellnessScore: 85,
        collaborationScore: 88,
        productivityScore: 82,
        satisfactionScore: 87,
        innovationScore: 79,
        supportScore: 91,
        recentActivities: [
          'Weekly team wellness check-in',
          'Collaborative problem-solving session',
          'Innovation workshop participation'
        ],
        challenges: [
          'High workload during sprint',
          'Remote team coordination'
        ],
        strengths: [
          'Strong peer support network',
          'Excellent communication',
          'High engagement in wellness programs'
        ]
      },
      {
        id: 2,
        name: 'Sales Team Bravo',
        lead: 'Michael Chen',
        members: 6,
        wellnessScore: 78,
        collaborationScore: 75,
        productivityScore: 88,
        satisfactionScore: 82,
        innovationScore: 72,
        supportScore: 79,
        recentActivities: [
          'Stress management workshop',
          'Team building exercise',
          'Performance review session'
        ],
        challenges: [
          'High-pressure sales targets',
          'Work-life balance concerns'
        ],
        strengths: [
          'High productivity',
          'Strong goal orientation',
          'Good team morale'
        ]
      },
      {
        id: 3,
        name: 'Marketing Team Charlie',
        lead: 'Emily Rodriguez',
        members: 5,
        wellnessScore: 83,
        collaborationScore: 92,
        productivityScore: 85,
        satisfactionScore: 89,
        innovationScore: 88,
        supportScore: 86,
        recentActivities: [
          'Creative brainstorming session',
          'Wellness challenge participation',
          'Cross-team collaboration'
        ],
        challenges: [
          'Creative burnout prevention',
          'Deadline management'
        ],
        strengths: [
          'Excellent collaboration',
          'High creativity',
          'Strong team culture'
        ]
      },
      {
        id: 4,
        name: 'HR Team Delta',
        lead: 'David Thompson',
        members: 4,
        wellnessScore: 90,
        collaborationScore: 85,
        productivityScore: 87,
        satisfactionScore: 92,
        innovationScore: 75,
        supportScore: 94,
        recentActivities: [
          'Employee wellness program launch',
          'Team support initiatives',
          'Policy development'
        ],
        challenges: [
          'Balancing multiple priorities',
          'Supporting other teams'
        ],
        strengths: [
          'High empathy and support',
          'Strong organizational skills',
          'Excellent communication'
        ]
      }
    ],
    teamMetrics: [
      {
        metric: 'Team Collaboration',
        average: 85,
        trend: 'improving',
        description: 'Cross-team collaboration effectiveness',
        impact: 'High'
      },
      {
        metric: 'Communication Quality',
        average: 82,
        trend: 'stable',
        description: 'Team communication and information sharing',
        impact: 'High'
      },
      {
        metric: 'Peer Support',
        average: 88,
        trend: 'improving',
        description: 'Team member support and assistance',
        impact: 'High'
      },
      {
        metric: 'Team Morale',
        average: 84,
        trend: 'improving',
        description: 'Overall team satisfaction and engagement',
        impact: 'Medium'
      },
      {
        metric: 'Innovation Culture',
        average: 78,
        trend: 'stable',
        description: 'Team creativity and innovation',
        impact: 'Medium'
      },
      {
        metric: 'Work-Life Balance',
        average: 81,
        trend: 'improving',
        description: 'Team work-life balance satisfaction',
        impact: 'High'
      }
    ],
    teamInterventions: [
      {
        id: 1,
        teamId: 1,
        type: 'Wellness Workshop',
        title: 'Stress Management for Engineers',
        status: 'completed',
        effectiveness: 92,
        participants: 8,
        description: 'Specialized stress management workshop for engineering team'
      },
      {
        id: 2,
        teamId: 2,
        type: 'Team Building',
        title: 'Sales Team Retreat',
        status: 'scheduled',
        effectiveness: 0,
        participants: 6,
        description: 'Team building retreat to improve collaboration'
      },
      {
        id: 3,
        teamId: 3,
        type: 'Innovation Program',
        title: 'Creative Wellness Challenge',
        status: 'active',
        effectiveness: 85,
        participants: 5,
        description: 'Wellness challenge focused on creative teams'
      },
      {
        id: 4,
        teamId: 4,
        type: 'Support Training',
        title: 'HR Team Support Skills',
        status: 'completed',
        effectiveness: 89,
        participants: 4,
        description: 'Advanced support and empathy training'
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
  const teamTrendData = [
    { month: 'Oct', collaboration: 82, communication: 80, productivity: 85, satisfaction: 83, innovation: 75, support: 85 },
    { month: 'Nov', collaboration: 84, communication: 81, productivity: 86, satisfaction: 84, innovation: 76, support: 86 },
    { month: 'Dec', collaboration: 85, communication: 82, productivity: 87, satisfaction: 85, innovation: 77, support: 87 },
    { month: 'Jan', collaboration: 88, communication: 82, productivity: 88, satisfaction: 87, innovation: 78, support: 88 },
  ];

  const teamRadarData = [
    { metric: 'Collaboration', value: 85, fullMark: 100 },
    { metric: 'Communication', value: 82, fullMark: 100 },
    { metric: 'Productivity', value: 88, fullMark: 100 },
    { metric: 'Satisfaction', value: 87, fullMark: 100 },
    { metric: 'Innovation', value: 78, fullMark: 100 },
    { metric: 'Support', value: 88, fullMark: 100 },
  ];

  const teamComparisonData = teamAnalyticsData.teams.map(team => ({
    team: team.name,
    overall: Math.round((team.wellnessScore + team.collaborationScore + team.productivityScore + team.satisfactionScore + team.innovationScore + team.supportScore) / 6),
    wellness: team.wellnessScore,
    collaboration: team.collaborationScore,
    productivity: team.productivityScore,
  }));

  const collaborationScatterData = teamAnalyticsData.teams.map(team => ({
    team: team.name,
    collaboration: team.collaborationScore,
    productivity: team.productivityScore,
    satisfaction: team.satisfactionScore,
    size: team.members,
  }));

  return (
    <Box sx={{ p: 3, maxWidth: 1400, mx: 'auto' }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" sx={{ fontWeight: 600, color: 'primary.main' }}>
          Team Analytics Dashboard
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
            <Grid item xs={12} md={3}>
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
            
            <Grid item xs={12} md={3}>
              <FormControl fullWidth>
                <InputLabel>Team</InputLabel>
                <Select
                  value={selectedTeam}
                  onChange={(e) => setSelectedTeam(e.target.value)}
                  label="Team"
                >
                  <MenuItem value="all">All Teams</MenuItem>
                  {teamAnalyticsData.teams.map(team => (
                    <MenuItem key={team.id} value={team.id}>{team.name}</MenuItem>
                  ))}
                </Select>
              </FormControl>
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
              </Stack>
            </Grid>
            
            <Grid item xs={12} md={3}>
              <Typography variant="body2" gutterBottom>
                Last Updated: {new Date(teamAnalyticsData.lastUpdated).toLocaleDateString()}
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

      {/* Team Overview */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Team sx={{ mr: 1, color: 'primary.main' }} />
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Overall Team Score
                </Typography>
              </Box>
              
              <Box sx={{ textAlign: 'center', mb: 2 }}>
                <Typography variant="h3" sx={{ fontWeight: 700, color: `${getScoreColor(teamAnalyticsData.overallTeamScore)}.main` }}>
                  {teamAnalyticsData.overallTeamScore}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  out of 100
                </Typography>
              </Box>
              
              <Chip
                label={teamAnalyticsData.overallTeamScore >= 85 ? 'Excellent' : teamAnalyticsData.overallTeamScore >= 70 ? 'Good' : 'Needs Improvement'}
                color={getScoreColor(teamAnalyticsData.overallTeamScore) as any}
                sx={{ fontWeight: 600 }}
              />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <GroupWork sx={{ mr: 1, color: 'primary.main' }} />
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Team Statistics
                </Typography>
              </Box>
              
              <List dense>
                <ListItem>
                  <ListItemIcon>
                    <People color="primary" />
                  </ListItemIcon>
                  <ListItemText
                    primary={`${teamAnalyticsData.totalTeams} Total Teams`}
                    secondary={`${teamAnalyticsData.activeTeams} Active`}
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <Handshake color="success" />
                  </ListItemIcon>
                  <ListItemText
                    primary="Average Team Size"
                    secondary="6 members"
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <Celebration color="warning" />
                  </ListItemIcon>
                  <ListItemText
                    primary="Top Performing Team"
                    secondary="Engineering Alpha"
                  />
                </ListItem>
              </List>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <TrendingUp sx={{ mr: 1, color: 'primary.main' }} />
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Key Trends
                </Typography>
              </Box>
              
              <List dense>
                {Object.entries(teamAnalyticsData.trends).map(([key, trend]) => (
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

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Support sx={{ mr: 1, color: 'primary.main' }} />
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Recent Activities
                </Typography>
              </Box>
              
              <List dense>
                <ListItem>
                  <ListItemIcon>
                    <CheckCircle color="success" />
                  </ListItemIcon>
                  <ListItemText
                    primary="Wellness Workshop"
                    secondary="Completed by 3 teams"
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <GroupWork color="primary" />
                  </ListItemIcon>
                  <ListItemText
                    primary="Team Building"
                    secondary="2 teams scheduled"
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <Feedback color="warning" />
                  </ListItemIcon>
                  <ListItemText
                    primary="Feedback Session"
                    secondary="All teams participated"
                  />
                </ListItem>
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Tabs */}
      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={tabValue} onChange={handleTabChange} aria-label="team analytics tabs">
          <Tab label="Team Overview" />
          <Tab label="Team Metrics" />
          <Tab label="Collaboration Analysis" />
          <Tab label="Interventions" />
          <Tab label="Advanced Analytics" />
        </Tabs>
      </Box>

      {/* Team Overview Tab */}
      <TabPanel value={tabValue} index={0}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  Team Performance Overview
                </Typography>
                
                <TableContainer component={Paper}>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Team</TableCell>
                        <TableCell>Lead</TableCell>
                        <TableCell>Members</TableCell>
                        <TableCell>Overall Score</TableCell>
                        <TableCell>Wellness</TableCell>
                        <TableCell>Collaboration</TableCell>
                        <TableCell>Productivity</TableCell>
                        <TableCell>Satisfaction</TableCell>
                        <TableCell>Innovation</TableCell>
                        <TableCell>Support</TableCell>
                        <TableCell>Actions</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {teamAnalyticsData.teams.map((team) => {
                        const overallScore = Math.round((team.wellnessScore + team.collaborationScore + team.productivityScore + team.satisfactionScore + team.innovationScore + team.supportScore) / 6);
                        return (
                          <TableRow key={team.id}>
                            <TableCell>
                              <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                                {team.name}
                              </Typography>
                            </TableCell>
                            <TableCell>
                              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                <Avatar sx={{ width: 24, height: 24, mr: 1 }}>
                                  {team.lead.charAt(0)}
                                </Avatar>
                                <Typography variant="body2">
                                  {team.lead}
                                </Typography>
                              </Box>
                            </TableCell>
                            <TableCell>
                              <Typography variant="body2">
                                {team.members}
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
                                    value={team.wellnessScore}
                                    color={getScoreColor(team.wellnessScore) as any}
                                    sx={{ height: 8, borderRadius: 4 }}
                                  />
                                </Box>
                                <Typography variant="body2">{team.wellnessScore}%</Typography>
                              </Box>
                            </TableCell>
                            <TableCell>
                              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                <Box sx={{ width: '100%', mr: 1 }}>
                                  <LinearProgress
                                    variant="determinate"
                                    value={team.collaborationScore}
                                    color={getScoreColor(team.collaborationScore) as any}
                                    sx={{ height: 8, borderRadius: 4 }}
                                  />
                                </Box>
                                <Typography variant="body2">{team.collaborationScore}%</Typography>
                              </Box>
                            </TableCell>
                            <TableCell>
                              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                <Box sx={{ width: '100%', mr: 1 }}>
                                  <LinearProgress
                                    variant="determinate"
                                    value={team.productivityScore}
                                    color={getScoreColor(team.productivityScore) as any}
                                    sx={{ height: 8, borderRadius: 4 }}
                                  />
                                </Box>
                                <Typography variant="body2">{team.productivityScore}%</Typography>
                              </Box>
                            </TableCell>
                            <TableCell>
                              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                <Box sx={{ width: '100%', mr: 1 }}>
                                  <LinearProgress
                                    variant="determinate"
                                    value={team.satisfactionScore}
                                    color={getScoreColor(team.satisfactionScore) as any}
                                    sx={{ height: 8, borderRadius: 4 }}
                                  />
                                </Box>
                                <Typography variant="body2">{team.satisfactionScore}%</Typography>
                              </Box>
                            </TableCell>
                            <TableCell>
                              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                <Box sx={{ width: '100%', mr: 1 }}>
                                  <LinearProgress
                                    variant="determinate"
                                    value={team.innovationScore}
                                    color={getScoreColor(team.innovationScore) as any}
                                    sx={{ height: 8, borderRadius: 4 }}
                                  />
                                </Box>
                                <Typography variant="body2">{team.innovationScore}%</Typography>
                              </Box>
                            </TableCell>
                            <TableCell>
                              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                <Box sx={{ width: '100%', mr: 1 }}>
                                  <LinearProgress
                                    variant="determinate"
                                    value={team.supportScore}
                                    color={getScoreColor(team.supportScore) as any}
                                    sx={{ height: 8, borderRadius: 4 }}
                                  />
                                </Box>
                                <Typography variant="body2">{team.supportScore}%</Typography>
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

      {/* Team Metrics Tab */}
      <TabPanel value={tabValue} index={1}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  Team Performance Metrics
                </Typography>
                
                <TableContainer component={Paper}>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Metric</TableCell>
                        <TableCell>Average Score</TableCell>
                        <TableCell>Trend</TableCell>
                        <TableCell>Description</TableCell>
                        <TableCell>Impact</TableCell>
                        <TableCell>Actions</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {teamAnalyticsData.teamMetrics.map((metric) => (
                        <TableRow key={metric.metric}>
                          <TableCell>
                            <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                              {metric.metric}
                            </Typography>
                          </TableCell>
                          <TableCell>
                            <Box sx={{ display: 'flex', alignItems: 'center' }}>
                              <Box sx={{ width: '100%', mr: 1 }}>
                                <LinearProgress
                                  variant="determinate"
                                  value={metric.average}
                                  color={getScoreColor(metric.average) as any}
                                  sx={{ height: 8, borderRadius: 4 }}
                                />
                              </Box>
                              <Typography variant="body2">
                                {metric.average}%
                              </Typography>
                            </Box>
                          </TableCell>
                          <TableCell>
                            <Box sx={{ display: 'flex', alignItems: 'center' }}>
                              {getTrendIcon(metric.trend)}
                              <Typography variant="body2" sx={{ ml: 1 }}>
                                {getTrendLabel(metric.trend)}
                              </Typography>
                            </Box>
                          </TableCell>
                          <TableCell>
                            <Typography variant="body2" color="text.secondary">
                              {metric.description}
                            </Typography>
                          </TableCell>
                          <TableCell>
                            <Chip
                              label={metric.impact}
                              color={metric.impact === 'High' ? 'error' : 'warning'}
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

      {/* Collaboration Analysis Tab */}
      <TabPanel value={tabValue} index={2}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={8}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  Team Collaboration Trends
                </Typography>
                
                <ResponsiveContainer width="100%" height={400}>
                  <LineChart data={teamTrendData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis domain={[0, 100]} />
                    <RechartsTooltip />
                    <Line type="monotone" dataKey="collaboration" stroke="#4caf50" strokeWidth={2} name="Collaboration" />
                    <Line type="monotone" dataKey="communication" stroke="#2196f3" strokeWidth={2} name="Communication" />
                    <Line type="monotone" dataKey="productivity" stroke="#ff9800" strokeWidth={2} name="Productivity" />
                    <Line type="monotone" dataKey="satisfaction" stroke="#9c27b0" strokeWidth={2} name="Satisfaction" />
                    <Line type="monotone" dataKey="innovation" stroke="#f44336" strokeWidth={2} name="Innovation" />
                    <Line type="monotone" dataKey="support" stroke="#607d8b" strokeWidth={2} name="Support" />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  Collaboration vs Productivity
                </Typography>
                
                <ResponsiveContainer width="100%" height={300}>
                  <ScatterChart>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="number" dataKey="collaboration" name="Collaboration" domain={[0, 100]} />
                    <YAxis type="number" dataKey="productivity" name="Productivity" domain={[0, 100]} />
                    <RechartsTooltip cursor={{ strokeDasharray: '3 3' }} />
                    <Scatter name="Teams" data={collaborationScatterData} fill="#8884d8" />
                  </ScatterChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Interventions Tab */}
      <TabPanel value={tabValue} index={3}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  Team Interventions & Programs
                </Typography>
                
                <TableContainer component={Paper}>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Intervention</TableCell>
                        <TableCell>Team</TableCell>
                        <TableCell>Type</TableCell>
                        <TableCell>Status</TableCell>
                        <TableCell>Effectiveness</TableCell>
                        <TableCell>Participants</TableCell>
                        <TableCell>Actions</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {teamAnalyticsData.teamInterventions.map((intervention) => (
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
                            <Typography variant="body2">
                              {teamAnalyticsData.teams.find(t => t.id === intervention.teamId)?.name}
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
                              label={intervention.status}
                              color={intervention.status === 'completed' ? 'success' : intervention.status === 'active' ? 'warning' : 'default'}
                              size="small"
                            />
                          </TableCell>
                          <TableCell>
                            {intervention.effectiveness > 0 ? (
                              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                <Box sx={{ width: '100%', mr: 1 }}>
                                  <LinearProgress
                                    variant="determinate"
                                    value={intervention.effectiveness}
                                    color={getScoreColor(intervention.effectiveness) as any}
                                    sx={{ height: 8, borderRadius: 4 }}
                                  />
                                </Box>
                                <Typography variant="body2">
                                  {intervention.effectiveness}%
                                </Typography>
                              </Box>
                            ) : (
                              <Typography variant="body2" color="text.secondary">
                                Pending
                              </Typography>
                            )}
                          </TableCell>
                          <TableCell>
                            <Typography variant="body2">
                              {intervention.participants}
                            </Typography>
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
                  Team Performance Radar
                </Typography>
                
                <ResponsiveContainer width="100%" height={300}>
                  <RadarChart data={teamRadarData}>
                    <PolarGrid />
                    <PolarAngleAxis dataKey="metric" />
                    <PolarRadiusAxis domain={[0, 100]} />
                    <Radar
                      name="Team Score"
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
                  Team Comparison
                </Typography>
                
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={teamComparisonData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="team" angle={-45} textAnchor="end" height={80} />
                    <YAxis domain={[0, 100]} />
                    <RechartsTooltip />
                    <Bar dataKey="overall" fill="#8884d8" name="Overall Score" />
                    <Bar dataKey="wellness" fill="#4caf50" name="Wellness" />
                    <Bar dataKey="collaboration" fill="#ff9800" name="Collaboration" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  Team Correlation Analysis
                </Typography>
                
                <ResponsiveContainer width="100%" height={400}>
                  <ComposedChart data={teamTrendData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis yAxisId="left" domain={[0, 100]} />
                    <YAxis yAxisId="right" orientation="right" domain={[0, 100]} />
                    <RechartsTooltip />
                    <Area
                      yAxisId="left"
                      type="monotone"
                      dataKey="collaboration"
                      stroke="#4caf50"
                      fill="#4caf50"
                      fillOpacity={0.3}
                      name="Collaboration"
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

      {/* Floating Action Button */}
      <SpeedDial
        ariaLabel="Team Analytics Actions"
        sx={{ position: 'fixed', bottom: 16, right: 16 }}
        icon={<SpeedDialIcon />}
      >
        <SpeedDialAction
          icon={<Add />}
          tooltipTitle="Add Team"
          onClick={() => dispatch(addNotification({ message: 'Add team functionality', type: 'info' }))}
        />
        <SpeedDialAction
          icon={<GroupWork />}
          tooltipTitle="Team Building"
          onClick={() => dispatch(addNotification({ message: 'Team building initiated', type: 'success' }))}
        />
        <SpeedDialAction
          icon={<Support />}
          tooltipTitle="Support Request"
          onClick={() => dispatch(addNotification({ message: 'Support request sent', type: 'success' }))}
        />
        <SpeedDialAction
          icon={<Feedback />}
          tooltipTitle="Feedback"
          onClick={() => dispatch(addNotification({ message: 'Feedback collected', type: 'success' }))}
        />
      </SpeedDial>
    </Box>
  );
};

export default TeamAnalytics;
