import asyncio
import os
from typing import Dict, List
from groq import AsyncGroq
from dotenv import load_dotenv

load_dotenv()

class AISessionManager:
    def __init__(self):
        self.client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
        self.session_title = ""
        self.session_description = ""
        self.conversation_history: List[Dict] = []
        self.session_active = False
        self.session_context = ""

    async def start_session(self, title: str, description: str) -> str:
        self.session_title = title
        self.session_description = description
        self.session_active = True
        self.conversation_history = []

        self.session_context = f"""You are an interactive AI conversation partner for: '{title}'
Description: {description}

Your personality:
- Conversational and engaging like ChatGPT voice mode
- Naturally interactive - ask questions and encourage participation
- Respond to interruptions gracefully
- Keep conversations flowing naturally
- Be enthusiastic and personable

Your approach:
1. Start with a warm, conversational welcome
2. Share knowledge in bite-sized, digestible pieces
3. Frequently ask "What do you think?" or "Have you experienced this?"
4. Encourage the participant to share their thoughts
5. Build on their responses naturally
6. Make it feel like a friendly expert conversation

Start with a brief welcome and immediately engage them with a question about their experience or interest in the topic."""

        response = await self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "system", "content": self.session_context}],
            max_tokens=150
        )

        ai_response = response.choices[0].message.content
        self.conversation_history.append({"role": "assistant", "content": ai_response})
        return ai_response

    async def process_user_input(self, user_message: str) -> str:
        if not self.session_active:
            return "Please start a session first by providing a title and description."

        self.conversation_history.append({"role": "user", "content": user_message})
        
        system_prompt = f"""{self.session_context}

Conversation Guidelines:
- Respond naturally to what they just said
- Share relevant insights or knowledge
- Ask follow-up questions to keep them engaged
- Be conversational, not lecture-like
- Encourage them to participate and share
- Keep responses concise but valuable (2-3 sentences max)
- Always end with a question or prompt to continue the conversation

Respond to their input in a natural, engaging way."""

        response = await self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                *self.conversation_history[-10:]
            ],
            max_tokens=150
        )

        ai_response = response.choices[0].message.content
        self.conversation_history.append({"role": "assistant", "content": ai_response})
        return ai_response