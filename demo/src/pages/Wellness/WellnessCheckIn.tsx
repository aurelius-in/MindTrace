import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';

const WellnessCheckIn: React.FC = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" sx={{ fontWeight: 600, mb: 3 }}>
        Wellness Check-in
      </Typography>
      <Card>
        <CardContent>
          <Typography variant="body1">
            This is a demo version of the wellness check-in page. In the full application, users would be able to complete comprehensive wellness assessments, track their mood, stress levels, and other wellness metrics.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default WellnessCheckIn;
