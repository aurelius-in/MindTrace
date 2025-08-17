import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';

const RiskAssessment: React.FC = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" sx={{ fontWeight: 600, mb: 3 }}>
        Risk Assessment
      </Typography>
      <Card>
        <CardContent>
          <Typography variant="body1">
            This is a demo version of the risk assessment page. In the full application, users would be able to view detailed risk assessments, identify potential wellness issues, and access recommendations for risk mitigation.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default RiskAssessment;
