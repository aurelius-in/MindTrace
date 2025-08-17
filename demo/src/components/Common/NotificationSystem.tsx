import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { Snackbar, Alert, AlertColor } from '@mui/material';
import { RootState } from '../../store';
import { removeNotification } from '../../store/slices/uiSlice';

const NotificationSystem: React.FC = () => {
  const dispatch = useDispatch();
  const notifications = useSelector((state: RootState) => state.ui.notifications);

  const handleClose = (id: string) => {
    dispatch(removeNotification(id));
  };

  const handleAutoClose = (id: string, duration: number = 6000) => {
    setTimeout(() => {
      dispatch(removeNotification(id));
    }, duration);
  };

  useEffect(() => {
    notifications.forEach(notification => {
      if (notification.duration && notification.duration > 0) {
        handleAutoClose(notification.id, notification.duration);
      }
    });
  }, [notifications]);

  if (notifications.length === 0) {
    return null;
  }

  const latestNotification = notifications[notifications.length - 1];

  return (
    <Snackbar
      open={notifications.length > 0}
      autoHideDuration={latestNotification.duration || 6000}
      onClose={() => handleClose(latestNotification.id)}
      anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
      sx={{ zIndex: 9999 }}
    >
      <Alert
        onClose={() => handleClose(latestNotification.id)}
        severity={latestNotification.type as AlertColor}
        variant="filled"
        sx={{ width: '100%' }}
      >
        {latestNotification.message}
      </Alert>
    </Snackbar>
  );
};

export default NotificationSystem;
