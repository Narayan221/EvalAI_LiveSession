# Live AI Session Platform

## Overview
A real-time AI-powered video session platform that enables natural voice conversations with intelligent AI responses, featuring modern web interface and advanced conversation management.

## Core Functionalities

### Voice Interaction
- **Continuous Speech Recognition**: WebKit Speech Recognition API for real-time voice input
- **Speech Synthesis**: Browser-native TTS with configurable voice parameters
- **Interruption Support**: Users can interrupt AI mid-speech for natural conversation flow
- **Auto-restart Listening**: Seamless voice recognition restart after AI responses

### AI Conversation Management
- **Session-based Context**: Maintains conversation context throughout the session
- **Topic Locking**: AI strictly adheres to session title and cannot change topics
- **Conversation Modes**: Gitter (exploratory) and Bargain (decision-focused) detection
- **Smart Response Generation**: Context-aware responses based on session parameters

### Video Interface
- **Dual View System**: AI main view with user picture-in-picture
- **View Switching**: Toggle between AI-focused and user-focused layouts
- **Animated AI Avatar**: Visual feedback during AI speech with realistic movements
- **Responsive Design**: Mobile-optimized split-screen layout

### Real-time Communication
- **WebSocket Integration**: Instant bidirectional communication
- **Live Chat**: Text-based messaging alongside voice interaction
- **Session Management**: Structured session start/end with proper cleanup

## Technical Stack

### Backend Technologies
- **FastAPI**: High-performance Python web framework
- **WebSocket**: Real-time communication protocol
- **Groq API**: LLM integration using llama-3.1-8b-instant model
- **Pydantic**: Data validation and settings management

### Frontend Technologies
- **Vanilla JavaScript**: Core application logic
- **WebRTC**: Camera and microphone access
- **CSS3**: Modern styling with gradients, blur effects, and animations
- **HTML5**: Semantic markup and media elements

### AI Integration
- **Groq LLM**: llama-3.1-8b-instant for conversation generation
- **Whisper STT**: Speech-to-text processing via Groq
- **Browser TTS**: Native speech synthesis for AI responses

## Architecture

### Session Flow
1. **Initialization**: User provides session title and description
2. **Media Setup**: Camera and microphone permission and configuration
3. **AI Introduction**: Context-aware session opening by AI
4. **Conversation Loop**: Continuous voice/text interaction with AI responses
5. **Session Cleanup**: Proper resource cleanup on session end

### Conversation System
- **Context Management**: Session title and description maintain conversation focus
- **Response Pipeline**: Voice input → Groq processing → AI response → TTS output
- **Topic Enforcement**: Strict adherence to session parameters prevents topic drift
- **Mode Detection**: Automatic identification of conversation style and approach

### Prompting Strategy
- **System Prompts**: Define AI personality and conversation constraints
- **Context Injection**: Session details integrated into every AI interaction
- **Response Formatting**: Structured AI responses with speaking flags
- **Topic Boundaries**: Hard limits on conversation scope and subject changes

## Key Features

### User Experience
- **Natural Conversation**: ChatGPT-like voice interaction experience
- **Visual Feedback**: Animated AI avatar during speech
- **Intuitive Controls**: Clean, mobile-app-inspired interface
- **Responsive Design**: Optimized for desktop and mobile devices

### Technical Capabilities
- **Real-time Processing**: Sub-second response times for voice interactions
- **Error Handling**: Graceful degradation and automatic recovery
- **Resource Management**: Proper cleanup of media streams and connections
- **Cross-browser Support**: Compatible with modern web browsers

### Security & Performance
- **Environment Configuration**: Secure API key management
- **Media Permissions**: Proper handling of camera/microphone access
- **Connection Management**: Robust WebSocket connection handling
- **Memory Management**: Automatic cleanup on page refresh/close

## Implementation Highlights

### Advanced Prompting
- **Role Definition**: AI acts as professional mentor/facilitator
- **Constraint Setting**: Absolute topic focus with no deviation allowed
- **Context Preservation**: Session parameters maintained throughout conversation
- **Response Control**: Structured output with metadata for frontend processing

### Modern Web Technologies
- **Glass Morphism**: Translucent UI elements with backdrop blur
- **CSS Animations**: Smooth transitions and interactive feedback
- **Responsive Layout**: Flexible grid system adapting to screen sizes
- **Progressive Enhancement**: Core functionality works without advanced features

### Real-time Architecture
- **Event-driven Design**: WebSocket events trigger appropriate responses
- **State Management**: Clean separation of UI state and application logic
- **Error Recovery**: Automatic reconnection and graceful error handling
- **Performance Optimization**: Efficient DOM manipulation and resource usage

## Usage Workflow

1. **Session Setup**: Define conversation topic and optional description
2. **Media Initialization**: Grant camera/microphone permissions
3. **AI Engagement**: AI provides contextual introduction and guidance
4. **Interactive Conversation**: Natural voice/text communication
5. **Session Management**: Clean termination with resource cleanup

This platform demonstrates modern web development practices, AI integration techniques, and user experience design principles in a cohesive, production-ready application.