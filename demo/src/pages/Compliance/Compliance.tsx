import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';

const Compliance: React.FC = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" sx={{ fontWeight: 600, mb: 3 }}>
        Compliance & Privacy
      </Typography>
      <Card>
        <CardContent>
          <Typography variant="body1">
            This is a demo version of the compliance page. In the full application, users would be able to view compliance reports, privacy settings, audit trails, and data management options.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Compliance;
