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
        self.conversation_mode = "gitter"  # gitter or bargain

    async def start_session(self, title: str, description: str) -> str:
        self.session_title = title
        self.session_description = description
        self.session_active = True
        self.conversation_history = []
        self.conversation_mode = "gitter"  # Start with casual mode

        self.session_context = f"""You are an interactive AI conversation partner for: '{title}'
Description: {description}

CONVERSATION MODES:
- GITTER MODE: Casual, exploratory conversation. Be engaging, ask questions, share insights naturally.
- BARGAIN MODE: Decision-focused, negotiation-style. Be decisive, provide clear options, guide toward conclusions.

Your personality:
- Conversational and engaging like ChatGPT voice mode
- Naturally interactive - encourage participation
- Handle interruptions gracefully and build on them
- Adapt your response style based on conversation mode
- Be enthusiastic and personable

INTERRUPTION HANDLING:
- Welcome interruptions as natural conversation flow
- Build on what the user says immediately
- Don't restart - continue from where interrupted
- Make interruptions feel like natural dialogue

Start in GITTER mode with a warm welcome and engage them about the topic."""

        response = await self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "system", "content": self.session_context}],
            max_tokens=150
        )

        ai_response = response.choices[0].message.content
        self.conversation_history.append({"role": "assistant", "content": ai_response})
        return ai_response

    def _classify_message(self, message: str) -> str:
        """Classify message to determine conversation mode"""
        bargain_keywords = [
            "decide", "choose", "negotiate", "price", "deal", "agree", "option", 
            "decision", "select", "pick", "conclude", "finalize", "settle"
        ]
        
        gitter_keywords = [
            "tell me", "explain", "what about", "how", "why", "interesting", 
            "think", "feel", "experience", "story", "example"
        ]
        
        message_lower = message.lower()
        
        bargain_score = sum(1 for keyword in bargain_keywords if keyword in message_lower)
        gitter_score = sum(1 for keyword in gitter_keywords if keyword in message_lower)
        
        if bargain_score > gitter_score:
            return "bargain"
        return "gitter"

    async def process_user_input(self, user_message: str) -> str:
        if not self.session_active:
            return "Please start a session first by providing a title and description."

        # Classify the conversation mode based on user input
        detected_mode = self._classify_message(user_message)
        
        # Switch modes if needed
        mode_changed = False
        if detected_mode != self.conversation_mode:
            self.conversation_mode = detected_mode
            mode_changed = True

        self.conversation_history.append({"role": "user", "content": user_message})
        
        print(f"DEBUG: Message: '{user_message}' | Mode: {self.conversation_mode} | Changed: {mode_changed}")

        # Build context-aware system prompt
        mode_context = self._get_mode_context()
        
        system_prompt = f"""{self.session_context}

CURRENT MODE: {self.conversation_mode.upper()}
{mode_context}

RESPONSE GUIDELINES:
- This is a natural conversation - the user just interrupted or responded
- Build directly on what they said
- Don't restart or ignore the interruption
- Match the conversation mode style
- Keep responses conversational (2-3 sentences)
- Always end with engagement (question or prompt)
- Make interruptions feel natural and welcomed

Respond naturally to their input in {self.conversation_mode} mode."""

        response = await self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                *self.conversation_history[-8:]  # Keep recent context
            ],
            max_tokens=150
        )

        ai_response = response.choices[0].message.content
        
        # Add mode indicator to response if mode changed
        if mode_changed:
            mode_indicator = f"[{self.conversation_mode.upper()} MODE] "
            ai_response = mode_indicator + ai_response
        
        self.conversation_history.append({"role": "assistant", "content": ai_response})
        return ai_response

    def _get_mode_context(self) -> str:
        """Get context for current conversation mode"""
        if self.conversation_mode == "bargain":
            return """BARGAIN MODE ACTIVE:
- Be decisive and solution-oriented
- Provide clear options and recommendations
- Guide toward decisions and conclusions
- Use phrases like "Here are your options", "I recommend", "The best choice is"
- Help them reach actionable outcomes"""
        else:
            return """GITTER MODE ACTIVE:
- Be exploratory and engaging
- Ask follow-up questions
- Share interesting insights and examples
- Use phrases like "That's fascinating", "What do you think about", "Have you considered"
- Keep the conversation flowing naturally"""