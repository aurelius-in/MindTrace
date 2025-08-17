import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';

const Profile: React.FC = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" sx={{ fontWeight: 600, mb: 3 }}>
        User Profile
      </Typography>
      <Card>
        <CardContent>
          <Typography variant="body1">
            This is a demo version of the user profile page. In the full application, users would be able to view and edit their profile information, wellness preferences, goals, and account settings.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Profile;
