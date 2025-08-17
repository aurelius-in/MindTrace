// Mock data for Enterprise Employee Wellness AI Demo
// This file contains realistic mock data that simulates a real application environment

export interface MockUser {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  role: 'employee' | 'manager' | 'admin' | 'hr';
  department: string;
  position: string;
  company: string;
  avatar_url?: string;
  is_active: boolean;
  is_verified: boolean;
  hire_date: string;
  timezone: string;
  language: string;
  preferences: Record<string, any>;
  wellness_profile: {
    goals: string[];
    interests: string[];
    challenges: string[];
  };
}

export interface MockWellnessEntry {
  id: string;
  user_id: string;
  entry_type: 'comprehensive' | 'quick_mood';
  value: number;
  description: string;
  mood_score: number;
  stress_score: number;
  energy_score: number;
  sleep_hours: number;
  sleep_quality: number;
  work_life_balance: number;
  social_support: number;
  physical_activity: number;
  nutrition_quality: number;
  productivity_level: number;
  tags: string[];
  factors: Record<string, any>;
  recommendations: string[];
  risk_indicators: string[];
  is_anonymous: boolean;
  created_at: string;
}

export interface MockResource {
  id: string;
  title: string;
  description: string;
  category: string;
  difficulty_level: 'beginner' | 'intermediate' | 'advanced';
  duration_minutes: number;
  tags: string[];
  author: string;
  content_url: string;
  thumbnail_url?: string;
  is_active: boolean;
  view_count: number;
  rating: number;
  rating_count: number;
  created_at: string;
}

export interface MockAnalytics {
  organizational_health: {
    overall_score: number;
    trend: 'improving' | 'stable' | 'declining';
    departments: Array<{
      name: string;
      score: number;
      trend: string;
      employee_count: number;
    }>;
    kpis: Array<{
      name: string;
      value: number;
      target: number;
      status: 'good' | 'warning' | 'critical';
    }>;
  };
  team_analytics: {
    team_id: string;
    team_name: string;
    wellness_score: number;
    engagement_score: number;
    productivity_score: number;
    collaboration_score: number;
    members: Array<{
      user_id: string;
      name: string;
      role: string;
      wellness_score: number;
      participation_rate: number;
    }>;
    trends: Array<{
      date: string;
      wellness_score: number;
      engagement_score: number;
    }>;
  };
  risk_assessment: {
    overall_risk_level: 'low' | 'medium' | 'high';
    risk_factors: Array<{
      factor: string;
      severity: 'low' | 'medium' | 'high';
      impact: number;
      recommendations: string[];
    }>;
    trends: Array<{
      date: string;
      risk_level: string;
      risk_score: number;
    }>;
  };
}

export interface MockNotification {
  id: string;
  user_id: string;
  title: string;
  message: string;
  notification_type: 'info' | 'warning' | 'success' | 'error';
  priority: 'low' | 'medium' | 'high';
  is_read: boolean;
  created_at: string;
  metadata?: Record<string, any>;
}

export interface MockConversation {
  id: string;
  user_id: string;
  messages: Array<{
    id: string;
    role: 'user' | 'assistant';
    content: string;
    timestamp: string;
    metadata?: Record<string, any>;
  }>;
  summary?: string;
  created_at: string;
  updated_at: string;
}

