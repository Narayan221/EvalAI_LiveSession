#!/usr/bin/env python3
"""Download SpeechT5 models for offline use"""

import os
from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan

def download_speecht5_models():
    """Download all SpeechT5 models to local cache"""
    print("Downloading SpeechT5 models...")
    
    try:
        # Download processor
        print("1/3 Downloading SpeechT5 Processor...")
        processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
        print("✓ Processor downloaded")
        
        # Download TTS model
        print("2/3 Downloading SpeechT5 TTS Model...")
        model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
        print("✓ TTS Model downloaded")
        
        # Download vocoder
        print("3/3 Downloading SpeechT5 HiFiGAN Vocoder...")
        vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")
        print("✓ Vocoder downloaded")
        
        print("\n🎉 All SpeechT5 models downloaded successfully!")
        print("Models are cached locally and ready for offline use.")
        
    except Exception as e:
        print(f"❌ Download failed: {e}")
        print("Check your internet connection and try again.")

if __name__ == "__main__":
    download_speecht5_models()