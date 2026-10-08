from gtts import gTTS
import io

def generate_audio(text: str, lang: str = 'English') -> bytes:
    """
    Generates TTS audio bytes for the given text using Google TTS (gTTS).
    """
    try:
        # Map selected language to gTTS language codes
        language_code = 'ur' if lang.lower() == 'urdu' else 'en'
        
        tts = gTTS(text=text, lang=language_code, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        return fp.getvalue()
    except Exception as e:
        print(f"TTS Error: {e}")
        return None
