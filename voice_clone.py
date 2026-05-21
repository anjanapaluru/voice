from TTS.api import TTS
import os
import torch

# Initialize TTS once to avoid reloading for every request
# Note: XTTSv2 requires an agreement to terms (handled by environment or manually)
# For local run, xtts automatically downloads models to ~/.local/share/tts or equivalent

def clone_voice(text, speaker_wav_path, output_path):
    """
    Clones the voice from speaker_wav_path and generates speech for 'text'.
    """
    try:
        # Check if CUDA is available for faster generation
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Load the model
        # Using multillingual xtts_v2 as requested
        tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2").to(device)
        
        # Generate speech
        tts.tts_to_file(
            text=text,
            speaker_wav=speaker_wav_path,
            language="en",
            file_path=output_path
        )
        return True
    except Exception as e:
        print(f"Voice Cloning Error: {e}")
        return False
