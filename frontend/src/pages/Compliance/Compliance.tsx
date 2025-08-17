import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';

const Compliance: React.FC = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" sx={{ mb: 3, fontWeight: 600 }}>
        Compliance & Privacy
      </Typography>
      <Card>
        <CardContent>
          <Typography variant="body1">
            Compliance monitoring and privacy controls will be displayed here.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Compliance;
