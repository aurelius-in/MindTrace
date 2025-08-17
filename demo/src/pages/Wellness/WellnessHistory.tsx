import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';

const WellnessHistory: React.FC = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" sx={{ fontWeight: 600, mb: 3 }}>
        Wellness History
      </Typography>
      <Card>
        <CardContent>
          <Typography variant="body1">
            This is a demo version of the wellness history page. In the full application, users would be able to view their wellness check-in history, track trends over time, and see detailed analytics of their wellness journey.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default WellnessHistory;
