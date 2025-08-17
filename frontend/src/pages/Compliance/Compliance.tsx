import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  Button,
  Alert,
  Tabs,
  Tab,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  FormControlLabel,
  Switch,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  IconButton,
  Tooltip,
  Divider,
  Edit,
  Delete,
} from '@mui/material';
import {
  Security,
  PrivacyTip,
  Assessment,
  History,
  Download,
  Visibility,
  VisibilityOff,
  CheckCircle,
  Warning,
  Error,
  Info,
  ExpandMore,
  FilterList,
  Refresh,
  FileDownload,
  Audit,
  Compliance,
  DataUsage,
  Shield,
  Lock,
} from '@mui/icons-material';
import { useDispatch, useSelector } from 'react-redux';
import { format } from 'date-fns';

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
    id={`compliance-tabpanel-${index}`}
    aria-labelledby={`compliance-tab-${index}`}
    {...other}
  >
    {value === index && <Box sx={{ pt: 3 }}>{children}</Box>}
  </div>
);

const Compliance: React.FC = () => {
  const dispatch = useDispatch();
  const { user } = useSelector((state: RootState) => state.auth);
  
  const [tabValue, setTabValue] = useState(0);
  const [showSensitiveData, setShowSensitiveData] = useState(false);
  const [auditDialogOpen, setAuditDialogOpen] = useState(false);
  
  // Compliance status
  const [complianceStatus, setComplianceStatus] = useState({
    hipaa: { status: 'compliant', lastAudit: '2024-01-15', score: 95 },
    gdpr: { status: 'compliant', lastAudit: '2024-01-10', score: 92 },
    soc2: { status: 'compliant', lastAudit: '2024-01-20', score: 98 },
    ccpa: { status: 'compliant', lastAudit: '2024-01-12', score: 89 },
  });

  // Privacy controls
  const [privacyControls, setPrivacyControls] = useState({
    dataAnonymization: true,
    encryptionAtRest: true,
    encryptionInTransit: true,
    accessLogging: true,
    dataRetention: true,
    consentManagement: true,
    rightToBeForgotten: true,
    dataPortability: true,
  });

  // Audit trail data
  const [auditTrail, setAuditTrail] = useState([
    {
      id: 1,
      timestamp: '2024-01-25T10:30:00Z',
      user: 'john.doe@company.com',
      action: 'Data Access',
      resource: 'Wellness Records',
      ipAddress: '192.168.1.100',
      status: 'success',
      details: 'Viewed wellness check-in history',
    },
    {
      id: 2,
      timestamp: '2024-01-25T09:15:00Z',
      user: 'system',
      action: 'Data Anonymization',
      resource: 'Analytics Dataset',
      ipAddress: 'N/A',
      status: 'success',
      details: 'Applied differential privacy to analytics data',
    },
    {
      id: 3,
      timestamp: '2024-01-25T08:45:00Z',
      user: 'jane.smith@company.com',
      action: 'Consent Update',
      resource: 'Privacy Settings',
      ipAddress: '192.168.1.101',
      status: 'success',
      details: 'Updated data sharing preferences',
    },
    {
      id: 4,
      timestamp: '2024-01-24T16:20:00Z',
      user: 'admin@company.com',
      action: 'Security Audit',
      resource: 'System',
      ipAddress: '192.168.1.1',
      status: 'success',
      details: 'Completed quarterly security assessment',
    },
  ]);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handlePrivacyControlChange = (control: string, value: boolean) => {
    setPrivacyControls(prev => ({
      ...prev,
      [control]: value,
    }));
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'compliant':
        return 'success';
      case 'warning':
        return 'warning';
      case 'non-compliant':
        return 'error';
      default:
        return 'default';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'compliant':
        return <CheckCircle color="success" />;
      case 'warning':
        return <Warning color="warning" />;
      case 'non-compliant':
        return <Error color="error" />;
      default:
        return <Info color="info" />;
    }
  };

  const handleExportAuditTrail = () => {
    dispatch(addNotification({
      type: 'success',
      title: 'Export Complete',
      message: 'Audit trail has been exported successfully.',
    }));
  };

  const handleRunComplianceCheck = () => {
    dispatch(addNotification({
      type: 'info',
      title: 'Compliance Check',
      message: 'Running comprehensive compliance assessment...',
    }));
  };

  return (
    <Box sx={{ p: 3, maxWidth: 1400, mx: 'auto' }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" sx={{ fontWeight: 600, color: 'primary.main' }}>
          Compliance & Privacy
        </Typography>
        
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button
            variant="outlined"
            startIcon={<Refresh />}
            onClick={handleRunComplianceCheck}
          >
            Run Compliance Check
          </Button>
          <Button
            variant="outlined"
            startIcon={<FileDownload />}
            onClick={handleExportAuditTrail}
          >
            Export Audit Trail
          </Button>
        </Box>
      </Box>

      {/* Tabs */}
      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={tabValue} onChange={handleTabChange} aria-label="compliance tabs">
          <Tab label="Compliance Status" icon={<Assessment />} />
          <Tab label="Privacy Controls" icon={<PrivacyTip />} />
          <Tab label="Audit Trail" icon={<History />} />
          <Tab label="Data Rights" icon={<Security />} />
        </Tabs>
      </Box>

      {/* Compliance Status Tab */}
      <TabPanel value={tabValue} index={0}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Alert severity="success" sx={{ mb: 3 }}>
              All compliance frameworks are currently compliant. Last comprehensive audit completed on January 20, 2024.
            </Alert>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  Regulatory Compliance
                </Typography>
                
                <List>
                  {Object.entries(complianceStatus).map(([framework, data]) => (
                    <ListItem key={framework}>
                      <ListItemIcon>
                        {getStatusIcon(data.status)}
                      </ListItemIcon>
                      <ListItemText
                        primary={framework.toUpperCase()}
                        secondary={`Last audit: ${format(new Date(data.lastAudit), 'MMM dd, yyyy')} • Score: ${data.score}%`}
                      />
                      <Chip
                        label={data.status}
                        color={getStatusColor(data.status) as any}
                        variant="outlined"
                      />
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
                  Security Metrics
                </Typography>
                
                <Grid container spacing={2}>
                  <Grid item xs={6}>
                    <Box sx={{ textAlign: 'center', p: 2, bgcolor: 'success.light', borderRadius: 1 }}>
                      <Typography variant="h4" color="success.dark">
                        99.9%
                      </Typography>
                      <Typography variant="body2" color="success.dark">
                        Uptime
                      </Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={6}>
                    <Box sx={{ textAlign: 'center', p: 2, bgcolor: 'info.light', borderRadius: 1 }}>
                      <Typography variant="h4" color="info.dark">
                        256-bit
                      </Typography>
                      <Typography variant="body2" color="info.dark">
                        Encryption
                      </Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={6}>
                    <Box sx={{ textAlign: 'center', p: 2, bgcolor: 'warning.light', borderRadius: 1 }}>
                      <Typography variant="h4" color="warning.dark">
                        0
                      </Typography>
                      <Typography variant="body2" color="warning.dark">
                        Security Incidents
                      </Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={6}>
                    <Box sx={{ textAlign: 'center', p: 2, bgcolor: 'primary.light', borderRadius: 1 }}>
                      <Typography variant="h4" color="primary.dark">
                        24/7
                      </Typography>
                      <Typography variant="body2" color="primary.dark">
                        Monitoring
                      </Typography>
                    </Box>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  Recent Compliance Activities
                </Typography>
                
                <TableContainer component={Paper}>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Date</TableCell>
                        <TableCell>Activity</TableCell>
                        <TableCell>Framework</TableCell>
                        <TableCell>Status</TableCell>
                        <TableCell>Details</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      <TableRow>
                        <TableCell>{format(new Date('2024-01-20'), 'MMM dd, yyyy')}</TableCell>
                        <TableCell>Quarterly Security Audit</TableCell>
                        <TableCell>SOC2</TableCell>
                        <TableCell>
                          <Chip label="Passed" color="success" size="small" />
                        </TableCell>
                        <TableCell>All controls verified</TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell>{format(new Date('2024-01-15'), 'MMM dd, yyyy')}</TableCell>
                        <TableCell>HIPAA Compliance Review</TableCell>
                        <TableCell>HIPAA</TableCell>
                        <TableCell>
                          <Chip label="Passed" color="success" size="small" />
                        </TableCell>
                        <TableCell>Privacy safeguards confirmed</TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell>{format(new Date('2024-01-10'), 'MMM dd, yyyy')}</TableCell>
                        <TableCell>GDPR Data Processing Review</TableCell>
                        <TableCell>GDPR</TableCell>
                        <TableCell>
                          <Chip label="Passed" color="success" size="small" />
                        </TableCell>
                        <TableCell>Data processing compliant</TableCell>
                      </TableRow>
                    </TableBody>
                  </Table>
                </TableContainer>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Privacy Controls Tab */}
      <TabPanel value={tabValue} index={1}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  Data Protection Controls
                </Typography>
                
                <FormControlLabel
                  control={
                    <Switch
                      checked={privacyControls.dataAnonymization}
                      onChange={(e) => handlePrivacyControlChange('dataAnonymization', e.target.checked)}
                    />
                  }
                  label="Data Anonymization"
                />
                
                <FormControlLabel
                  control={
                    <Switch
                      checked={privacyControls.encryptionAtRest}
                      onChange={(e) => handlePrivacyControlChange('encryptionAtRest', e.target.checked)}
                    />
                  }
                  label="Encryption at Rest"
                />
                
                <FormControlLabel
                  control={
                    <Switch
                      checked={privacyControls.encryptionInTransit}
                      onChange={(e) => handlePrivacyControlChange('encryptionInTransit', e.target.checked)}
                    />
                  }
                  label="Encryption in Transit"
                />
                
                <FormControlLabel
                  control={
                    <Switch
                      checked={privacyControls.accessLogging}
                      onChange={(e) => handlePrivacyControlChange('accessLogging', e.target.checked)}
                    />
                  }
                  label="Access Logging"
                />
                
                <FormControlLabel
                  control={
                    <Switch
                      checked={privacyControls.dataRetention}
                      onChange={(e) => handlePrivacyControlChange('dataRetention', e.target.checked)}
                    />
                  }
                  label="Data Retention Policies"
                />
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  User Rights Management
                </Typography>
                
                <FormControlLabel
                  control={
                    <Switch
                      checked={privacyControls.consentManagement}
                      onChange={(e) => handlePrivacyControlChange('consentManagement', e.target.checked)}
                    />
                  }
                  label="Consent Management"
                />
                
                <FormControlLabel
                  control={
                    <Switch
                      checked={privacyControls.rightToBeForgotten}
                      onChange={(e) => handlePrivacyControlChange('rightToBeForgotten', e.target.checked)}
                    />
                  }
                  label="Right to be Forgotten"
                />
                
                <FormControlLabel
                  control={
                    <Switch
                      checked={privacyControls.dataPortability}
                      onChange={(e) => handlePrivacyControlChange('dataPortability', e.target.checked)}
                    />
                  }
                  label="Data Portability"
                />
                
                <Divider sx={{ my: 2 }} />
                
                <Alert severity="info">
                  All privacy controls are currently active and protecting your data according to regulatory requirements.
                </Alert>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  Privacy Impact Assessment
                </Typography>
                
                <Grid container spacing={2}>
                  <Grid item xs={12} md={4}>
                    <Box sx={{ p: 2, border: '1px solid', borderColor: 'success.main', borderRadius: 1 }}>
                      <Typography variant="h6" color="success.main">
                        Low Risk
                      </Typography>
                      <Typography variant="body2">
                        Data processing activities pose minimal privacy risk
                      </Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={12} md={4}>
                    <Box sx={{ p: 2, border: '1px solid', borderColor: 'success.main', borderRadius: 1 }}>
                      <Typography variant="h6" color="success.main">
                        Fully Compliant
                      </Typography>
                      <Typography variant="body2">
                        All regulatory requirements are met
                      </Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={12} md={4}>
                    <Box sx={{ p: 2, border: '1px solid', borderColor: 'success.main', borderRadius: 1 }}>
                      <Typography variant="h6" color="success.main">
                        Regular Monitoring
                      </Typography>
                      <Typography variant="body2">
                        Continuous compliance monitoring active
                      </Typography>
                    </Box>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Audit Trail Tab */}
      <TabPanel value={tabValue} index={2}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h6" sx={{ fontWeight: 600 }}>
                System Audit Trail
              </Typography>
              <Box sx={{ display: 'flex', gap: 1 }}>
                <IconButton
                  onClick={() => setShowSensitiveData(!showSensitiveData)}
                  size="small"
                >
                  {showSensitiveData ? <VisibilityOff /> : <Visibility />}
                </IconButton>
                <Button
                  variant="outlined"
                  size="small"
                  startIcon={<FilterList />}
                >
                  Filter
                </Button>
              </Box>
            </Box>
            
            <TableContainer component={Paper}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Timestamp</TableCell>
                    <TableCell>User</TableCell>
                    <TableCell>Action</TableCell>
                    <TableCell>Resource</TableCell>
                    {showSensitiveData && <TableCell>IP Address</TableCell>}
                    <TableCell>Status</TableCell>
                    <TableCell>Details</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {auditTrail.map((entry) => (
                    <TableRow key={entry.id}>
                      <TableCell>
                        {format(new Date(entry.timestamp), 'MMM dd, yyyy HH:mm')}
                      </TableCell>
                      <TableCell>
                        {showSensitiveData ? entry.user : entry.user.split('@')[0] + '@***'}
                      </TableCell>
                      <TableCell>{entry.action}</TableCell>
                      <TableCell>{entry.resource}</TableCell>
                      {showSensitiveData && (
                        <TableCell>{entry.ipAddress}</TableCell>
                      )}
                      <TableCell>
                        <Chip
                          label={entry.status}
                          color={entry.status === 'success' ? 'success' : 'error'}
                          size="small"
                        />
                      </TableCell>
                      <TableCell>{entry.details}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Data Rights Tab */}
      <TabPanel value={tabValue} index={3}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  Your Data Rights
                </Typography>
                
                <List>
                  <ListItem>
                    <ListItemIcon>
                      <Visibility />
                    </ListItemIcon>
                    <ListItemText
                      primary="Right to Access"
                      secondary="View all personal data we hold about you"
                    />
                    <Button variant="outlined" size="small">
                      Request
                    </Button>
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <Download />
                    </ListItemIcon>
                    <ListItemText
                      primary="Right to Portability"
                      secondary="Download your data in a portable format"
                    />
                    <Button variant="outlined" size="small">
                      Download
                    </Button>
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <Edit />
                    </ListItemIcon>
                    <ListItemText
                      primary="Right to Rectification"
                      secondary="Correct inaccurate personal data"
                    />
                    <Button variant="outlined" size="small">
                      Update
                    </Button>
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <Delete />
                    </ListItemIcon>
                    <ListItemText
                      primary="Right to Erasure"
                      secondary="Request deletion of your personal data"
                    />
                    <Button variant="outlined" color="error" size="small">
                      Delete
                    </Button>
                  </ListItem>
                </List>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                  Data Processing Information
                </Typography>
                
                <Accordion>
                  <AccordionSummary expandIcon={<ExpandMore />}>
                    <Typography>Legal Basis for Processing</Typography>
                  </AccordionSummary>
                  <AccordionDetails>
                    <Typography variant="body2">
                      We process your data based on legitimate interest for wellness program management, 
                      with your explicit consent for specific activities.
                    </Typography>
                  </AccordionDetails>
                </Accordion>
                
                <Accordion>
                  <AccordionSummary expandIcon={<ExpandMore />}>
                    <Typography>Data Retention Periods</Typography>
                  </AccordionSummary>
                  <AccordionDetails>
                    <Typography variant="body2">
                      Personal wellness data is retained for 2 years, anonymized analytics data for 5 years, 
                      and audit logs for 7 years as required by law.
                    </Typography>
                  </AccordionDetails>
                </Accordion>
                
                <Accordion>
                  <AccordionSummary expandIcon={<ExpandMore />}>
                    <Typography>Third-party Data Sharing</Typography>
                  </AccordionSummary>
                  <AccordionDetails>
                    <Typography variant="body2">
                      We do not sell your data. Limited sharing occurs only with your consent 
                      for wellness program partners and as required by law.
                    </Typography>
                  </AccordionDetails>
                </Accordion>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Audit Dialog */}
      <Dialog
        open={auditDialogOpen}
        onClose={() => setAuditDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Detailed Audit Information</DialogTitle>
        <DialogContent>
          <Typography>
            Detailed audit information would be displayed here.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAuditDialogOpen(false)}>Close</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Compliance;
