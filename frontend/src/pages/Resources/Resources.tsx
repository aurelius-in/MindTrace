import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';

const Resources: React.FC = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" sx={{ mb: 3, fontWeight: 600 }}>
        Wellness Resources
      </Typography>
      <Card>
        <CardContent>
          <Typography variant="body1">
            Wellness resources and recommendations will be displayed here.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Resources;
