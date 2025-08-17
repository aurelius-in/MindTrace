import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';

const WellnessChat: React.FC = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" sx={{ mb: 3, fontWeight: 600 }}>
        Wellness Chat
      </Typography>
      <Card>
        <CardContent>
          <Typography variant="body1">
            AI wellness chat functionality will be implemented here.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default WellnessChat;
