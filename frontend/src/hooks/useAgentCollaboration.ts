import { useState, useEffect, useCallback, useRef } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '../store';
import { addNotification } from '../store/slices/uiSlice';

export interface AgentCollaborationState {
  isActive: boolean;
  participatingAgents: string[];
  collaborationPattern: 'emergent' | 'consensus' | 'hierarchical' | 'peer_to_peer' | 'competitive';
  currentStep: number;
  totalSteps: number;
  agentResponses: Record<string, any>;
  emergentInsights: string[];
  trustUpdates: Record<string, number>;
  collaborationTime: number;
  performanceMetrics: Record<string, {
    responseTime: number;
    success: boolean;
    confidence: number;
  }>;
}

export interface CollaborationRequest {
  message: string;
  context: {
    userRole: string;
    sessionId: string;
    timestamp: string;
  };
  collaborationPattern?: AgentCollaborationState['collaborationPattern'];
  priority?: number;
  timeout?: number;
}

export interface AgentCapability {
  id: string;
  name: string;
  description: string;
  category: 'analysis' | 'recommendation' | 'detection' | 'enforcement' | 'generation';
  confidence: number;
}

export const useAgentCollaboration = () => {
  const dispatch = useDispatch();
  const { user } = useSelector((state: RootState) => state.auth);
  
  const [collaborationState, setCollaborationState] = useState<AgentCollaborationState>({
    isActive: false,
    participatingAgents: [],
    collaborationPattern: 'emergent',
    currentStep: 0,
    totalSteps: 0,
    agentResponses: {},
    emergentInsights: [],
    trustUpdates: {},
    collaborationTime: 0,
    performanceMetrics: {},
  });

  const [agentCapabilities, setAgentCapabilities] = useState<Record<string, AgentCapability[]>>({
    'wellness_companion': [
      {
        id: 'conversation_management',
        name: 'Conversation Management',
        description: 'Manages empathetic conversations and provides emotional support',
        category: 'analysis',
        confidence: 0.95,
      },
      {
        id: 'crisis_intervention',
        name: 'Crisis Intervention',
        description: 'Identifies and responds to crisis situations',
        category: 'detection',
        confidence: 0.98,
      },
    ],
    'sentiment_risk_detection': [
      {
        id: 'sentiment_analysis',
        name: 'Sentiment Analysis',
        description: 'Analyzes emotional content and sentiment patterns',
        category: 'analysis',
        confidence: 0.92,
      },
      {
        id: 'risk_detection',
        name: 'Risk Detection',
        description: 'Identifies burnout and mental health risks',
        category: 'detection',
        confidence: 0.89,
      },
    ],
    'resource_recommendation': [
      {
        id: 'resource_matching',
        name: 'Resource Matching',
        description: 'Matches users with appropriate wellness resources',
        category: 'recommendation',
        confidence: 0.91,
      },
      {
        id: 'predictive_modeling',
        name: 'Predictive Modeling',
        description: 'Predicts user needs and preferences',
        category: 'generation',
        confidence: 0.87,
      },
    ],
    'analytics_reporting': [
      {
        id: 'analytics_generation',
        name: 'Analytics Generation',
        description: 'Generates comprehensive wellness analytics',
        category: 'generation',
        confidence: 0.94,
      },
      {
        id: 'trend_analysis',
        name: 'Trend Analysis',
        description: 'Analyzes wellness trends and patterns',
        category: 'analysis',
        confidence: 0.90,
      },
    ],
    'policy_privacy': [
      {
        id: 'privacy_enforcement',
        name: 'Privacy Enforcement',
        description: 'Ensures data privacy and compliance',
        category: 'enforcement',
        confidence: 0.99,
      },
    ],
  });

  const collaborationTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const startTimeRef = useRef<number>(0);

  const initiateCollaboration = useCallback(async (request: CollaborationRequest) => {
    if (collaborationState.isActive) {
      dispatch(addNotification({
        type: 'warning',
        title: 'Collaboration Already Active',
        message: 'Please wait for the current collaboration to complete.',
      }));
      return;
    }

    const pattern = request.collaborationPattern || 'emergent';
    const timeout = request.timeout || 30000; // 30 seconds default

    // Determine participating agents based on collaboration pattern
    const agents = getAgentsForPattern(pattern);
    
    setCollaborationState(prev => ({
      ...prev,
      isActive: true,
      participatingAgents: agents,
      collaborationPattern: pattern,
      currentStep: 0,
      totalSteps: getTotalStepsForPattern(pattern),
      agentResponses: {},
      emergentInsights: [],
      trustUpdates: {},
      collaborationTime: 0,
      performanceMetrics: {},
    }));

    startTimeRef.current = Date.now();

    // Start collaboration process
    await executeCollaboration(request, pattern, agents, timeout);
  }, [collaborationState.isActive, dispatch]);

  const executeCollaboration = useCallback(async (
    request: CollaborationRequest,
    pattern: AgentCollaborationState['collaborationPattern'],
    agents: string[],
    timeout: number
  ) => {
    try {
      switch (pattern) {
        case 'emergent':
          await executeEmergentCollaboration(request, agents, timeout);
          break;
        case 'consensus':
          await executeConsensusCollaboration(request, agents, timeout);
          break;
        case 'hierarchical':
          await executeHierarchicalCollaboration(request, agents, timeout);
          break;
        case 'peer_to_peer':
          await executePeerCollaboration(request, agents, timeout);
          break;
        case 'competitive':
          await executeCompetitiveCollaboration(request, agents, timeout);
          break;
        default:
          throw new Error(`Unknown collaboration pattern: ${pattern}`);
      }
    } catch (error) {
      console.error('Collaboration execution failed:', error);
      dispatch(addNotification({
        type: 'error',
        title: 'Collaboration Failed',
        message: 'The agent collaboration encountered an error.',
      }));
    } finally {
      completeCollaboration();
    }
  }, [dispatch]);

  const executeEmergentCollaboration = useCallback(async (
    request: CollaborationRequest,
    agents: string[],
    timeout: number
  ) => {
    // Step 1: Initial agent responses
    setCollaborationState(prev => ({ ...prev, currentStep: 1 }));
    
    const initialResponses = await Promise.all(
      agents.map(async (agent) => {
        const response = await simulateAgentResponse(agent, request, 'initial');
        return { agent, response };
      })
    );

    // Update state with initial responses
    setCollaborationState(prev => ({
      ...prev,
      agentResponses: Object.fromEntries(
        initialResponses.map(({ agent, response }) => [agent, { initial: response }])
      ),
      currentStep: 2,
    }));

    // Step 2: Emergent behavior - agents build upon each other's responses
    const emergentInsights: string[] = [];
    const enhancedResponses: Record<string, any> = {};

    for (const { agent, response } of initialResponses) {
      if (response.success && response.data) {
        // Other agents build upon this response
        for (const otherAgent of agents) {
          if (otherAgent !== agent) {
            const enhancedResponse = await simulateAgentResponse(
              otherAgent,
              {
                ...request,
                message: `${request.message} [Building upon ${agent}'s insights: ${JSON.stringify(response.data)}]`,
              },
              'enhanced'
            );

            if (enhancedResponse.success) {
              enhancedResponses[otherAgent] = enhancedResponse;
              emergentInsights.push(`${otherAgent} built upon ${agent}'s insights`);
            }
          }
        }
      }
    }

    // Update state with emergent insights
    setCollaborationState(prev => ({
      ...prev,
      agentResponses: {
        ...prev.agentResponses,
        ...Object.fromEntries(
          Object.entries(enhancedResponses).map(([agent, response]) => [
            agent,
            { ...prev.agentResponses[agent], enhanced: response }
          ])
        ),
      },
      emergentInsights,
      currentStep: 3,
    }));

  }, []);

  const executeConsensusCollaboration = useCallback(async (
    request: CollaborationRequest,
    agents: string[],
    timeout: number
  ) => {
    // Step 1: Initial consensus round
    setCollaborationState(prev => ({ ...prev, currentStep: 1 }));
    
    const initialResponses = await Promise.all(
      agents.map(async (agent) => {
        const response = await simulateAgentResponse(agent, request, 'initial');
        return { agent, response };
      })
    );

    setCollaborationState(prev => ({
      ...prev,
      agentResponses: Object.fromEntries(
        initialResponses.map(({ agent, response }) => [agent, { initial: response }])
      ),
      currentStep: 2,
    }));

    // Step 2: Consensus building rounds
    const maxRounds = 3;
    let consensusReached = false;

    for (let round = 0; round < maxRounds && !consensusReached; round++) {
      const consensusResponses = await Promise.all(
        agents.map(async (agent) => {
          const consensusData = {
            ...request,
            message: `${request.message} [Consensus Round ${round + 1}]`,
          };
          const response = await simulateAgentResponse(agent, consensusData, 'consensus');
          return { agent, response };
        })
      );

      // Check for consensus
      const consensusScores = consensusResponses
        .map(({ response }) => response.data?.consensus_score || 0)
        .filter(score => score > 0);

      if (consensusScores.length > 0 && consensusScores.reduce((a, b) => a + b, 0) / consensusScores.length > 0.8) {
        consensusReached = true;
      }

      setCollaborationState(prev => ({
        ...prev,
        agentResponses: {
          ...prev.agentResponses,
          ...Object.fromEntries(
            consensusResponses.map(({ agent, response }) => [
              agent,
              { ...prev.agentResponses[agent], [`consensus_round_${round}`]: response }
            ])
          ),
        },
        currentStep: 3 + round,
      }));
    }

  }, []);

  const executeHierarchicalCollaboration = useCallback(async (
    request: CollaborationRequest,
    agents: string[],
    timeout: number
  ) => {
    // Define hierarchy: privacy -> sentiment -> analytics -> resource -> wellness
    const hierarchy = [
      'policy_privacy',
      'sentiment_risk_detection',
      'analytics_reporting',
      'resource_recommendation',
      'wellness_companion',
    ].filter(agent => agents.includes(agent));

    let currentData = request;
    let step = 1;

    for (const agent of hierarchy) {
      setCollaborationState(prev => ({ ...prev, currentStep: step }));
      
      const response = await simulateAgentResponse(agent, currentData, 'hierarchical');
      
      setCollaborationState(prev => ({
        ...prev,
        agentResponses: {
          ...prev.agentResponses,
          [agent]: { hierarchical: response, level: hierarchy.indexOf(agent) }
        },
      }));

      // Pass enhanced data to next level
      if (response.success && response.data) {
        currentData = {
          ...currentData,
          message: `${currentData.message} [Enhanced by ${agent}: ${JSON.stringify(response.data)}]`,
        };
      }

      step++;
    }

  }, []);

  const executePeerCollaboration = useCallback(async (
    request: CollaborationRequest,
    agents: string[],
    timeout: number
  ) => {
    setCollaborationState(prev => ({ ...prev, currentStep: 1 }));
    
    // Execute all agents in parallel
    const peerResponses = await Promise.all(
      agents.map(async (agent) => {
        const response = await simulateAgentResponse(agent, request, 'peer');
        return { agent, response };
      })
    );

    setCollaborationState(prev => ({
      ...prev,
      agentResponses: Object.fromEntries(
        peerResponses.map(({ agent, response }) => [agent, { peer: response }])
      ),
      currentStep: 2,
    }));

  }, []);

  const executeCompetitiveCollaboration = useCallback(async (
    request: CollaborationRequest,
    agents: string[],
    timeout: number
  ) => {
    setCollaborationState(prev => ({ ...prev, currentStep: 1 }));
    
    // All agents compete to provide the best solution
    const competitiveResponses = await Promise.all(
      agents.map(async (agent) => {
        const response = await simulateAgentResponse(agent, request, 'competitive');
        return { agent, response };
      })
    );

    // Evaluate and select best response
    const bestResponse = evaluateCompetitiveResponses(competitiveResponses);

    setCollaborationState(prev => ({
      ...prev,
      agentResponses: Object.fromEntries(
        competitiveResponses.map(({ agent, response }) => [
          agent,
          { competitive: response, isBest: response === bestResponse }
        ])
      ),
      currentStep: 2,
    }));

  }, []);

  const simulateAgentResponse = useCallback(async (
    agent: string,
    request: CollaborationRequest,
    responseType: string
  ) => {
    const startTime = Date.now();
    
    // Simulate processing time
    const processingTime = Math.random() * 2000 + 500; // 500-2500ms
    await new Promise(resolve => setTimeout(resolve, processingTime));
    
    const responseTime = Date.now() - startTime;
    const success = Math.random() > 0.1; // 90% success rate
    const confidence = Math.random() * 0.3 + 0.7; // 70-100% confidence

    // Generate response based on agent type
    const response = generateAgentResponse(agent, request, responseType, success, confidence);

    // Update performance metrics
    setCollaborationState(prev => ({
      ...prev,
      performanceMetrics: {
        ...prev.performanceMetrics,
        [agent]: {
          responseTime,
          success,
          confidence,
        },
      },
    }));

    return response;
  }, []);

  const generateAgentResponse = useCallback((
    agent: string,
    request: CollaborationRequest,
    responseType: string,
    success: boolean,
    confidence: number
  ) => {
    if (!success) {
      return {
        success: false,
        data: {},
        message: `Agent ${agent} failed to process request`,
        confidence: 0,
      };
    }

    const baseResponse = {
      success: true,
      confidence,
      timestamp: new Date().toISOString(),
    };

    switch (agent) {
      case 'wellness_companion':
        return {
          ...baseResponse,
          data: {
            emotional_support: 'I understand how you\'re feeling and I\'m here to help.',
            conversation_guidance: 'Let\'s explore this together.',
            escalation_needed: confidence < 0.8,
          },
          message: 'Provided empathetic support and conversation guidance',
        };

      case 'sentiment_risk_detection':
        return {
          ...baseResponse,
          data: {
            sentiment_score: Math.random() * 2 - 1, // -1 to 1
            risk_level: Math.random(),
            risk_indicators: ['stress', 'overwhelm'],
            confidence: confidence,
          },
          message: 'Analyzed sentiment and assessed risk level',
        };

      case 'resource_recommendation':
        return {
          ...baseResponse,
          data: {
            recommended_resources: [
              { id: 'meditation_101', title: 'Meditation Basics', confidence: confidence },
              { id: 'stress_management', title: 'Stress Management Techniques', confidence: confidence },
            ],
            resource_count: 2,
            match_score: confidence,
          },
          message: 'Generated personalized resource recommendations',
        };

      case 'analytics_reporting':
        return {
          ...baseResponse,
          data: {
            wellness_score: Math.random() * 100,
            trend_analysis: 'Improving over the last 7 days',
            insights: ['Consistent check-ins', 'Positive mood trends'],
            confidence: confidence,
          },
          message: 'Generated wellness analytics and insights',
        };

      case 'policy_privacy':
        return {
          ...baseResponse,
          data: {
            privacy_compliant: true,
            data_anonymized: true,
            compliance_score: 0.95,
            audit_trail: 'Generated',
          },
          message: 'Ensured privacy compliance and data protection',
        };

      default:
        return {
          ...baseResponse,
          data: { processed: true },
          message: `Processed request using ${agent}`,
        };
    }
  }, []);

  const evaluateCompetitiveResponses = useCallback((responses: Array<{ agent: string; response: any }>) => {
    // Evaluate responses based on multiple criteria
    const scoredResponses = responses.map(({ agent, response }) => {
      let score = 0;
      
      if (response.success) score += 0.3;
      if (response.data && Object.keys(response.data).length > 0) score += 0.2;
      if (response.confidence) score += response.confidence * 0.3;
      if (response.message && response.message.length > 10) score += 0.2;
      
      return { agent, response, score };
    });

    // Return the response with the highest score
    return scoredResponses.reduce((best, current) => 
      current.score > best.score ? current : best
    ).response;
  }, []);

  const getAgentsForPattern = useCallback((pattern: AgentCollaborationState['collaborationPattern']) => {
    switch (pattern) {
      case 'emergent':
        return ['wellness_companion', 'sentiment_risk_detection', 'resource_recommendation'];
      case 'consensus':
        return ['wellness_companion', 'sentiment_risk_detection', 'analytics_reporting'];
      case 'hierarchical':
        return ['policy_privacy', 'sentiment_risk_detection', 'analytics_reporting', 'resource_recommendation', 'wellness_companion'];
      case 'peer_to_peer':
        return ['wellness_companion', 'sentiment_risk_detection', 'resource_recommendation'];
      case 'competitive':
        return ['wellness_companion', 'sentiment_risk_detection', 'resource_recommendation', 'analytics_reporting'];
      default:
        return ['wellness_companion'];
    }
  }, []);

  const getTotalStepsForPattern = useCallback((pattern: AgentCollaborationState['collaborationPattern']) => {
    switch (pattern) {
      case 'emergent':
        return 3;
      case 'consensus':
        return 5; // Initial + up to 3 consensus rounds + final
      case 'hierarchical':
        return 5; // One step per agent in hierarchy
      case 'peer_to_peer':
        return 2;
      case 'competitive':
        return 2;
      default:
        return 1;
    }
  }, []);

  const completeCollaboration = useCallback(() => {
    const collaborationTime = Date.now() - startTimeRef.current;
    
    setCollaborationState(prev => ({
      ...prev,
      isActive: false,
      collaborationTime,
    }));

    if (collaborationTimeoutRef.current) {
      clearTimeout(collaborationTimeoutRef.current);
      collaborationTimeoutRef.current = null;
    }

    dispatch(addNotification({
      type: 'success',
      title: 'Collaboration Complete',
      message: `Agent collaboration completed in ${(collaborationTime / 1000).toFixed(1)} seconds.`,
    }));
  }, [dispatch]);

  const cancelCollaboration = useCallback(() => {
    setCollaborationState(prev => ({
      ...prev,
      isActive: false,
    }));

    if (collaborationTimeoutRef.current) {
      clearTimeout(collaborationTimeoutRef.current);
      collaborationTimeoutRef.current = null;
    }

    dispatch(addNotification({
      type: 'info',
      title: 'Collaboration Cancelled',
      message: 'Agent collaboration was cancelled.',
    }));
  }, [dispatch]);

  // Update collaboration time while active
  useEffect(() => {
    if (collaborationState.isActive) {
      const interval = setInterval(() => {
        setCollaborationState(prev => ({
          ...prev,
          collaborationTime: Date.now() - startTimeRef.current,
        }));
      }, 100);

      return () => clearInterval(interval);
    }
  }, [collaborationState.isActive]);

  return {
    collaborationState,
    agentCapabilities,
    initiateCollaboration,
    cancelCollaboration,
    getAgentCapabilities: (agentId: string) => agentCapabilities[agentId] || [],
  };
};
