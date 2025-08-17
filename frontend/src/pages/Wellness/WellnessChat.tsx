import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  TextField,
  Button,
  Avatar,
  Paper,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Chip,
  Divider,
  IconButton,
  CircularProgress,
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Grid,
} from '@mui/material';
import {
  Send,
  Psychology,
  Person,
  SmartToy,
  Refresh,
  Settings,
  Lightbulb,
  Favorite,
  Warning,
  CheckCircle,
  Info,
  Chat,
  EmojiEmotions,
  LocalHospital,
  FitnessCenter,
  School,
} from '@mui/icons-material';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';

import { RootState } from '../../store';
import { sendConversation, fetchConversations } from '../../store/slices/wellnessSlice';
import { addNotification } from '../../store/slices/uiSlice';
import LoadingSpinner from '../../components/Common/LoadingSpinner';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'ai';
  timestamp: Date;
  sentiment?: 'positive' | 'negative' | 'neutral';
  riskLevel?: 'low' | 'medium' | 'high';
  suggestions?: string[];
  agentType?: string;
}

interface ChatSession {
  id: string;
  title: string;
  messages: Message[];
  createdAt: Date;
  lastActivity: Date;
}

const WellnessChat: React.FC = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { user } = useSelector((state: RootState) => state.auth);
  const { conversations, isLoading } = useSelector((state: RootState) => state.wellness);
  
  const [currentMessage, setCurrentMessage] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isTyping, setIsTyping] = useState(false);
  const [selectedAgent, setSelectedAgent] = useState('wellness');
  const [showAgentSelector, setShowAgentSelector] = useState(false);
  const [sessionId] = useState(`session_${Date.now()}`);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const agents = [
    {
      id: 'wellness',
      name: 'Wellness Companion',
      description: 'General wellness support and guidance',
      icon: <EmojiEmotions />,
      color: 'primary',
    },
    {
      id: 'cbt',
      name: 'CBT Specialist',
      description: 'Cognitive Behavioral Therapy techniques',
      icon: <Psychology />,
      color: 'secondary',
    },
    {
      id: 'stress',
      name: 'Stress Management',
      description: 'Stress reduction and coping strategies',
      icon: <FitnessCenter />,
      color: 'success',
    },
    {
      id: 'crisis',
      name: 'Crisis Support',
      description: 'Immediate support for difficult situations',
      icon: <LocalHospital />,
      color: 'error',
    },
    {
      id: 'learning',
      name: 'Wellness Education',
      description: 'Learn about mental health and wellness',
      icon: <School />,
      color: 'info',
    },
  ];

  const quickPrompts = [
    "I'm feeling stressed about work",
    "I'm having trouble sleeping",
    "I need help with work-life balance",
    "I'm feeling overwhelmed",
    "I want to improve my mood",
    "I need coping strategies",
    "I'm feeling anxious",
    "I want to build resilience",
  ];

  useEffect(() => {
    // Load previous conversations
    dispatch(fetchConversations());
    
    // Add welcome message
    const welcomeMessage: Message = {
      id: 'welcome',
      text: `Hello ${user?.firstName || 'there'}! I'm your AI wellness companion. I'm here to support your mental health and well-being. How can I help you today?`,
      sender: 'ai',
      timestamp: new Date(),
      sentiment: 'positive',
      agentType: 'wellness',
    };
    
    setMessages([welcomeMessage]);
  }, [dispatch, user]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async () => {
    if (!currentMessage.trim() || isTyping) return;

    const userMessage: Message = {
      id: `user_${Date.now()}`,
      text: currentMessage,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setCurrentMessage('');
    setIsTyping(true);

    try {
      // Send message to backend
      const response = await dispatch(sendConversation(currentMessage));
      
      // Simulate AI response (in real app, this would come from the backend)
      setTimeout(() => {
        const aiResponse = generateAIResponse(currentMessage, selectedAgent);
        setMessages(prev => [...prev, aiResponse]);
        setIsTyping(false);
      }, 1000);

    } catch (error) {
      setIsTyping(false);
      dispatch(addNotification({
        type: 'error',
        title: 'Message Failed',
        message: 'Failed to send message. Please try again.',
      }));
    }
  };

  const generateAIResponse = (userMessage: string, agentType: string): Message => {
    const lowerMessage = userMessage.toLowerCase();
    
    // Simple response logic (in real app, this would be handled by the AI agents)
    let response = '';
    let sentiment: 'positive' | 'negative' | 'neutral' = 'neutral';
    let riskLevel: 'low' | 'medium' | 'high' = 'low';
    let suggestions: string[] = [];

    if (lowerMessage.includes('stress') || lowerMessage.includes('overwhelm')) {
      response = "I understand you're feeling stressed. Stress is a natural response, but it's important to manage it effectively. Let's work on some strategies together.";
      sentiment = 'negative';
      riskLevel = 'medium';
      suggestions = [
        'Try deep breathing exercises',
        'Take a 5-minute break',
        'Practice progressive muscle relaxation',
        'Consider talking to a manager about workload'
      ];
    } else if (lowerMessage.includes('sleep') || lowerMessage.includes('tired')) {
      response = "Sleep is crucial for your well-being. Poor sleep can affect your mood, energy, and overall health. Let me help you improve your sleep hygiene.";
      sentiment = 'neutral';
      suggestions = [
        'Establish a consistent bedtime routine',
        'Limit screen time before bed',
        'Create a comfortable sleep environment',
        'Avoid caffeine in the afternoon'
      ];
    } else if (lowerMessage.includes('anxious') || lowerMessage.includes('worry')) {
      response = "Anxiety can be challenging to manage. It's important to acknowledge your feelings and develop healthy coping mechanisms. You're not alone in this.";
      sentiment = 'negative';
      riskLevel = 'medium';
      suggestions = [
        'Practice mindfulness meditation',
        'Use grounding techniques',
        'Consider speaking with a mental health professional',
        'Try journaling your thoughts'
      ];
    } else if (lowerMessage.includes('happy') || lowerMessage.includes('good') || lowerMessage.includes('great')) {
      response = "That's wonderful to hear! Positive emotions are important for your overall well-being. What's contributing to your good mood?";
      sentiment = 'positive';
      suggestions = [
        'Share your positive experience with others',
        'Practice gratitude',
        'Build on this positive momentum',
        'Remember this feeling for challenging times'
      ];
    } else {
      response = "Thank you for sharing that with me. I'm here to listen and support you. Could you tell me more about how you're feeling or what's on your mind?";
      sentiment = 'neutral';
      suggestions = [
        'Try the wellness check-in feature',
        'Explore our wellness resources',
        'Consider speaking with a professional',
        'Practice self-care activities'
      ];
    }

    return {
      id: `ai_${Date.now()}`,
      text: response,
      sender: 'ai',
      timestamp: new Date(),
      sentiment,
      riskLevel,
      suggestions,
      agentType,
    };
  };

  const handleQuickPrompt = (prompt: string) => {
    setCurrentMessage(prompt);
  };

  const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSendMessage();
    }
  };

  const getSentimentColor = (sentiment?: string) => {
    switch (sentiment) {
      case 'positive': return 'success.main';
      case 'negative': return 'error.main';
      default: return 'text.primary';
    }
  };

  const getRiskColor = (riskLevel?: string) => {
    switch (riskLevel) {
      case 'high': return 'error.main';
      case 'medium': return 'warning.main';
      default: return 'success.main';
    }
  };

  return (
    <Box sx={{ p: 3, maxWidth: 1200, mx: 'auto', height: 'calc(100vh - 200px)' }}>
      <Typography variant="h4" sx={{ mb: 3, fontWeight: 600, color: 'primary.main' }}>
        Wellness Chat
      </Typography>

      <Grid container spacing={3} sx={{ height: '100%' }}>
        {/* Chat Interface */}
        <Grid item xs={12} lg={8}>
          <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
            <CardContent sx={{ flex: 1, display: 'flex', flexDirection: 'column', p: 0 }}>
              {/* Chat Header */}
              <Box sx={{ 
                p: 2, 
                borderBottom: 1, 
                borderColor: 'divider',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between'
              }}>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <Avatar sx={{ bgcolor: 'primary.main', mr: 2 }}>
                    <SmartToy />
                  </Avatar>
                  <Box>
                    <Typography variant="h6" sx={{ fontWeight: 600 }}>
                      AI Wellness Companion
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Available 24/7 for support
                    </Typography>
                  </Box>
                </Box>
                
                <Box>
                  <IconButton 
                    onClick={() => setShowAgentSelector(true)}
                    size="small"
                  >
                    <Settings />
                  </IconButton>
                </Box>
              </Box>

              {/* Messages Area */}
              <Box sx={{ 
                flex: 1, 
                overflow: 'auto', 
                p: 2,
                display: 'flex',
                flexDirection: 'column',
                gap: 2
              }}>
                {messages.map((message) => (
                  <Box
                    key={message.id}
                    sx={{
                      display: 'flex',
                      justifyContent: message.sender === 'user' ? 'flex-end' : 'flex-start',
                      mb: 2,
                    }}
                  >
                    <Paper
                      sx={{
                        p: 2,
                        maxWidth: '70%',
                        backgroundColor: message.sender === 'user' ? 'primary.main' : 'grey.100',
                        color: message.sender === 'user' ? 'white' : 'text.primary',
                        borderRadius: 2,
                        position: 'relative',
                      }}
                    >
                      <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                        <Avatar
                          sx={{
                            width: 24,
                            height: 24,
                            mr: 1,
                            bgcolor: message.sender === 'user' ? 'white' : 'primary.main',
                            color: message.sender === 'user' ? 'primary.main' : 'white',
                          }}
                        >
                          {message.sender === 'user' ? <Person /> : <SmartToy />}
                        </Avatar>
                        <Typography variant="caption" color="text.secondary">
                          {message.timestamp.toLocaleTimeString()}
                        </Typography>
                      </Box>

                      <Typography variant="body1" sx={{ mb: 1 }}>
                        {message.text}
                      </Typography>

                      {/* Sentiment and Risk Indicators */}
                      {(message.sentiment || message.riskLevel) && (
                        <Box sx={{ display: 'flex', gap: 1, mt: 1 }}>
                          {message.sentiment && (
                            <Chip
                              label={message.sentiment}
                              size="small"
                              color={message.sentiment === 'positive' ? 'success' : 
                                     message.sentiment === 'negative' ? 'error' : 'default'}
                            />
                          )}
                          {message.riskLevel && message.riskLevel !== 'low' && (
                            <Chip
                              label={`Risk: ${message.riskLevel}`}
                              size="small"
                              color={message.riskLevel === 'high' ? 'error' : 'warning'}
                            />
                          )}
                        </Box>
                      )}

                      {/* Suggestions */}
                      {message.suggestions && message.suggestions.length > 0 && (
                        <Box sx={{ mt: 2 }}>
                          <Typography variant="caption" sx={{ fontWeight: 600, display: 'block', mb: 1 }}>
                            Suggestions:
                          </Typography>
                          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                            {message.suggestions.map((suggestion, index) => (
                              <Chip
                                key={index}
                                label={suggestion}
                                size="small"
                                variant="outlined"
                                onClick={() => handleQuickPrompt(suggestion)}
                                sx={{ cursor: 'pointer' }}
                              />
                            ))}
                          </Box>
                        </Box>
                      )}
                    </Paper>
                  </Box>
                ))}

                {/* Typing Indicator */}
                {isTyping && (
                  <Box sx={{ display: 'flex', justifyContent: 'flex-start', mb: 2 }}>
                    <Paper sx={{ p: 2, backgroundColor: 'grey.100' }}>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <CircularProgress size={16} sx={{ mr: 1 }} />
                        <Typography variant="body2" color="text.secondary">
                          AI is typing...
                        </Typography>
                      </Box>
                    </Paper>
                  </Box>
                )}

                <div ref={messagesEndRef} />
              </Box>

              {/* Quick Prompts */}
              <Box sx={{ p: 2, borderTop: 1, borderColor: 'divider' }}>
                <Typography variant="body2" sx={{ mb: 1, fontWeight: 500 }}>
                  Quick prompts:
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {quickPrompts.slice(0, 4).map((prompt) => (
                    <Chip
                      key={prompt}
                      label={prompt}
                      size="small"
                      variant="outlined"
                      onClick={() => handleQuickPrompt(prompt)}
                      sx={{ cursor: 'pointer' }}
                    />
                  ))}
                </Box>
              </Box>

              {/* Message Input */}
              <Box sx={{ p: 2, borderTop: 1, borderColor: 'divider' }}>
                <Box sx={{ display: 'flex', gap: 1 }}>
                  <TextField
                    fullWidth
                    multiline
                    maxRows={4}
                    placeholder="Type your message here..."
                    value={currentMessage}
                    onChange={(e) => setCurrentMessage(e.target.value)}
                    onKeyPress={handleKeyPress}
                    disabled={isTyping}
                  />
                  <Button
                    variant="contained"
                    onClick={handleSendMessage}
                    disabled={!currentMessage.trim() || isTyping}
                    sx={{ minWidth: 'auto', px: 2 }}
                  >
                    <Send />
                  </Button>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Sidebar */}
        <Grid item xs={12} lg={4}>
          {/* Current Agent Info */}
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                Current Agent
              </Typography>
              
              {(() => {
                const agent = agents.find(a => a.id === selectedAgent);
                return (
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <Avatar sx={{ bgcolor: `${agent?.color}.main`, mr: 2 }}>
                      {agent?.icon}
                    </Avatar>
                    <Box>
                      <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                        {agent?.name}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {agent?.description}
                      </Typography>
                    </Box>
                  </Box>
                );
              })()}

              <Button
                variant="outlined"
                size="small"
                onClick={() => setShowAgentSelector(true)}
                startIcon={<Settings />}
              >
                Change Agent
              </Button>
            </CardContent>
          </Card>

          {/* Wellness Tips */}
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                Wellness Tips
              </Typography>
              
              <List dense>
                <ListItem>
                  <ListItemAvatar>
                    <Avatar sx={{ bgcolor: 'success.main' }}>
                      <Lightbulb />
                    </Avatar>
                  </ListItemAvatar>
                  <ListItemText
                    primary="Practice mindfulness"
                    secondary="Take 5 minutes to focus on your breath"
                  />
                </ListItem>
                
                <ListItem>
                  <ListItemAvatar>
                    <Avatar sx={{ bgcolor: 'primary.main' }}>
                      <Favorite />
                    </Avatar>
                  </ListItemAvatar>
                  <ListItemText
                    primary="Express gratitude"
                    secondary="Write down 3 things you're thankful for"
                  />
                </ListItem>
                
                <ListItem>
                  <ListItemAvatar>
                    <Avatar sx={{ bgcolor: 'warning.main' }}>
                      <FitnessCenter />
                    </Avatar>
                  </ListItemAvatar>
                  <ListItemText
                    primary="Move your body"
                    secondary="Even a short walk can boost your mood"
                  />
                </ListItem>
              </List>
            </CardContent>
          </Card>

          {/* Crisis Resources */}
          <Card>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                Need Immediate Help?
              </Typography>
              
              <Alert severity="info" sx={{ mb: 2 }}>
                If you're in crisis or need immediate support, please reach out to:
              </Alert>
              
              <List dense>
                <ListItem>
                  <ListItemText
                    primary="National Suicide Prevention Lifeline"
                    secondary="988 or 1-800-273-8255"
                  />
                </ListItem>
                
                <ListItem>
                  <ListItemText
                    primary="Crisis Text Line"
                    secondary="Text HOME to 741741"
                  />
                </ListItem>
                
                <ListItem>
                  <ListItemText
                    primary="Your EAP Provider"
                    secondary="Contact HR for details"
                  />
                </ListItem>
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Agent Selector Dialog */}
      <Dialog 
        open={showAgentSelector} 
        onClose={() => setShowAgentSelector(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Choose Your AI Agent</DialogTitle>
        <DialogContent>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            Different agents specialize in different areas of wellness support. Choose the one that best fits your current needs.
          </Typography>
          
          <Grid container spacing={2}>
            {agents.map((agent) => (
              <Grid item xs={12} key={agent.id}>
                <Card
                  sx={{
                    cursor: 'pointer',
                    border: selectedAgent === agent.id ? 2 : 1,
                    borderColor: selectedAgent === agent.id ? 'primary.main' : 'divider',
                    '&:hover': {
                      borderColor: 'primary.main',
                      backgroundColor: 'action.hover',
                    },
                  }}
                  onClick={() => {
                    setSelectedAgent(agent.id);
                    setShowAgentSelector(false);
                  }}
                >
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <Avatar sx={{ bgcolor: `${agent.color}.main`, mr: 2 }}>
                        {agent.icon}
                      </Avatar>
                      <Box sx={{ flex: 1 }}>
                        <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                          {agent.name}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          {agent.description}
                        </Typography>
                      </Box>
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowAgentSelector(false)}>
            Cancel
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default WellnessChat;
