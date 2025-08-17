import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';

const Settings: React.FC = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" sx={{ mb: 3, fontWeight: 600 }}>
        Settings
      </Typography>
      <Card>
        <CardContent>
          <Typography variant="body1">
            Application settings and configuration will be displayed here.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Settings;
