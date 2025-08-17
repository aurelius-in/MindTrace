import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';

const Analytics: React.FC = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" sx={{ fontWeight: 600, mb: 3 }}>
        Analytics Overview
      </Typography>
      <Card>
        <CardContent>
          <Typography variant="body1">
            This is a demo version of the analytics overview page. In the full application, users would be able to view comprehensive analytics about organizational wellness, team performance, and individual wellness trends.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Analytics;
