import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';

const Settings: React.FC = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" sx={{ fontWeight: 600, mb: 3 }}>
        Settings
      </Typography>
      <Card>
        <CardContent>
          <Typography variant="body1">
            This is a demo version of the settings page. In the full application, users would be able to configure application settings, notification preferences, privacy settings, and other customization options.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Settings;
