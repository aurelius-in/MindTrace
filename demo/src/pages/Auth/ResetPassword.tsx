import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';

const ResetPassword: React.FC = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" sx={{ fontWeight: 600, mb: 3 }}>
        Reset Password
      </Typography>
      <Card>
        <CardContent>
          <Typography variant="body1">
            This is a demo version of the reset password page. In the full application, users would be able to set a new password after receiving a reset link.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default ResetPassword;
