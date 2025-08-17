import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  TextField,
  Button,
  Typography,
  Alert,
  CircularProgress,
  InputAdornment,
  IconButton,
  Fade,
  Zoom,
  useTheme,
  Card,
  CardContent,
  LinearProgress,
  Chip
} from '@mui/material';
import {
  Visibility,
  VisibilityOff,
  Lock,
  ArrowForward,
  Security,
  CheckCircle,
  Error,
  Refresh
} from '@mui/icons-material';
import { useNavigate, useSearchParams } from 'react-router-dom';

interface PasswordStrength {
  score: number;
  label: string;
  color: 'error' | 'warning' | 'info' | 'success';
}

const ResetPassword: React.FC = () => {
  const theme = useTheme();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  
  const [formData, setFormData] = useState({
    password: '',
    confirmPassword: ''
  });
  
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [formErrors, setFormErrors] = useState<{ password?: string; confirmPassword?: string }>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);
  const [showError, setShowError] = useState('');
  const [passwordStrength, setPasswordStrength] = useState<PasswordStrength>({
    score: 0,
    label: 'Very Weak',
    color: 'error'
  });

  // Get token from URL params
  const token = searchParams.get('token');

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

  // Handle input changes
  const handleInputChange = (field: 'password' | 'confirmPassword') => (
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
    const errors: { password?: string; confirmPassword?: string } = {};
    
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
    
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  // Handle form submission
  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    if (!token) {
      setShowError('Invalid reset token. Please request a new password reset.');
      return;
    }
    
    setIsSubmitting(true);
    setShowError('');
    
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // For demo purposes, show success
      setShowSuccess(true);
      
      // In a real implementation, you would call the API
      // const response = await api.post('/auth/reset-password', { 
      //   token, 
      //   password: formData.password 
      // });
      
    } catch (error) {
      setShowError('Failed to reset password. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  // Handle back to login
  const handleBackToLogin = () => {
    navigate('/login');
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
                  background: `linear-gradient(135deg, ${theme.palette.secondary.main} 0%, ${theme.palette.secondary.dark} 100%)`,
                  color: 'white',
                  padding: 3,
                  textAlign: 'center'
                }}
              >
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', mb: 2 }}>
                  <Refresh sx={{ fontSize: 40, mr: 1 }} />
                  <Typography variant="h4" component="h1" fontWeight="bold">
                    Set New Password
                  </Typography>
                </Box>
                <Typography variant="body1" sx={{ opacity: 0.9 }}>
                  Create a strong password for your account
                </Typography>
              </Box>

              {/* Form */}
              <Box sx={{ padding: 4 }}>
                {showError && (
                  <Alert severity="error" sx={{ mb: 3 }}>
                    {showError}
                  </Alert>
                )}

                {showSuccess ? (
                  <Box>
                    <Alert 
                      severity="success" 
                      icon={<CheckCircle />}
                      sx={{ mb: 3 }}
                    >
                      <Typography variant="h6" sx={{ mb: 1 }}>
                        Password Reset Successful!
                      </Typography>
                      <Typography variant="body2">
                        Your password has been updated. You can now sign in with your new password.
                      </Typography>
                    </Alert>

                    <Card sx={{ mb: 3, background: 'rgba(76, 175, 80, 0.04)', border: '1px solid rgba(76, 175, 80, 0.1)' }}>
                      <CardContent>
                        <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center' }}>
                          <Security sx={{ mr: 1, color: 'success.main' }} />
                          Security Tips
                        </Typography>
                        <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                          • Keep your password secure and don't share it
                        </Typography>
                        <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                          • Use different passwords for different accounts
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          • Consider using a password manager
                        </Typography>
                      </CardContent>
                    </Card>

                    <Button
                      fullWidth
                      variant="contained"
                      startIcon={<ArrowForward />}
                      onClick={handleBackToLogin}
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
                      Sign In Now
                    </Button>
                  </Box>
                ) : (
                  <Box>
                    <Typography variant="body1" color="text.secondary" sx={{ mb: 3, textAlign: 'center' }}>
                      Choose a strong password that you'll remember. Make sure it's at least 8 characters long and includes a mix of letters, numbers, and symbols.
                    </Typography>

                    <form onSubmit={handleSubmit}>
                      {/* New Password */}
                      <TextField
                        fullWidth
                        label="New Password"
                        type={showPassword ? 'text' : 'password'}
                        value={formData.password}
                        onChange={handleInputChange('password')}
                        error={!!formErrors.password}
                        helperText={formErrors.password}
                        disabled={isSubmitting}
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
                          mb: 2,
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
                        <Box sx={{ mb: 3 }}>
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

                      {/* Confirm Password */}
                      <TextField
                        fullWidth
                        label="Confirm New Password"
                        type={showConfirmPassword ? 'text' : 'password'}
                        value={formData.confirmPassword}
                        onChange={handleInputChange('confirmPassword')}
                        error={!!formErrors.confirmPassword}
                        helperText={formErrors.confirmPassword}
                        disabled={isSubmitting}
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
                          mb: 3,
                          '& .MuiOutlinedInput-root': {
                            borderRadius: 2,
                            '&:hover fieldset': {
                              borderColor: theme.palette.primary.main
                            }
                          }
                        }}
                      />

                      <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        size="large"
                        disabled={isSubmitting}
                        startIcon={isSubmitting ? <CircularProgress size={20} /> : <Refresh />}
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
                        {isSubmitting ? 'Updating Password...' : 'Update Password'}
                      </Button>
                    </form>

                    {/* Security Info Card */}
                    <Card sx={{ mt: 3, background: 'rgba(156, 39, 176, 0.04)', border: '1px solid rgba(156, 39, 176, 0.1)' }}>
                      <CardContent>
                        <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center' }}>
                          <Security sx={{ mr: 1, color: 'secondary.main' }} />
                          Password Requirements
                        </Typography>
                        <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                          • At least 8 characters long
                        </Typography>
                        <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                          • Include uppercase and lowercase letters
                        </Typography>
                        <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                          • Include at least one number
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          • Include at least one special character
                        </Typography>
                      </CardContent>
                    </Card>

                    {/* Back to Login */}
                    <Box sx={{ mt: 3, textAlign: 'center' }}>
                      <Button
                        variant="text"
                        onClick={handleBackToLogin}
                        sx={{
                          color: theme.palette.secondary.main,
                          textDecoration: 'none',
                          fontWeight: 'bold',
                          '&:hover': {
                            backgroundColor: 'rgba(156, 39, 176, 0.04)'
                          }
                        }}
                      >
                        Back to Login
                      </Button>
                    </Box>
                  </Box>
                )}
              </Box>
            </Paper>
          </Zoom>
        </Box>
      </Fade>
    </Box>
  );
};

export default ResetPassword;