// Mock Users
export const mockUsers: MockUser[] = [
  {
    id: '1',
    email: 'sarah.johnson@techcorp.com',
    first_name: 'Sarah',
    last_name: 'Johnson',
    role: 'employee',
    department: 'Engineering',
    position: 'Senior Software Engineer',
    company: 'TechCorp',
    avatar_url: 'https://images.unsplash.com/photo-1494790108755-2616b612b786?w=150&h=150&fit=crop&crop=face',
    is_active: true,
    is_verified: true,
    hire_date: '2022-03-15',
    timezone: 'America/New_York',
    language: 'en',
    preferences: {
      notifications: {
        email: true,
        push: true,
        sms: false
      },
      privacy: {
        anonymous_checkins: false,
        share_analytics: true
      }
    },
    wellness_profile: {
      goals: ['Reduce stress', 'Improve work-life balance', 'Better sleep'],
      interests: ['Meditation', 'Exercise', 'Nutrition'],
      challenges: ['Long work hours', 'Screen time', 'Sedentary lifestyle']
    }
  },
  {
    id: '2',
    email: 'michael.chen@techcorp.com',
    first_name: 'Michael',
    last_name: 'Chen',
    role: 'manager',
    department: 'Engineering',
    position: 'Engineering Manager',
    company: 'TechCorp',
    avatar_url: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face',
    is_active: true,
    is_verified: true,
    hire_date: '2021-08-20',
    timezone: 'America/Los_Angeles',
    language: 'en',
    preferences: {
      notifications: {
        email: true,
        push: false,
        sms: false
      },
      privacy: {
        anonymous_checkins: false,
        share_analytics: true
      }
    },
    wellness_profile: {
      goals: ['Team wellness', 'Leadership development', 'Stress management'],
      interests: ['Team building', 'Leadership', 'Wellness programs'],
      challenges: ['Team management', 'Work-life balance', 'Decision making']
    }
  },
  {
    id: '3',
    email: 'emily.rodriguez@techcorp.com',
    first_name: 'Emily',
    last_name: 'Rodriguez',
    role: 'hr',
    department: 'Human Resources',
    position: 'HR Specialist',
    company: 'TechCorp',
    avatar_url: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150&h=150&fit=crop&crop=face',
    is_active: true,
    is_verified: true,
    hire_date: '2023-01-10',
    timezone: 'America/Chicago',
    language: 'en',
    preferences: {
      notifications: {
        email: true,
        push: true,
        sms: true
      },
      privacy: {
        anonymous_checkins: false,
        share_analytics: true
      }
    },
    wellness_profile: {
      goals: ['Employee wellness', 'Program development', 'Data analysis'],
      interests: ['Wellness programs', 'Employee engagement', 'Analytics'],
      challenges: ['Program adoption', 'Data privacy', 'Resource allocation']
    }
  }
];

// Mock Wellness Entries
export const mockWellnessEntries: MockWellnessEntry[] = [
  {
    id: '1',
    user_id: '1',
    entry_type: 'comprehensive',
    value: 7.5,
    description: 'Feeling good today! Had a productive morning and feeling energized.',
    mood_score: 8.0,
    stress_score: 4.0,
    energy_score: 7.5,
    sleep_hours: 7.5,
    sleep_quality: 8.0,
    work_life_balance: 7.0,
    social_support: 8.0,
    physical_activity: 6.0,
    nutrition_quality: 7.0,
    productivity_level: 8.0,
    tags: ['positive', 'productive', 'energized'],
    factors: {
      workload: 'moderate',
      sleep: 'good',
      exercise: 'completed',
      social: 'connected'
    },
    recommendations: [
      'Continue your current routine',
      'Consider adding more physical activity',
      'Maintain good sleep habits'
    ],
    risk_indicators: [],
    is_anonymous: false,
    created_at: '2024-01-15T08:30:00Z'
  },
  {
    id: '2',
    user_id: '1',
    entry_type: 'comprehensive',
    value: 6.0,
    description: 'A bit stressed with the upcoming deadline, but managing well.',
    mood_score: 6.5,
    stress_score: 7.0,
    energy_score: 6.0,
    sleep_hours: 6.5,
    sleep_quality: 6.0,
    work_life_balance: 5.5,
    social_support: 7.0,
    physical_activity: 4.0,
    nutrition_quality: 6.0,
    productivity_level: 7.0,
    tags: ['stressed', 'deadline', 'managing'],
    factors: {
      workload: 'high',
      sleep: 'adequate',
      exercise: 'minimal',
      social: 'limited'
    },
    recommendations: [
      'Take short breaks throughout the day',
      'Practice stress management techniques',
      'Try to get more sleep tonight'
    ],
    risk_indicators: ['high_stress', 'poor_sleep'],
    is_anonymous: false,
    created_at: '2024-01-14T09:15:00Z'
  },
  {
    id: '3',
    user_id: '2',
    entry_type: 'comprehensive',
    value: 8.0,
    description: 'Great team meeting today. Feeling confident about our project direction.',
    mood_score: 8.5,
    stress_score: 3.0,
    energy_score: 8.0,
    sleep_hours: 8.0,
    sleep_quality: 8.5,
    work_life_balance: 8.0,
    social_support: 9.0,
    physical_activity: 7.0,
    nutrition_quality: 8.0,
    productivity_level: 8.5,
    tags: ['confident', 'team', 'productive'],
    factors: {
      workload: 'balanced',
      sleep: 'excellent',
      exercise: 'completed',
      social: 'very_connected'
    },
    recommendations: [
      'Excellent work! Keep up the momentum',
      'Share your positive energy with the team',
      'Consider mentoring others'
    ],
    risk_indicators: [],
    is_anonymous: false,
    created_at: '2024-01-15T10:00:00Z'
  }
];

