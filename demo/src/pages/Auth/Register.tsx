import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';

const Register: React.FC = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" sx={{ fontWeight: 600, mb: 3 }}>
        Register
      </Typography>
      <Card>
        <CardContent>
          <Typography variant="body1">
            This is a demo version of the register page. In the full application, users would be able to create new accounts and set up their wellness profiles.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Register;
