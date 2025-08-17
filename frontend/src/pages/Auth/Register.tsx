import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  TextField,
  Button,
  Typography,
  Link,
  Alert,
  CircularProgress,
  InputAdornment,
  IconButton,
  Divider,
  Grid,
  Card,
  CardContent,
  Fade,
  Zoom,
  useTheme,
  useMediaQuery,
  FormControlLabel,
  Checkbox,
  LinearProgress,
  Chip
} from '@mui/material';
import {
  Visibility,
  VisibilityOff,
  Email,
  Lock,
  Person,
  Business,
  Phone,
  Google,
  Microsoft,
  GitHub,
  PersonAdd,
  ArrowForward,
  Security,
  VerifiedUser,
  CheckCircle,
  Error
} from '@mui/icons-material';
import { useNavigate, Link as RouterLink } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { register } from '../../store/slices/authSlice';
import { RootState } from '../../store';

interface RegisterFormData {
  firstName: string;
  lastName: string;
  email: string;
  password: string;
  confirmPassword: string;
  company: string;
  phone: string;
  department: string;
  position: string;
}

interface PasswordStrength {
  score: number;
  label: string;
  color: 'error' | 'warning' | 'info' | 'success';
}

const Register: React.FC = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const navigate = useNavigate();
  const dispatch = useDispatch();
  
  const { loading, error, user } = useSelector((state: RootState) => state.auth);
  
  const [formData, setFormData] = useState<RegisterFormData>({
    firstName: '',
    lastName: '',
    email: '',
    password: '',
    confirmPassword: '',
    company: '',
    phone: '',
    department: '',
    position: ''
  });
  
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [acceptTerms, setAcceptTerms] = useState(false);
  const [acceptPrivacy, setAcceptPrivacy] = useState(false);
  const [formErrors, setFormErrors] = useState<Partial<RegisterFormData>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);
  const [passwordStrength, setPasswordStrength] = useState<PasswordStrength>({
    score: 0,
    label: 'Very Weak',
    color: 'error'
  });

  // Redirect if already logged in
  useEffect(() => {
    if (user) {
      navigate('/dashboard');
    }
  }, [user, navigate]);

  // Calculate password strength
  useEffect(() => {
    const calculatePasswordStrength = (password: string): PasswordStrength => {
      let score = 0;
      let label = 'Very Weak';
      let color: 'error' | 'warning' | 'info' | 'success' = 'error';

      if (password.length >= 8) score += 1;
      if (/[a-z]/.test(password)) score += 1;
      if (/[A-Z]/.test(password)) score += 1;
      if (/[0-9]/.test(password)) score += 1;
      if (/[^A-Za-z0-9]/.test(password)) score += 1;

      if (score >= 5) {
        label = 'Very Strong';
        color = 'success';
      } else if (score >= 4) {
        label = 'Strong';
        color = 'success';
      } else if (score >= 3) {
        label = 'Good';
        color = 'info';
      } else if (score >= 2) {
        label = 'Fair';
        color = 'warning';
      } else {
        label = 'Weak';
        color = 'error';
      }

      return { score, label, color };
    };

    setPasswordStrength(calculatePasswordStrength(formData.password));
  }, [formData.password]);

  // Handle form input changes
  const handleInputChange = (field: keyof RegisterFormData) => (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const value = event.target.value;
    setFormData(prev => ({ ...prev, [field]: value }));
    
    // Clear error when user starts typing
    if (formErrors[field]) {
      setFormErrors(prev => ({ ...prev, [field]: undefined }));
    }
  };

  // Validate form
  const validateForm = (): boolean => {
    const errors: Partial<RegisterFormData> = {};
    
    if (!formData.firstName.trim()) {
      errors.firstName = 'First name is required';
    }
    
    if (!formData.lastName.trim()) {
      errors.lastName = 'Last name is required';
    }
    
    if (!formData.email) {
      errors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      errors.email = 'Please enter a valid email address';
    }
    
    if (!formData.password) {
      errors.password = 'Password is required';
    } else if (formData.password.length < 8) {
      errors.password = 'Password must be at least 8 characters';
    } else if (passwordStrength.score < 3) {
      errors.password = 'Password is too weak';
    }
    
    if (!formData.confirmPassword) {
      errors.confirmPassword = 'Please confirm your password';
    } else if (formData.password !== formData.confirmPassword) {
      errors.confirmPassword = 'Passwords do not match';
    }
    
    if (!formData.company.trim()) {
      errors.company = 'Company name is required';
    }
    
    if (!formData.department.trim()) {
      errors.department = 'Department is required';
    }
    
    if (!formData.position.trim()) {
      errors.position = 'Position is required';
    }
    
    if (!acceptTerms) {
      // This would be handled differently in a real form
      console.warn('Terms must be accepted');
    }
    
    if (!acceptPrivacy) {
      // This would be handled differently in a real form
      console.warn('Privacy policy must be accepted');
    }
    
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  // Handle form submission
  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    setIsSubmitting(true);
    
    try {
      const result = await dispatch(register({
        firstName: formData.firstName,
        lastName: formData.lastName,
        email: formData.email,
        password: formData.password,
        company: formData.company,
        phone: formData.phone,
        department: formData.department,
        position: formData.position
      }) as any);
      
      if (register.fulfilled.match(result)) {
        setShowSuccess(true);
        setTimeout(() => {
          navigate('/dashboard');
        }, 2000);
      }
    } catch (err) {
      console.error('Registration failed:', err);
    } finally {
      setIsSubmitting(false);
    }
  };

  // Handle social registration
  const handleSocialRegister = (provider: string) => {
    console.log(`Registering with ${provider}`);
    alert(`${provider} registration would be implemented here`);
  };

  // Toggle password visibility
  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  const toggleConfirmPasswordVisibility = () => {
    setShowConfirmPassword(!showConfirmPassword);
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        background: `linear-gradient(135deg, ${theme.palette.secondary.main} 0%, ${theme.palette.primary.main} 100%)`,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: 2
      }}
    >
      <Fade in timeout={800}>
        <Box sx={{ width: '100%', maxWidth: 600 }}>
          <Zoom in timeout={1000}>
            <Paper
              elevation={24}
              sx={{
                borderRadius: 3,
                overflow: 'hidden',
                background: 'rgba(255, 255, 255, 0.95)',
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255, 255, 255, 0.2)'
              }}
            >
              {/* Header */}
              <Box
                sx={{
                  background: `linear-gradient(135deg, ${theme.palette.secondary.main} 0%, ${theme.palette.secondary.dark} 100%)`,
                  color: 'white',
                  padding: 3,
                  textAlign: 'center'
                }}
              >
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', mb: 2 }}>
                  <PersonAdd sx={{ fontSize: 40, mr: 1 }} />
                  <Typography variant="h4" component="h1" fontWeight="bold">
                    Join Enterprise Wellness
                  </Typography>
                </Box>
                <Typography variant="body1" sx={{ opacity: 0.9 }}>
                  Create your account and start your wellness journey
                </Typography>
              </Box>

              {/* Form */}
              <Box sx={{ padding: 4 }}>
                {error && (
                  <Alert severity="error" sx={{ mb: 3 }}>
                    {error}
                  </Alert>
                )}

                {showSuccess && (
                  <Alert severity="success" sx={{ mb: 3 }}>
                    Registration successful! Welcome to Enterprise Wellness. Redirecting to dashboard...
                  </Alert>
                )}

                <form onSubmit={handleSubmit}>
                  <Grid container spacing={3}>
                    {/* Name Fields */}
                    <Grid item xs={12} sm={6}>
                      <TextField
                        fullWidth
                        label="First Name"
                        value={formData.firstName}
                        onChange={handleInputChange('firstName')}
                        error={!!formErrors.firstName}
                        helperText={formErrors.firstName}
                        InputProps={{
                          startAdornment: (
                            <InputAdornment position="start">
                              <Person color="primary" />
                            </InputAdornment>
                          )
                        }}
                        sx={{
                          '& .MuiOutlinedInput-root': {
                            borderRadius: 2,
                            '&:hover fieldset': {
                              borderColor: theme.palette.primary.main
                            }
                          }
                        }}
                      />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <TextField
                        fullWidth
                        label="Last Name"
                        value={formData.lastName}
                        onChange={handleInputChange('lastName')}
                        error={!!formErrors.lastName}
                        helperText={formErrors.lastName}
                        sx={{
                          '& .MuiOutlinedInput-root': {
                            borderRadius: 2,
                            '&:hover fieldset': {
                              borderColor: theme.palette.primary.main
                            }
                          }
                        }}
                      />
                    </Grid>

                    {/* Email */}
                    <Grid item xs={12}>
                      <TextField
                        fullWidth
                        label="Email Address"
                        type="email"
                        value={formData.email}
                        onChange={handleInputChange('email')}
                        error={!!formErrors.email}
                        helperText={formErrors.email}
                        InputProps={{
                          startAdornment: (
                            <InputAdornment position="start">
                              <Email color="primary" />
                            </InputAdornment>
                          )
                        }}
                        sx={{
                          '& .MuiOutlinedInput-root': {
                            borderRadius: 2,
                            '&:hover fieldset': {
                              borderColor: theme.palette.primary.main
                            }
                          }
                        }}
                      />
                    </Grid>

                    {/* Company Info */}
                    <Grid item xs={12} sm={6}>
                      <TextField
                        fullWidth
                        label="Company"
                        value={formData.company}
                        onChange={handleInputChange('company')}
                        error={!!formErrors.company}
                        helperText={formErrors.company}
                        InputProps={{
                          startAdornment: (
                            <InputAdornment position="start">
                              <Business color="primary" />
                            </InputAdornment>
                          )
                        }}
                        sx={{
                          '& .MuiOutlinedInput-root': {
                            borderRadius: 2,
                            '&:hover fieldset': {
                              borderColor: theme.palette.primary.main
                            }
                          }
                        }}
                      />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <TextField
                        fullWidth
                        label="Phone (Optional)"
                        value={formData.phone}
                        onChange={handleInputChange('phone')}
                        InputProps={{
                          startAdornment: (
                            <InputAdornment position="start">
                              <Phone color="primary" />
                            </InputAdornment>
                          )
                        }}
                        sx={{
                          '& .MuiOutlinedInput-root': {
                            borderRadius: 2,
                            '&:hover fieldset': {
                              borderColor: theme.palette.primary.main
                            }
                          }
                        }}
                      />
                    </Grid>

                    {/* Department and Position */}
                    <Grid item xs={12} sm={6}>
                      <TextField
                        fullWidth
                        label="Department"
                        value={formData.department}
                        onChange={handleInputChange('department')}
                        error={!!formErrors.department}
                        helperText={formErrors.department}
                        sx={{
                          '& .MuiOutlinedInput-root': {
                            borderRadius: 2,
                            '&:hover fieldset': {
                              borderColor: theme.palette.primary.main
                            }
                          }
                        }}
                      />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <TextField
                        fullWidth
                        label="Position"
                        value={formData.position}
                        onChange={handleInputChange('position')}
                        error={!!formErrors.position}
                        helperText={formErrors.position}
                        sx={{
                          '& .MuiOutlinedInput-root': {
                            borderRadius: 2,
                            '&:hover fieldset': {
                              borderColor: theme.palette.primary.main
                            }
                          }
                        }}
                      />
                    </Grid>

                    {/* Password */}
                    <Grid item xs={12}>
                      <TextField
                        fullWidth
                        label="Password"
                        type={showPassword ? 'text' : 'password'}
                        value={formData.password}
                        onChange={handleInputChange('password')}
                        error={!!formErrors.password}
                        helperText={formErrors.password}
                        InputProps={{
                          startAdornment: (
                            <InputAdornment position="start">
                              <Lock color="primary" />
                            </InputAdornment>
                          ),
                          endAdornment: (
                            <InputAdornment position="end">
                              <IconButton
                                onClick={togglePasswordVisibility}
                                edge="end"
                                size="small"
                              >
                                {showPassword ? <VisibilityOff /> : <Visibility />}
                              </IconButton>
                            </InputAdornment>
                          )
                        }}
                        sx={{
                          '& .MuiOutlinedInput-root': {
                            borderRadius: 2,
                            '&:hover fieldset': {
                              borderColor: theme.palette.primary.main
                            }
                          }
                        }}
                      />
                      
                      {/* Password Strength Indicator */}
                      {formData.password && (
                        <Box sx={{ mt: 1 }}>
                          <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                            <LinearProgress
                              variant="determinate"
                              value={(passwordStrength.score / 5) * 100}
                              color={passwordStrength.color}
                              sx={{ flex: 1, mr: 1, height: 6, borderRadius: 3 }}
                            />
                            <Chip
                              label={passwordStrength.label}
                              color={passwordStrength.color}
                              size="small"
                              icon={passwordStrength.score >= 4 ? <CheckCircle /> : <Error />}
                            />
                          </Box>
                          <Typography variant="caption" color="text.secondary">
                            Password must be at least 8 characters with uppercase, lowercase, number, and special character
                          </Typography>
                        </Box>
                      )}
                    </Grid>

                    {/* Confirm Password */}
                    <Grid item xs={12}>
                      <TextField
                        fullWidth
                        label="Confirm Password"
                        type={showConfirmPassword ? 'text' : 'password'}
                        value={formData.confirmPassword}
                        onChange={handleInputChange('confirmPassword')}
                        error={!!formErrors.confirmPassword}
                        helperText={formErrors.confirmPassword}
                        InputProps={{
                          startAdornment: (
                            <InputAdornment position="start">
                              <Lock color="primary" />
                            </InputAdornment>
                          ),
                          endAdornment: (
                            <InputAdornment position="end">
                              <IconButton
                                onClick={toggleConfirmPasswordVisibility}
                                edge="end"
                                size="small"
                              >
                                {showConfirmPassword ? <VisibilityOff /> : <Visibility />}
                              </IconButton>
                            </InputAdornment>
                          )
                        }}
                        sx={{
                          '& .MuiOutlinedInput-root': {
                            borderRadius: 2,
                            '&:hover fieldset': {
                              borderColor: theme.palette.primary.main
                            }
                          }
                        }}
                      />
                    </Grid>

                    {/* Terms and Privacy */}
                    <Grid item xs={12}>
                      <Box sx={{ mt: 2 }}>
                        <FormControlLabel
                          control={
                            <Checkbox
                              checked={acceptTerms}
                              onChange={(e) => setAcceptTerms(e.target.checked)}
                              color="primary"
                            />
                          }
                          label={
                            <Typography variant="body2">
                              I agree to the{' '}
                              <Link href="#" sx={{ color: theme.palette.primary.main }}>
                                Terms of Service
                              </Link>
                            </Typography>
                          }
                        />
                        <FormControlLabel
                          control={
                            <Checkbox
                              checked={acceptPrivacy}
                              onChange={(e) => setAcceptPrivacy(e.target.checked)}
                              color="primary"
                            />
                          }
                          label={
                            <Typography variant="body2">
                              I agree to the{' '}
                              <Link href="#" sx={{ color: theme.palette.primary.main }}>
                                Privacy Policy
                              </Link>
                            </Typography>
                          }
                        />
                      </Box>
                    </Grid>

                    {/* Register Button */}
                    <Grid item xs={12}>
                      <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        size="large"
                        disabled={isSubmitting || loading || !acceptTerms || !acceptPrivacy}
                        startIcon={isSubmitting ? <CircularProgress size={20} /> : <PersonAdd />}
                        endIcon={!isSubmitting && <ArrowForward />}
                        sx={{
                          borderRadius: 2,
                          py: 1.5,
                          fontSize: '1.1rem',
                          fontWeight: 'bold',
                          background: `linear-gradient(135deg, ${theme.palette.secondary.main} 0%, ${theme.palette.secondary.dark} 100%)`,
                          '&:hover': {
                            background: `linear-gradient(135deg, ${theme.palette.secondary.dark} 0%, ${theme.palette.secondary.main} 100%)`,
                            transform: 'translateY(-2px)',
                            boxShadow: theme.shadows[8]
                          },
                          transition: 'all 0.3s ease'
                        }}
                      >
                        {isSubmitting ? 'Creating Account...' : 'Create Account'}
                      </Button>
                    </Grid>
                  </Grid>
                </form>

                {/* Divider */}
                <Box sx={{ my: 3, display: 'flex', alignItems: 'center' }}>
                  <Divider sx={{ flex: 1 }} />
                  <Typography variant="body2" sx={{ mx: 2, color: 'text.secondary' }}>
                    OR
                  </Typography>
                  <Divider sx={{ flex: 1 }} />
                </Box>

                {/* Social Registration Buttons */}
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={4}>
                    <Button
                      fullWidth
                      variant="outlined"
                      startIcon={<Google />}
                      onClick={() => handleSocialRegister('Google')}
                      sx={{
                        borderRadius: 2,
                        py: 1.5,
                        borderColor: '#DB4437',
                        color: '#DB4437',
                        '&:hover': {
                          borderColor: '#DB4437',
                          backgroundColor: 'rgba(219, 68, 55, 0.04)'
                        }
                      }}
                    >
                      Google
                    </Button>
                  </Grid>
                  <Grid item xs={12} sm={4}>
                    <Button
                      fullWidth
                      variant="outlined"
                      startIcon={<Microsoft />}
                      onClick={() => handleSocialRegister('Microsoft')}
                      sx={{
                        borderRadius: 2,
                        py: 1.5,
                        borderColor: '#00A4EF',
                        color: '#00A4EF',
                        '&:hover': {
                          borderColor: '#00A4EF',
                          backgroundColor: 'rgba(0, 164, 239, 0.04)'
                        }
                      }}
                    >
                      Microsoft
                    </Button>
                  </Grid>
                  <Grid item xs={12} sm={4}>
                    <Button
                      fullWidth
                      variant="outlined"
                      startIcon={<GitHub />}
                      onClick={() => handleSocialRegister('GitHub')}
                      sx={{
                        borderRadius: 2,
                        py: 1.5,
                        borderColor: '#333',
                        color: '#333',
                        '&:hover': {
                          borderColor: '#333',
                          backgroundColor: 'rgba(51, 51, 51, 0.04)'
                        }
                      }}
                    >
                      GitHub
                    </Button>
                  </Grid>
                </Grid>

                {/* Benefits Card */}
                <Card sx={{ mt: 3, background: 'rgba(156, 39, 176, 0.04)', border: '1px solid rgba(156, 39, 176, 0.1)' }}>
                  <CardContent>
                    <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center' }}>
                      <VerifiedUser sx={{ mr: 1, color: 'secondary.main' }} />
                      What You'll Get
                    </Typography>
                    <Grid container spacing={1}>
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">
                          • Personalized Wellness Insights
                        </Typography>
                      </Grid>
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">
                          • AI-Powered Recommendations
                        </Typography>
                      </Grid>
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">
                          • Team Collaboration Tools
                        </Typography>
                      </Grid>
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">
                          • Advanced Analytics Dashboard
                        </Typography>
                      </Grid>
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">
                          • Privacy-First Design
                        </Typography>
                      </Grid>
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">
                          • 24/7 Support Access
                        </Typography>
                      </Grid>
                    </Grid>
                  </CardContent>
                </Card>

                {/* Sign In Link */}
                <Box sx={{ mt: 3, textAlign: 'center' }}>
                  <Typography variant="body2" color="text.secondary">
                    Already have an account?{' '}
                    <Link
                      component={RouterLink}
                      to="/login"
                      sx={{
                        color: theme.palette.secondary.main,
                        textDecoration: 'none',
                        fontWeight: 'bold',
                        '&:hover': {
                          textDecoration: 'underline'
                        }
                      }}
                    >
                      Sign in here
                    </Link>
                  </Typography>
                </Box>
              </Box>
            </Paper>
          </Zoom>
        </Box>
      </Fade>
    </Box>
  );
};

export default Register;
