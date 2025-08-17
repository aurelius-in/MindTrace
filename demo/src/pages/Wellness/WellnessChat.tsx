import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';

const WellnessChat: React.FC = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" sx={{ fontWeight: 600, mb: 3 }}>
        AI Wellness Chat
      </Typography>
      <Card>
        <CardContent>
          <Typography variant="body1">
            This is a demo version of the AI wellness chat page. In the full application, users would be able to have conversations with an AI wellness companion that provides personalized support and guidance.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default WellnessChat;
