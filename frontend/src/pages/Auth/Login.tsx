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
  useMediaQuery
} from '@mui/material';
import {
  Visibility,
  VisibilityOff,
  Email,
  Lock,
  Google,
  Microsoft,
  GitHub,
  Login as LoginIcon,
  ArrowForward,
  Security,
  VerifiedUser
} from '@mui/icons-material';
import { useNavigate, Link as RouterLink } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { login } from '../../store/slices/authSlice';
import { RootState } from '../../store';

interface LoginFormData {
  email: string;
  password: string;
}

const Login: React.FC = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const navigate = useNavigate();
  const dispatch = useDispatch();
  
  const { loading, error, user } = useSelector((state: RootState) => state.auth);
  
  const [formData, setFormData] = useState<LoginFormData>({
    email: '',
    password: ''
  });
  
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);
  const [formErrors, setFormErrors] = useState<Partial<LoginFormData>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);

  // Redirect if already logged in
  useEffect(() => {
    if (user) {
      navigate('/dashboard');
    }
  }, [user, navigate]);

  // Handle form input changes
  const handleInputChange = (field: keyof LoginFormData) => (
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
    const errors: Partial<LoginFormData> = {};
    
    if (!formData.email) {
      errors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      errors.email = 'Please enter a valid email address';
    }
    
    if (!formData.password) {
      errors.password = 'Password is required';
    } else if (formData.password.length < 6) {
      errors.password = 'Password must be at least 6 characters';
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
      const result = await dispatch(login({
        email: formData.email,
        password: formData.password,
        rememberMe
      }) as any);
      
      if (login.fulfilled.match(result)) {
        setShowSuccess(true);
        setTimeout(() => {
          navigate('/dashboard');
        }, 1000);
      }
    } catch (err) {
      console.error('Login failed:', err);
    } finally {
      setIsSubmitting(false);
    }
  };

  // Handle social login
  const handleSocialLogin = (provider: string) => {
    // In a real implementation, this would redirect to OAuth provider
    console.log(`Logging in with ${provider}`);
    // For demo purposes, show a message
    alert(`${provider} login would be implemented here`);
  };

  // Handle password visibility toggle
  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        background: `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.secondary.main} 100%)`,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: 2
      }}
    >
      <Fade in timeout={800}>
        <Box sx={{ width: '100%', maxWidth: 450 }}>
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
                  background: `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.primary.dark} 100%)`,
                  color: 'white',
                  padding: 3,
                  textAlign: 'center'
                }}
              >
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', mb: 2 }}>
                  <Security sx={{ fontSize: 40, mr: 1 }} />
                  <Typography variant="h4" component="h1" fontWeight="bold">
                    Welcome Back
                  </Typography>
                </Box>
                <Typography variant="body1" sx={{ opacity: 0.9 }}>
                  Sign in to your Enterprise Wellness account
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
                    Login successful! Redirecting to dashboard...
                  </Alert>
                )}

                <form onSubmit={handleSubmit}>
                  <Grid container spacing={3}>
                    {/* Email Field */}
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

                    {/* Password Field */}
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
                    </Grid>

                    {/* Remember Me & Forgot Password */}
                    <Grid item xs={12}>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <Link
                          component={RouterLink}
                          to="/forgot-password"
                          variant="body2"
                          sx={{
                            color: theme.palette.primary.main,
                            textDecoration: 'none',
                            '&:hover': {
                              textDecoration: 'underline'
                            }
                          }}
                        >
                          Forgot your password?
                        </Link>
                      </Box>
                    </Grid>

                    {/* Login Button */}
                    <Grid item xs={12}>
                      <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        size="large"
                        disabled={isSubmitting || loading}
                        startIcon={isSubmitting ? <CircularProgress size={20} /> : <LoginIcon />}
                        endIcon={!isSubmitting && <ArrowForward />}
                        sx={{
                          borderRadius: 2,
                          py: 1.5,
                          fontSize: '1.1rem',
                          fontWeight: 'bold',
                          background: `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.primary.dark} 100%)`,
                          '&:hover': {
                            background: `linear-gradient(135deg, ${theme.palette.primary.dark} 0%, ${theme.palette.primary.main} 100%)`,
                            transform: 'translateY(-2px)',
                            boxShadow: theme.shadows[8]
                          },
                          transition: 'all 0.3s ease'
                        }}
                      >
                        {isSubmitting ? 'Signing In...' : 'Sign In'}
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

                {/* Social Login Buttons */}
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={4}>
                    <Button
                      fullWidth
                      variant="outlined"
                      startIcon={<Google />}
                      onClick={() => handleSocialLogin('Google')}
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
                      onClick={() => handleSocialLogin('Microsoft')}
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
                      onClick={() => handleSocialLogin('GitHub')}
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

                {/* Features Card */}
                <Card sx={{ mt: 3, background: 'rgba(25, 118, 210, 0.04)', border: '1px solid rgba(25, 118, 210, 0.1)' }}>
                  <CardContent>
                    <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center' }}>
                      <VerifiedUser sx={{ mr: 1, color: 'primary.main' }} />
                      Enterprise Features
                    </Typography>
                    <Grid container spacing={1}>
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">
                          • AI-Powered Wellness Chat
                        </Typography>
                      </Grid>
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">
                          • Advanced Analytics
                        </Typography>
                      </Grid>
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">
                          • Team Insights
                        </Typography>
                      </Grid>
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">
                          • Privacy Controls
                        </Typography>
                      </Grid>
                    </Grid>
                  </CardContent>
                </Card>

                {/* Sign Up Link */}
                <Box sx={{ mt: 3, textAlign: 'center' }}>
                  <Typography variant="body2" color="text.secondary">
                    Don't have an account?{' '}
                    <Link
                      component={RouterLink}
                      to="/register"
                      sx={{
                        color: theme.palette.primary.main,
                        textDecoration: 'none',
                        fontWeight: 'bold',
                        '&:hover': {
                          textDecoration: 'underline'
                        }
                      }}
                    >
                      Sign up here
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

export default Login;
