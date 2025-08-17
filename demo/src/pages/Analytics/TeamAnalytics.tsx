import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';

const TeamAnalytics: React.FC = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" sx={{ fontWeight: 600, mb: 3 }}>
        Team Analytics
      </Typography>
      <Card>
        <CardContent>
          <Typography variant="body1">
            This is a demo version of the team analytics page. In the full application, users would be able to view detailed team wellness metrics, member performance, collaboration patterns, and team-specific wellness insights.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default TeamAnalytics;
