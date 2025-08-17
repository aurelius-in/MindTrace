import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';

const ResourceDetail: React.FC = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" sx={{ fontWeight: 600, mb: 3 }}>
        Resource Details
      </Typography>
      <Card>
        <CardContent>
          <Typography variant="body1">
            This is a demo version of the resource detail page. In the full application, users would be able to view detailed information about wellness resources, including content, ratings, reviews, and related materials.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default ResourceDetail;
