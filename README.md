# Live AI Session

A real-time AI-led session platform with WebRTC video support and intelligent conversation handling.

## Features

- **AI Session Leadership**: AI guides conversations based on session title
- **WebRTC Video**: Real-time video communication
- **Gitter vs Bargain**: Intelligent conversation mode detection
- **Real-time Chat**: WebSocket-based instant messaging
- **Simple UI**: Clean web interface

## Quick Start

1. **Setup Environment**:
   ```bash
   python setup.py
   ```

2. **Configure**:
   - Update `.env` with your OpenAI API key
   - Modify session title and AI personality

3. **Run**:
   ```bash
   # Activate virtual environment
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Unix/Linux/Mac
   
   # Start server
   python -m app.main
   ```

4. **Access**: Open http://localhost:8000

## Architecture

- **FastAPI Backend**: Handles WebSocket and HTTP requests
- **AI Session Manager**: Manages conversation flow and context
- **WebRTC Handler**: Manages video/audio streams
- **Real-time Communication**: WebSocket for instant interaction

## Conversation Modes

- **Gitter**: Casual conversation, engaging and exploratory
- **Bargain**: Decision-making, negotiation, clear options

## Next Steps

1. Integrate actual WebRTC library (aiortc)
2. Add voice synthesis for AI responses
3. Implement session recording
4. Add user authentication
5. Scale with Redis for multiple sessions