import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';

const Login: React.FC = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" sx={{ fontWeight: 600, mb: 3 }}>
        Login
      </Typography>
      <Card>
        <CardContent>
          <Typography variant="body1">
            This is a demo version of the login page. In the full application, users would be able to authenticate with their credentials to access the wellness platform.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Login;
