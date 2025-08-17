git import React, { useState, useEffect } from 'react';
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
  Avatar,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Divider,
  Button,
  IconButton,
  Tooltip,
  Paper,
  Alert,
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  TrendingFlat,
  CalendarToday,
  FilterList,
  Download,
  Refresh,
  Mood,
  Psychology,
  FitnessCenter,
  LocalHospital,
  CheckCircle,
  Warning,
  Info,
  EmojiEmotions,
  SentimentVeryDissatisfied,
  SentimentDissatisfied,
  SentimentNeutral,
  SentimentSatisfied,
  SentimentVerySatisfied,
} from '@mui/icons-material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from 'recharts';
import { useDispatch, useSelector } from 'react-redux';
import { format, subDays, startOfDay, endOfDay, parseISO } from 'date-fns';

import { RootState } from '../../store';
import { fetchWellnessEntries, fetchConversations } from '../../store/slices/wellnessSlice';
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
    id={`wellness-tabpanel-${index}`}
    aria-labelledby={`wellness-tab-${index}`}
    {...other}
  >
    {value === index && <Box sx={{ pt: 3 }}>{children}</Box>}
  </div>
);

const WellnessHistory: React.FC = () => {
  const dispatch = useDispatch();
  const { entries, conversations, isLoading } = useSelector((state: RootState) => state.wellness);
  
  const [tabValue, setTabValue] = useState(0);
  const [timeframe, setTimeframe] = useState('30d');
  const [selectedEntryType, setSelectedEntryType] = useState('all');
  const [isRefreshing, setIsRefreshing] = useState(false);

  const entryTypes = [
    { value: 'all', label: 'All Metrics', icon: <CheckCircle /> },
    { value: 'mood', label: 'Mood', icon: <Mood /> },
    { value: 'stress', label: 'Stress', icon: <Psychology /> },
    { value: 'energy', label: 'Energy', icon: <FitnessCenter /> },
    { value: 'sleep_quality', label: 'Sleep Quality', icon: <LocalHospital /> },
    { value: 'work_life_balance', label: 'Work-Life Balance', icon: <EmojiEmotions /> },
  ];

  const timeframes = [
    { value: '7d', label: 'Last 7 Days' },
    { value: '30d', label: 'Last 30 Days' },
    { value: '90d', label: 'Last 90 Days' },
    { value: '6m', label: 'Last 6 Months' },
    { value: '1y', label: 'Last Year' },
  ];

  useEffect(() => {
    loadData();
  }, [timeframe]);

  const loadData = async () => {
    setIsRefreshing(true);
    try {
      await Promise.all([
        dispatch(fetchWellnessEntries()),
        dispatch(fetchConversations()),
      ]);
    } catch (error) {
      dispatch(addNotification({
        type: 'error',
        title: 'Data Load Failed',
        message: 'Failed to load wellness history data.',
      }));
    } finally {
      setIsRefreshing(false);
    }
  };

  const getFilteredEntries = () => {
    const daysToSubtract = timeframe === '7d' ? 7 : 
                          timeframe === '30d' ? 30 : 
                          timeframe === '90d' ? 90 : 
                          timeframe === '6m' ? 180 : 365;
    
    const cutoffDate = subDays(new Date(), daysToSubtract);
    
    return entries.filter(entry => {
      const entryDate = parseISO(entry.createdAt);
      const matchesType = selectedEntryType === 'all' || entry.entryType === selectedEntryType;
      const matchesTimeframe = entryDate >= cutoffDate;
      return matchesType && matchesTimeframe;
    }).sort((a, b) => parseISO(b.createdAt).getTime() - parseISO(a.createdAt).getTime());
  };

  const getChartData = () => {
    const filteredEntries = getFilteredEntries();
    const groupedData: { [key: string]: any[] } = {};

    filteredEntries.forEach(entry => {
      const date = format(parseISO(entry.createdAt), 'yyyy-MM-dd');
      if (!groupedData[date]) {
        groupedData[date] = [];
      }
      groupedData[date].push(entry);
    });

    return Object.entries(groupedData).map(([date, dayEntries]) => {
      const dataPoint: any = { date, name: format(parseISO(date), 'MMM dd') };
      
      // Calculate averages for each metric type
      const metrics = ['mood', 'stress', 'energy', 'sleep_quality', 'work_life_balance'];
      metrics.forEach(metric => {
        const metricEntries = dayEntries.filter(entry => entry.entryType === metric);
        if (metricEntries.length > 0) {
          const avg = metricEntries.reduce((sum, entry) => sum + entry.value, 0) / metricEntries.length;
          dataPoint[metric] = Math.round(avg * 10) / 10;
        }
      });

      return dataPoint;
    }).sort((a, b) => parseISO(a.date).getTime() - parseISO(b.date).getTime());
  };

  const getMoodDistribution = () => {
    const moodEntries = entries.filter(entry => entry.entryType === 'mood');
    const distribution = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 };
    
    moodEntries.forEach(entry => {
      const value = Math.round(entry.value);
      if (distribution[value as keyof typeof distribution] !== undefined) {
        distribution[value as keyof typeof distribution]++;
      }
    });

    return Object.entries(distribution).map(([value, count]) => ({
      name: getMoodLabel(parseInt(value)),
      value: count,
      color: getMoodColor(parseInt(value)),
    }));
  };

  const getMoodLabel = (value: number) => {
    const labels = ['Very Poor', 'Poor', 'Okay', 'Good', 'Excellent'];
    return labels[value - 1] || 'Okay';
  };

  const getMoodColor = (value: number) => {
    const colors = ['#f44336', '#ff9800', '#ffc107', '#4caf50', '#2196f3'];
    return colors[value - 1] || '#ffc107';
  };

  const getMoodIcon = (value: number) => {
    const icons = [
      <SentimentVeryDissatisfied key="1" color="error" />,
      <SentimentDissatisfied key="2" color="warning" />,
      <SentimentNeutral key="3" color="action" />,
      <SentimentSatisfied key="4" color="success" />,
      <SentimentVerySatisfied key="5" color="primary" />,
    ];
    return icons[value - 1] || icons[2];
  };

  const getTrendAnalysis = () => {
    const filteredEntries = getFilteredEntries();
    if (filteredEntries.length < 2) return { trend: 'stable', message: 'Not enough data for trend analysis' };

    const recentEntries = filteredEntries.slice(0, Math.floor(filteredEntries.length / 2));
    const olderEntries = filteredEntries.slice(Math.floor(filteredEntries.length / 2));

    const recentAvg = recentEntries.reduce((sum, entry) => sum + entry.value, 0) / recentEntries.length;
    const olderAvg = olderEntries.reduce((sum, entry) => sum + entry.value, 0) / olderEntries.length;

    const difference = recentAvg - olderAvg;
    const percentageChange = (difference / olderAvg) * 100;

    if (Math.abs(percentageChange) < 5) {
      return { trend: 'stable', message: 'Your wellness has remained stable', percentageChange };
    } else if (percentageChange > 0) {
      return { trend: 'improving', message: 'Your wellness is improving!', percentageChange };
    } else {
      return { trend: 'declining', message: 'Your wellness needs attention', percentageChange };
    }
  };

  const getInsights = () => {
    const insights = [];
    const filteredEntries = getFilteredEntries();

    if (filteredEntries.length === 0) {
      insights.push('Start tracking your wellness to see insights here.');
      return insights;
    }

    // Most common entry type
    const entryTypeCounts: { [key: string]: number } = {};
    filteredEntries.forEach(entry => {
      entryTypeCounts[entry.entryType] = (entryTypeCounts[entry.entryType] || 0) + 1;
    });

    const mostTracked = Object.entries(entryTypeCounts).sort((a, b) => b[1] - a[1])[0];
    insights.push(`You track ${mostTracked[0].replace('_', ' ')} most frequently (${mostTracked[1]} times).`);

    // Average values
    const metrics = ['mood', 'stress', 'energy', 'sleep_quality', 'work_life_balance'];
    metrics.forEach(metric => {
      const metricEntries = filteredEntries.filter(entry => entry.entryType === metric);
      if (metricEntries.length > 0) {
        const avg = metricEntries.reduce((sum, entry) => sum + entry.value, 0) / metricEntries.length;
        insights.push(`Average ${metric.replace('_', ' ')}: ${avg.toFixed(1)}/10`);
      }
    });

    // Consistency
    const daysWithEntries = new Set(filteredEntries.map(entry => format(parseISO(entry.createdAt), 'yyyy-MM-dd'))).size;
    const totalDays = timeframe === '7d' ? 7 : timeframe === '30d' ? 30 : timeframe === '90d' ? 90 : timeframe === '6m' ? 180 : 365;
    const consistency = (daysWithEntries / totalDays) * 100;
    insights.push(`You've tracked ${consistency.toFixed(0)}% of days in this period.`);

    return insights;
  };

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleRefresh = () => {
    loadData();
  };

  const handleExport = () => {
    const filteredEntries = getFilteredEntries();
    const csvContent = [
      ['Date', 'Type', 'Value', 'Description', 'Tags'].join(','),
      ...filteredEntries.map(entry => [
        format(parseISO(entry.createdAt), 'yyyy-MM-dd HH:mm:ss'),
        entry.entryType,
        entry.value,
        entry.description || '',
        entry.tags?.join(';') || ''
      ].join(','))
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `wellness-history-${timeframe}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);

    dispatch(addNotification({
      type: 'success',
      title: 'Export Complete',
      message: 'Your wellness history has been exported successfully.',
    }));
  };

  const chartData = getChartData();
  const moodDistribution = getMoodDistribution();
  const trendAnalysis = getTrendAnalysis();
  const insights = getInsights();

  if (isLoading) {
    return <LoadingSpinner message="Loading wellness history..." />;
  }

  return (
    <Box sx={{ p: 3, maxWidth: 1400, mx: 'auto' }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" sx={{ fontWeight: 600, color: 'primary.main' }}>
          Wellness History
        </Typography>
        
        <Box sx={{ display: 'flex', gap: 2 }}>
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
                <InputLabel>Entry Type</InputLabel>
                <Select
                  value={selectedEntryType}
                  onChange={(e) => setSelectedEntryType(e.target.value)}
                  label="Entry Type"
                >
                  {entryTypes.map((type) => (
                    <MenuItem key={type.value} value={type.value}>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        {type.icon}
                        <Typography sx={{ ml: 1 }}>{type.label}</Typography>
                      </Box>
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12} md={4}>
              <Typography variant="body2" color="text.secondary">
                {getFilteredEntries().length} entries found
              </Typography>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Trend Analysis */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            {trendAnalysis.trend === 'improving' && <TrendingUp color="success" />}
            {trendAnalysis.trend === 'declining' && <TrendingDown color="error" />}
            {trendAnalysis.trend === 'stable' && <TrendingFlat color="action" />}
            <Typography variant="h6" sx={{ ml: 1, fontWeight: 600 }}>
              Trend Analysis
            </Typography>
          </Box>
          
          <Alert 
            severity={trendAnalysis.trend === 'improving' ? 'success' : 
                     trendAnalysis.trend === 'declining' ? 'warning' : 'info'}
            sx={{ mb: 2 }}
          >
            {trendAnalysis.message}
            {trendAnalysis.percentageChange && (
              <Typography variant="body2" sx={{ mt: 1 }}>
                Change: {trendAnalysis.percentageChange > 0 ? '+' : ''}{trendAnalysis.percentageChange.toFixed(1)}%
              </Typography>
            )}
          </Alert>
        </CardContent>
      </Card>

      {/* Tabs */}
      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={tabValue} onChange={handleTabChange} aria-label="wellness history tabs">
          <Tab label="Trends" />
          <Tab label="Mood Distribution" />
          <Tab label="Recent Entries" />
          <Tab label="Insights" />
        </Tabs>
      </Box>

      {/* Trends Tab */}
      <TabPanel value={tabValue} index={0}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                  Wellness Trends Over Time
                </Typography>
                
                {chartData.length > 0 ? (
                  <ResponsiveContainer width="100%" height={400}>
                    <LineChart data={chartData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" />
                      <YAxis domain={[0, 10]} />
                      <RechartsTooltip />
                      <Line type="monotone" dataKey="mood" stroke="#2196f3" strokeWidth={2} name="Mood" />
                      <Line type="monotone" dataKey="stress" stroke="#f44336" strokeWidth={2} name="Stress" />
                      <Line type="monotone" dataKey="energy" stroke="#4caf50" strokeWidth={2} name="Energy" />
                      <Line type="monotone" dataKey="sleep_quality" stroke="#9c27b0" strokeWidth={2} name="Sleep Quality" />
                      <Line type="monotone" dataKey="work_life_balance" stroke="#ff9800" strokeWidth={2} name="Work-Life Balance" />
                    </LineChart>
                  </ResponsiveContainer>
                ) : (
                  <Box sx={{ textAlign: 'center', py: 4 }}>
                    <Typography variant="body1" color="text.secondary">
                      No data available for the selected timeframe and filters.
                    </Typography>
                  </Box>
                )}
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Mood Distribution Tab */}
      <TabPanel value={tabValue} index={1}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                  Mood Distribution
                </Typography>
                
                {moodDistribution.some(item => item.value > 0) ? (
                  <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                      <Pie
                        data={moodDistribution}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="value"
                      >
                        {moodDistribution.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <RechartsTooltip />
                    </PieChart>
                  </ResponsiveContainer>
                ) : (
                  <Box sx={{ textAlign: 'center', py: 4 }}>
                    <Typography variant="body1" color="text.secondary">
                      No mood data available for the selected timeframe.
                    </Typography>
                  </Box>
                )}
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                  Mood Summary
                </Typography>
                
                <List>
                  {moodDistribution.map((item, index) => (
                    <ListItem key={index}>
                      <ListItemAvatar>
                        <Avatar sx={{ bgcolor: item.color }}>
                          {getMoodIcon(index + 1)}
                        </Avatar>
                      </ListItemAvatar>
                      <ListItemText
                        primary={item.name}
                        secondary={`${item.value} entries`}
                      />
                      <Chip 
                        label={`${((item.value / moodDistribution.reduce((sum, i) => sum + i.value, 0)) * 100).toFixed(1)}%`}
                        size="small"
                      />
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Recent Entries Tab */}
      <TabPanel value={tabValue} index={2}>
        <Card>
          <CardContent>
            <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
              Recent Entries
            </Typography>
            
            {getFilteredEntries().length > 0 ? (
              <List>
                {getFilteredEntries().slice(0, 20).map((entry, index) => (
                  <React.Fragment key={entry.id}>
                    <ListItem>
                      <ListItemAvatar>
                        <Avatar sx={{ bgcolor: 'primary.main' }}>
                          {entryTypes.find(type => type.value === entry.entryType)?.icon || <CheckCircle />}
                        </Avatar>
                      </ListItemAvatar>
                      <ListItemText
                        primary={
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                              {entryTypes.find(type => type.value === entry.entryType)?.label}
                            </Typography>
                            <Chip 
                              label={`${entry.value}/10`}
                              size="small"
                              color={entry.value >= 7 ? 'success' : entry.value >= 4 ? 'warning' : 'error'}
                            />
                          </Box>
                        }
                        secondary={
                          <Box>
                            <Typography variant="body2" color="text.secondary">
                              {format(parseISO(entry.createdAt), 'MMM dd, yyyy HH:mm')}
                            </Typography>
                            {entry.description && (
                              <Typography variant="body2" sx={{ mt: 1 }}>
                                {entry.description}
                              </Typography>
                            )}
                            {entry.tags && entry.tags.length > 0 && (
                              <Box sx={{ display: 'flex', gap: 1, mt: 1 }}>
                                {entry.tags.map((tag, tagIndex) => (
                                  <Chip
                                    key={tagIndex}
                                    label={tag.replace('-', ' ')}
                                    size="small"
                                    variant="outlined"
                                  />
                                ))}
                              </Box>
                            )}
                          </Box>
                        }
                      />
                    </ListItem>
                    {index < getFilteredEntries().slice(0, 20).length - 1 && <Divider />}
                  </React.Fragment>
                ))}
              </List>
            ) : (
              <Box sx={{ textAlign: 'center', py: 4 }}>
                <Typography variant="body1" color="text.secondary">
                  No entries found for the selected filters.
                </Typography>
              </Box>
            )}
          </CardContent>
        </Card>
      </TabPanel>

      {/* Insights Tab */}
      <TabPanel value={tabValue} index={3}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                  Wellness Insights
                </Typography>
                
                <List>
                  {insights.map((insight, index) => (
                    <ListItem key={index}>
                      <ListItemAvatar>
                        <Avatar sx={{ bgcolor: 'primary.main' }}>
                          <Info />
                        </Avatar>
                      </ListItemAvatar>
                      <ListItemText primary={insight} />
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>
    </Box>
  );
};

export default WellnessHistory;
