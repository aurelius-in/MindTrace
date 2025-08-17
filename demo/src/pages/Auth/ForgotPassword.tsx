import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';

const ForgotPassword: React.FC = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" sx={{ fontWeight: 600, mb: 3 }}>
        Forgot Password
      </Typography>
      <Card>
        <CardContent>
          <Typography variant="body1">
            This is a demo version of the forgot password page. In the full application, users would be able to reset their passwords through email verification.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default ForgotPassword;
