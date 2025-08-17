import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';

const ResourceDetail: React.FC = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" sx={{ mb: 3, fontWeight: 600 }}>
        Resource Details
      </Typography>
      <Card>
        <CardContent>
          <Typography variant="body1">
            Detailed resource information will be displayed here.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default ResourceDetail;
