import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';

const OrganizationalHealth: React.FC = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" sx={{ fontWeight: 600, mb: 3 }}>
        Organizational Health
      </Typography>
      <Card>
        <CardContent>
          <Typography variant="body1">
            This is a demo version of the organizational health page. In the full application, users would be able to view comprehensive organizational wellness metrics, department performance, and company-wide wellness initiatives.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default OrganizationalHealth;