// Mock Resources
export const mockResources: MockResource[] = [
  {
    id: '1',
    title: 'Mindful Breathing Techniques for Stress Relief',
    description: 'Learn simple breathing exercises that can help reduce stress and anxiety in just 5 minutes. Perfect for busy professionals who need quick stress relief during the workday.',
    category: 'stress_management',
    difficulty_level: 'beginner',
    duration_minutes: 5,
    tags: ['breathing', 'stress', 'meditation', 'quick'],
    author: 'Dr. Sarah Williams, Wellness Expert',
    content_url: 'https://example.com/breathing-techniques',
    thumbnail_url: 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=300&h=200&fit=crop',
    is_active: true,
    view_count: 1247,
    rating: 4.8,
    rating_count: 89,
    created_at: '2024-01-01T00:00:00Z'
  },
  {
    id: '2',
    title: 'Building Resilience: A Complete Guide',
    description: 'Comprehensive guide to building mental and emotional resilience in the workplace. Includes practical exercises, case studies, and actionable strategies for long-term wellness.',
    category: 'resilience',
    difficulty_level: 'intermediate',
    duration_minutes: 45,
    tags: ['resilience', 'mental-health', 'workplace', 'long-term'],
    author: 'Dr. Michael Chen, Clinical Psychologist',
    content_url: 'https://example.com/resilience-guide',
    thumbnail_url: 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=300&h=200&fit=crop',
    is_active: true,
    view_count: 892,
    rating: 4.6,
    rating_count: 67,
    created_at: '2024-01-05T00:00:00Z'
  },
  {
    id: '3',
    title: 'Quick Desk Exercises for Office Workers',
    description: 'Simple exercises you can do at your desk to improve posture, reduce tension, and boost energy levels. No equipment needed!',
    category: 'physical_wellness',
    difficulty_level: 'beginner',
    duration_minutes: 10,
    tags: ['exercise', 'desk', 'posture', 'energy'],
    author: 'Lisa Thompson, Physical Therapist',
    content_url: 'https://example.com/desk-exercises',
    thumbnail_url: 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=300&h=200&fit=crop',
    is_active: true,
    view_count: 2156,
    rating: 4.9,
    rating_count: 156,
    created_at: '2024-01-10T00:00:00Z'
  },
  {
    id: '4',
    title: 'Nutrition for Mental Performance',
    description: 'Discover how your diet affects your mental performance, mood, and energy levels. Learn about brain-boosting foods and meal planning strategies.',
    category: 'nutrition',
    difficulty_level: 'intermediate',
    duration_minutes: 30,
    tags: ['nutrition', 'brain', 'performance', 'diet'],
    author: 'Dr. Emily Rodriguez, Nutritionist',
    content_url: 'https://example.com/nutrition-mental-performance',
    thumbnail_url: 'https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=300&h=200&fit=crop',
    is_active: true,
    view_count: 1678,
    rating: 4.7,
    rating_count: 112,
    created_at: '2024-01-12T00:00:00Z'
  },
  {
    id: '5',
    title: 'Sleep Optimization for Professionals',
    description: 'Evidence-based strategies to improve sleep quality and quantity for busy professionals. Includes sleep hygiene practices and technology recommendations.',
    category: 'sleep',
    difficulty_level: 'beginner',
    duration_minutes: 20,
    tags: ['sleep', 'hygiene', 'rest', 'recovery'],
    author: 'Dr. James Wilson, Sleep Specialist',
    content_url: 'https://example.com/sleep-optimization',
    thumbnail_url: 'https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?w=300&h=200&fit=crop',
    is_active: true,
    view_count: 1345,
    rating: 4.5,
    rating_count: 78,
    created_at: '2024-01-08T00:00:00Z'
  }
];

