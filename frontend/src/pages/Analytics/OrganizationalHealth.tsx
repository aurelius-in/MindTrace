import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';

const OrganizationalHealth: React.FC = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" sx={{ mb: 3, fontWeight: 600 }}>
        Organizational Health
      </Typography>
      <Card>
        <CardContent>
          <Typography variant="body1">
            Organizational health metrics will be displayed here.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default OrganizationalHealth;
