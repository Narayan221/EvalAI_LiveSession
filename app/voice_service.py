import asyncio
import io
from groq import AsyncGroq
import os
from dotenv import load_dotenv
import torch
from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
import soundfile as sf
import numpy as np

load_dotenv()

class VoiceService:
    def __init__(self):
        self.groq_client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Skip SpeechT5 for now - use better TTS
        print("Using system TTS with optimized settings...")
        import pyttsx3
        self.tts = pyttsx3.init()
        self.tts_engine = "pyttsx3"
        
        # Find the best male voice
        voices = self.tts.getProperty('voices')
        if voices:
            # Look for specific good male voices
            for voice in voices:
                if any(name in voice.name.lower() for name in ['david', 'mark', 'male', 'george', 'james']):
                    self.tts.setProperty('voice', voice.id)
                    print(f"Using voice: {voice.name}")
                    break
            else:
                # Use first available voice
                self.tts.setProperty('voice', voices[0].id)
                print(f"Using default voice: {voices[0].name}")
        
        # Optimize for more natural speech
        self.tts.setProperty('rate', 140)    # Slower for clarity
        self.tts.setProperty('volume', 0.9)  # Slightly louder
        print("Voice service ready")
    
    async def speech_to_text(self, audio_file_path: str) -> str:
        """Convert speech to text using Groq Whisper"""
        with open(audio_file_path, "rb") as file:
            transcription = await self.groq_client.audio.transcriptions.create(
                file=(audio_file_path, file.read()),
                model="whisper-large-v3",
            )
        return transcription.text
    
    def clean_text_for_speech(self, text: str) -> str:
        """Clean text for natural speech synthesis"""
        import re
        
        # Remove ALL markdown and formatting
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Remove **bold**
        text = re.sub(r'\*(.*?)\*', r'\1', text)      # Remove *italic*
        text = re.sub(r'`(.*?)`', r'\1', text)        # Remove `code`
        text = re.sub(r'#{1,6}\s*', '', text)         # Remove headers
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)  # Remove links
        
        # Remove mode indicators and brackets
        text = re.sub(r'\[.*?MODE\]\s*', '', text)    # Remove [GITTER MODE], [BARGAIN MODE]
        text = re.sub(r'\[.*?\]', '', text)           # Remove any remaining brackets
        
        # Fix common speech issues
        text = text.replace('&', 'and')
        text = text.replace('@', 'at')
        text = text.replace('#', 'number')
        text = text.replace('%', 'percent')
        text = text.replace('*', '')  # Remove any remaining asterisks
        
        # Remove extra whitespace and newlines
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    async def text_to_speech(self, text: str, output_path: str = "output.wav") -> str:
        """Convert text to speech using SpeechT5 or fallback"""
        # Clean text for better speech
        clean_text = self.clean_text_for_speech(text)
        
        def generate_speech():
            try:
                # Use optimized pyttsx3
                self.tts.save_to_file(clean_text, output_path)
                self.tts.runAndWait()
                    
            except Exception as e:
                print(f"TTS generation failed: {e}")
        
        # Run in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, generate_speech)
        
        return output_path