// Mock Analytics
export const mockAnalytics: MockAnalytics = {
  organizational_health: {
    overall_score: 7.8,
    trend: 'improving',
    departments: [
      {
        name: 'Engineering',
        score: 8.2,
        trend: 'improving',
        employee_count: 45
      },
      {
        name: 'Marketing',
        score: 7.5,
        trend: 'stable',
        employee_count: 23
      },
      {
        name: 'Sales',
        score: 7.1,
        trend: 'improving',
        employee_count: 18
      },
      {
        name: 'Human Resources',
        score: 8.5,
        trend: 'improving',
        employee_count: 12
      },
      {
        name: 'Finance',
        score: 6.8,
        trend: 'declining',
        employee_count: 15
      }
    ],
    kpis: [
      {
        name: 'Employee Satisfaction',
        value: 8.1,
        target: 8.0,
        status: 'good'
      },
      {
        name: 'Stress Level',
        value: 6.2,
        target: 5.0,
        status: 'warning'
      },
      {
        name: 'Work-Life Balance',
        value: 7.4,
        target: 7.5,
        status: 'good'
      },
      {
        name: 'Team Collaboration',
        value: 8.3,
        target: 8.0,
        status: 'good'
      },
      {
        name: 'Productivity',
        value: 7.9,
        target: 8.0,
        status: 'good'
      }
    ]
  },
  team_analytics: {
    team_id: '1',
    team_name: 'Engineering Team',
    wellness_score: 8.2,
    engagement_score: 8.5,
    productivity_score: 8.1,
    collaboration_score: 8.3,
    members: [
      {
        user_id: '1',
        name: 'Sarah Johnson',
        role: 'Senior Software Engineer',
        wellness_score: 8.0,
        participation_rate: 95
      },
      {
        user_id: '4',
        name: 'David Kim',
        role: 'Software Engineer',
        wellness_score: 7.8,
        participation_rate: 88
      },
      {
        user_id: '5',
        name: 'Maria Garcia',
        role: 'Frontend Developer',
        wellness_score: 8.5,
        participation_rate: 92
      },
      {
        user_id: '6',
        name: 'Alex Thompson',
        role: 'Backend Developer',
        wellness_score: 7.9,
        participation_rate: 85
      }
    ],
    trends: [
      { date: '2024-01-01', wellness_score: 7.8, engagement_score: 8.2 },
      { date: '2024-01-08', wellness_score: 8.0, engagement_score: 8.4 },
      { date: '2024-01-15', wellness_score: 8.2, engagement_score: 8.5 }
    ]
  },
  risk_assessment: {
    overall_risk_level: 'low',
    risk_factors: [
      {
        factor: 'High workload periods',
        severity: 'medium',
        impact: 6.5,
        recommendations: [
          'Implement flexible work schedules',
          'Provide additional support during peak periods',
          'Encourage regular breaks'
        ]
      },
      {
        factor: 'Screen time exposure',
        severity: 'low',
        impact: 4.2,
        recommendations: [
          'Promote 20-20-20 rule (20 min break every 20 min)',
          'Encourage outdoor activities',
          'Provide blue light filters'
        ]
      },
      {
        factor: 'Sedentary work style',
        severity: 'low',
        impact: 3.8,
        recommendations: [
          'Implement standing desk options',
          'Schedule walking meetings',
          'Encourage regular movement breaks'
        ]
      }
    ],
    trends: [
      { date: '2024-01-01', risk_level: 'low', risk_score: 3.2 },
      { date: '2024-01-08', risk_level: 'low', risk_score: 3.5 },
      { date: '2024-01-15', risk_level: 'low', risk_score: 3.1 }
    ]
  }
};

