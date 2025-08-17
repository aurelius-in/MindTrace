import React, { useState } from 'react';
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
  Fade,
  Zoom,
  useTheme,
  Card,
  CardContent,
  IconButton
} from '@mui/material';
import {
  Email,
  ArrowBack,
  ArrowForward,
  Security,
  CheckCircle,
  Info
} from '@mui/icons-material';
import { useNavigate, Link as RouterLink } from 'react-router-dom';

const ForgotPassword: React.FC = () => {
  const theme = useTheme();
  const navigate = useNavigate();
  
  const [email, setEmail] = useState('');
  const [emailError, setEmailError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);
  const [showError, setShowError] = useState('');

  // Handle email input change
  const handleEmailChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const value = event.target.value;
    setEmail(value);
    
    // Clear error when user starts typing
    if (emailError) {
      setEmailError('');
    }
  };

  // Validate email
  const validateEmail = (): boolean => {
    if (!email) {
      setEmailError('Email is required');
      return false;
    }
    
    if (!/\S+@\S+\.\S+/.test(email)) {
      setEmailError('Please enter a valid email address');
      return false;
    }
    
    return true;
  };

  // Handle form submission
  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    
    if (!validateEmail()) {
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
      // const response = await api.post('/auth/forgot-password', { email });
      
    } catch (error) {
      setShowError('Failed to send reset email. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  // Handle back to login
  const handleBackToLogin = () => {
    navigate('/login');
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
                    Reset Password
                  </Typography>
                </Box>
                <Typography variant="body1" sx={{ opacity: 0.9 }}>
                  Enter your email to receive reset instructions
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
                        Check Your Email
                      </Typography>
                      <Typography variant="body2">
                        We've sent password reset instructions to <strong>{email}</strong>
                      </Typography>
                    </Alert>

                    <Card sx={{ mb: 3, background: 'rgba(76, 175, 80, 0.04)', border: '1px solid rgba(76, 175, 80, 0.1)' }}>
                      <CardContent>
                        <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center' }}>
                          <Info sx={{ mr: 1, color: 'success.main' }} />
                          What's Next?
                        </Typography>
                        <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                          • Check your email inbox (and spam folder)
                        </Typography>
                        <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                          • Click the reset link in the email
                        </Typography>
                        <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                          • Create a new password
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          • Sign in with your new password
                        </Typography>
                      </CardContent>
                    </Card>

                    <Button
                      fullWidth
                      variant="outlined"
                      startIcon={<ArrowBack />}
                      onClick={handleBackToLogin}
                      sx={{
                        borderRadius: 2,
                        py: 1.5,
                        fontSize: '1.1rem',
                        fontWeight: 'bold',
                        borderColor: theme.palette.primary.main,
                        color: theme.palette.primary.main,
                        '&:hover': {
                          borderColor: theme.palette.primary.dark,
                          backgroundColor: 'rgba(25, 118, 210, 0.04)'
                        }
                      }}
                    >
                      Back to Login
                    </Button>
                  </Box>
                ) : (
                  <Box>
                    <Typography variant="body1" color="text.secondary" sx={{ mb: 3, textAlign: 'center' }}>
                      Don't worry! It happens to the best of us. Enter your email address and we'll send you a link to reset your password.
                    </Typography>

                    <form onSubmit={handleSubmit}>
                      <TextField
                        fullWidth
                        label="Email Address"
                        type="email"
                        value={email}
                        onChange={handleEmailChange}
                        error={!!emailError}
                        helperText={emailError}
                        disabled={isSubmitting}
                        InputProps={{
                          startAdornment: (
                            <InputAdornment position="start">
                              <Email color="primary" />
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
                        startIcon={isSubmitting ? <CircularProgress size={20} /> : <Email />}
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
                        {isSubmitting ? 'Sending...' : 'Send Reset Link'}
                      </Button>
                    </form>

                    {/* Security Info Card */}
                    <Card sx={{ mt: 3, background: 'rgba(25, 118, 210, 0.04)', border: '1px solid rgba(25, 118, 210, 0.1)' }}>
                      <CardContent>
                        <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center' }}>
                          <Security sx={{ mr: 1, color: 'primary.main' }} />
                          Security Notice
                        </Typography>
                        <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                          • Reset links expire in 1 hour
                        </Typography>
                        <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                          • Only request a reset if you own this email
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          • Contact support if you need assistance
                        </Typography>
                      </CardContent>
                    </Card>

                    {/* Back to Login */}
                    <Box sx={{ mt: 3, textAlign: 'center' }}>
                      <Button
                        variant="text"
                        startIcon={<ArrowBack />}
                        onClick={handleBackToLogin}
                        sx={{
                          color: theme.palette.primary.main,
                          textDecoration: 'none',
                          fontWeight: 'bold',
                          '&:hover': {
                            backgroundColor: 'rgba(25, 118, 210, 0.04)'
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

export default ForgotPassword;
