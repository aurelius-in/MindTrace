import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';

const TeamAnalytics: React.FC = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" sx={{ mb: 3, fontWeight: 600 }}>
        Team Analytics
      </Typography>
      <Card>
        <CardContent>
          <Typography variant="body1">
            Team wellness analytics will be displayed here.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default TeamAnalytics;