// Mock Notifications
export const mockNotifications: MockNotification[] = [
  {
    id: '1',
    user_id: '1',
    title: 'Wellness Check-in Reminder',
    message: 'Don\'t forget to complete your weekly wellness check-in. Your insights help us create a better workplace for everyone.',
    notification_type: 'info',
    priority: 'medium',
    is_read: false,
    created_at: '2024-01-15T09:00:00Z',
    metadata: { reminder_type: 'weekly_checkin' }
  },
  {
    id: '2',
    user_id: '1',
    title: 'New Resource Available',
    message: 'Check out our new guide on "Mindful Breathing Techniques for Stress Relief" - perfect for busy professionals!',
    notification_type: 'success',
    priority: 'low',
    is_read: true,
    created_at: '2024-01-14T14:30:00Z',
    metadata: { resource_id: '1', resource_title: 'Mindful Breathing Techniques' }
  },
  {
    id: '3',
    user_id: '1',
    title: 'Wellness Goal Achievement',
    message: 'Congratulations! You\'ve achieved your goal of reducing stress levels. Keep up the great work!',
    notification_type: 'success',
    priority: 'high',
    is_read: false,
    created_at: '2024-01-13T16:45:00Z',
    metadata: { goal_type: 'stress_reduction', achievement_date: '2024-01-13' }
  }
];

// Mock Conversations
export const mockConversations: MockConversation[] = [
  {
    id: '1',
    user_id: '1',
    messages: [
      {
        id: '1',
        role: 'user',
        content: 'I\'ve been feeling really stressed lately with all the deadlines at work. Any suggestions?',
        timestamp: '2024-01-15T10:30:00Z'
      },
      {
        id: '2',
        role: 'assistant',
        content: 'I understand how challenging deadlines can be! Let\'s work through this together. First, can you tell me more about what specifically is causing the most stress? Is it the volume of work, the time pressure, or something else?',
        timestamp: '2024-01-15T10:30:30Z'
      },
      {
        id: '3',
        role: 'user',
        content: 'It\'s mostly the time pressure. I feel like I don\'t have enough time to do quality work.',
        timestamp: '2024-01-15T10:31:00Z'
      },
      {
        id: '4',
        role: 'assistant',
        content: 'That\'s a very common concern. Here are some strategies that might help:\n\n1. **Time Blocking**: Try scheduling specific time slots for different tasks\n2. **Prioritization**: Focus on the most important tasks first\n3. **Break Tasks Down**: Large projects can feel overwhelming - break them into smaller, manageable pieces\n4. **Communicate**: Let your manager know if deadlines feel unrealistic\n\nWould you like me to help you create a specific plan for any of these approaches?',
        timestamp: '2024-01-15T10:31:30Z'
      }
    ],
    summary: 'Discussion about work stress and time management strategies',
    created_at: '2024-01-15T10:30:00Z',
    updated_at: '2024-01-15T10:31:30Z'
  }
];

// Search suggestions for pre-loaded search
export const searchSuggestions = [
  'stress management techniques',
  'work-life balance tips',
  'mindfulness exercises',
  'sleep improvement',
  'team collaboration',
  'productivity hacks',
  'mental health resources',
  'physical wellness',
  'nutrition advice',
  'resilience building'
];

// Pre-loaded search phrase and results
export const preloadedSearch = {
  query: 'stress management techniques',
  results: [
    {
      id: '1',
      title: 'Mindful Breathing Techniques for Stress Relief',
      description: 'Learn simple breathing exercises that can help reduce stress and anxiety in just 5 minutes.',
      category: 'stress_management',
      rating: 4.8,
      duration: '5 min'
    },
    {
      id: '2',
      title: 'Building Resilience: A Complete Guide',
      description: 'Comprehensive guide to building mental and emotional resilience in the workplace.',
      category: 'resilience',
      rating: 4.6,
      duration: '45 min'
    },
    {
      id: '3',
      title: 'Quick Desk Exercises for Office Workers',
      description: 'Simple exercises you can do at your desk to improve posture and reduce tension.',
      category: 'physical_wellness',
      rating: 4.9,
      duration: '10 min'
    }
  ]
};

// Export all mock data
export const mockData = {
  users: mockUsers,
  wellnessEntries: mockWellnessEntries,
  resources: mockResources,
  analytics: mockAnalytics,
  notifications: mockNotifications,
  conversations: mockConversations,
  searchSuggestions,
  preloadedSearch
};

export default mockData;
