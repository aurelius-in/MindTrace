import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';

const WellnessHistory: React.FC = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" sx={{ mb: 3, fontWeight: 600 }}>
        Wellness History
      </Typography>
      <Card>
        <CardContent>
          <Typography variant="body1">
            Wellness history and trends will be displayed here.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default WellnessHistory;
