import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import wellnessReducer from './slices/wellnessSlice';
import analyticsReducer from './slices/analyticsSlice';
import uiReducer from './slices/uiSlice';
import resourcesReducer from './slices/resourcesSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    wellness: wellnessReducer,
    analytics: analyticsReducer,
    ui: uiReducer,
    resources: resourcesReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST', 'persist/REHYDRATE'],
      },
    }),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
