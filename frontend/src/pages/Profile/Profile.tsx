import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';

const Profile: React.FC = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" sx={{ mb: 3, fontWeight: 600 }}>
        Profile
      </Typography>
      <Card>
        <CardContent>
          <Typography variant="body1">
            User profile and preferences will be displayed here.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Profile;
