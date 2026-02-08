/**
 * Chat API service layer for the Todo AI Chatbot Integration
 * Handles communication between the frontend chat component and the agent service
 */

interface ChatRequest {
  message: string;
  conversation_id?: string;
  user_id: number;
}

interface ChatResponse {
  reply: string;
  conversation_id: string;
  actions_taken: Array<{[key: string]: any}>;
  timestamp: string;
}

interface ChatHistoryRequest {
  conversation_id: string;
  user_id: number;
  limit?: number;
  offset?: number;
}

interface ChatHistoryResponse {
  messages: Array<{role: string, content: string, timestamp: string}>;
  conversation_id: string;
  total_messages: number;
}

interface NewConversationRequest {
  user_id: number;
}

interface NewConversationResponse {
  conversation_id: string;
  message: string;
}

/**
 * Send a message to the AI agent
 * @param request - The chat request containing the message and context
 * @returns The AI agent's response
 */
export async function sendMessage(request: ChatRequest): Promise<ChatResponse> {
  try {
    const token = localStorage.getItem('access_token');
    if (!token) {
      throw new Error('Authentication required');
    }

    const response = await fetch(`${process.env.NEXT_PUBLIC_CHAT_API_URL || 'http://localhost:8001'}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error sending message:', error);
    throw error;
  }
}

/**
 * Get chat history for a conversation
 * @param request - The request containing conversation and user details
 * @returns The conversation history
 */
export async function getChatHistory(request: ChatHistoryRequest): Promise<ChatHistoryResponse> {
  try {
    const token = localStorage.getItem('access_token');
    if (!token) {
      throw new Error('Authentication required');
    }

    const params = new URLSearchParams({
      conversation_id: request.conversation_id,
      user_id: request.user_id.toString(),
      ...(request.limit && { limit: request.limit.toString() }),
      ...(request.offset && { offset: request.offset.toString() }),
    });

    const response = await fetch(`${process.env.NEXT_PUBLIC_CHAT_API_URL || 'http://localhost:8001'}/api/chat/history?${params}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error getting chat history:', error);
    throw error;
  }
}

/**
 * Start a new conversation
 * @param request - The request containing user details
 * @returns Information about the new conversation
 */
export async function startNewConversation(request: NewConversationRequest): Promise<NewConversationResponse> {
  try {
    const token = localStorage.getItem('access_token');
    if (!token) {
      throw new Error('Authentication required');
    }

    const response = await fetch(`${process.env.NEXT_PUBLIC_CHAT_API_URL || 'http://localhost:8001'}/api/chat/new`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error starting new conversation:', error);
    throw error;
  }
}