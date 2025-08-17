# Enterprise Employee Wellness AI - Demo

This is a demo version of the Enterprise Employee Wellness AI platform that showcases the user interface and functionality with realistic mock data.

## Features

- **Auto-login**: The demo automatically logs in with a sample user account
- **Realistic Mock Data**: Comprehensive mock data including users, wellness entries, resources, and analytics
- **Pre-loaded Search**: The Resources page comes pre-loaded with a search for "stress management techniques"
- **Full UI Navigation**: Complete navigation through all major sections of the application
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## Quick Start

1. **Install Dependencies**:
   ```bash
   cd demo
   npm install
   ```

2. **Start the Demo**:
   ```bash
   npm start
   ```

3. **Open in Browser**:
   The demo will open automatically at `http://localhost:3000`

## Demo Features

### Dashboard
- Overview of wellness metrics
- Quick action cards for main features
- Recent activity feed

### Resources
- Pre-loaded search for "stress management techniques"
- Filterable resource library
- Realistic resource cards with ratings and metadata

### Analytics (Manager/HR Access)
- Organizational health metrics
- Team analytics
- Risk assessment data

### Navigation
- Collapsible sidebar with role-based access
- Header with user profile and notifications
- Responsive design for all screen sizes

## Mock Data

The demo includes realistic mock data for:

- **Users**: Sample employees with different roles and departments
- **Wellness Entries**: Historical wellness check-ins with detailed metrics
- **Resources**: Wellness resources with ratings, categories, and descriptions
- **Analytics**: Organizational health data, team metrics, and risk assessments
- **Notifications**: Sample notifications and alerts

## Demo Credentials

The demo automatically logs in with:
- **Email**: sarah.johnson@techcorp.com
- **Role**: Employee
- **Department**: Engineering

## File Structure

```
demo/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── Common/
│   │   │   ├── LoadingSpinner.tsx
│   │   │   └── NotificationSystem.tsx
│   │   └── Layout/
│   │       ├── Header.tsx
│   │       └── Sidebar.tsx
│   ├── pages/
│   │   ├── Auth/
│   │   ├── Dashboard/
│   │   ├── Wellness/
│   │   ├── Resources/
│   │   ├── Analytics/
│   │   ├── Profile/
│   │   ├── Settings/
│   │   └── Compliance/
│   ├── store/
│   │   ├── slices/
│   │   └── index.ts
│   ├── App.tsx
│   ├── index.tsx
│   └── index.css
├── mock-data/
│   └── index.ts
├── package.json
└── README.md
```

## Customization

### Adding More Mock Data

Edit `mock-data/index.ts` to add:
- Additional users
- More wellness entries
- New resources
- Extended analytics data

### Modifying the UI

The demo uses Material-UI components and can be customized by:
- Updating theme colors in `src/index.tsx`
- Modifying component styles
- Adding new pages and routes

### Changing Pre-loaded Search

To change the pre-loaded search term, modify:
1. `mock-data/index.ts` - Update the `preloadedSearch.query`
2. `src/pages/Resources/Resources.tsx` - Update the initial `searchTerm` state

## Technical Details

- **Framework**: React 18 with TypeScript
- **UI Library**: Material-UI (MUI)
- **State Management**: Redux Toolkit
- **Routing**: React Router v6
- **Mock Data**: TypeScript interfaces with realistic data

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge

## Troubleshooting

### Common Issues

1. **Port 3000 in use**: The demo will automatically try port 3001
2. **Dependencies not found**: Run `npm install` again
3. **TypeScript errors**: Ensure all dependencies are properly installed

### Performance

The demo is optimized for performance with:
- Lazy loading of components
- Efficient state management
- Optimized mock data structures

## Next Steps

This demo showcases the UI and user experience. For the full application:

1. Connect to a real backend API
2. Implement actual authentication
3. Add real database integration
4. Deploy to production environment

## Support

For questions about the demo or the full application, please refer to the main project documentation.
