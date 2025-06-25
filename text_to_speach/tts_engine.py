# tts_engine.py

import pyttsx3                      # Import the pyttsx3 library for text-to-speech
import tempfile                     # Import tempfile to create temporary files

# Initialize a single pyttsx3 engine instance when the module is loaded
engine = pyttsx3.init()             # .init() returns an Engine object

def list_voices():
    """
    Return a list of (voice_id, description) for all installed voices.
    """
    voices = engine.getProperty('voices')  # Query engine for available voices
    result = []                            # Prepare list to hold (id, desc) tuples
    for v in voices:                       # Iterate over each Voice object
        lang = v.languages[0]              # Grab the first language code
        if isinstance(lang, bytes):        # Some drivers return bytes for languages
            try:
                lang = lang.decode('utf-8')# Decode bytes to string if needed
            except:
                lang = str(lang)           # Fallback: convert to generic string
        # Build a human-friendly description: "Name — en_US Female"
        desc = f"{v.name} — {lang} {v.gender or ''}".strip()
        result.append((v.id, desc))        # Add the (voice_id, description) tuple
    return result                          # Return the full list

def set_voice(voice_id):
    """Set the engine’s voice by passing its internal ID."""
    engine.setProperty('voice', voice_id)# Configure the engine’s 'voice' property

def set_rate(rate: int):
    """Set the speed (words per minute)."""
    engine.setProperty('rate', rate)      # Configure the engine’s 'rate' property

def set_volume(volume: float):
    """Set the volume (0.0 to 1.0)."""
    engine.setProperty('volume', volume)  # Configure the engine’s 'volume' property

def save_to_file(text: str) -> str:
    """
    Synthesize `text` to a temporary WAV file.
    Returns the file path of the created WAV.
    """
    tf = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    # Create a temp file that persists after close, with .wav extension
    path = tf.name                        # Grab the filename (full path)
    tf.close()                            # Close the handle so pyttsx3 can write to it

    engine.save_to_file(text, path)       # Queue up the text-to-speech conversion
    engine.runAndWait()                   # Process queued commands until done
    return path                           # Return the path to the WAV file