import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
import shutil
import os

# 🔧 Try to detect ffmpeg automatically, fallback to system PATH
try:
    # First try to find ffmpeg in system PATH
    ffmpeg_path = shutil.which('ffmpeg')
    if ffmpeg_path:
        AudioSegment.converter = ffmpeg_path
        AudioSegment.ffmpeg = ffmpeg_path
        AudioSegment.ffprobe = shutil.which('ffprobe') or ffmpeg_path.replace('ffmpeg', 'ffprobe')
    else:
        # If not in PATH, try common Windows locations
        common_paths = [
            r"C:\ffmpeg\bin\ffmpeg.exe",
            r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
            r"C:\Users\user\OneDrive\Desktop\ffmpeg-7.1.1-essentials_build\bin\ffmpeg.exe"
        ]
        for path in common_paths:
            if os.path.exists(path):
                AudioSegment.converter = path
                AudioSegment.ffmpeg = path
                break
except Exception as e:
    logging.warning(f"Could not configure ffmpeg path: {e}. Audio conversion may not work properly.")

logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(levelname)s - %(message)s')

def record_audio(file_path, timeout=20, phrase_time_limit=None):
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start speaking now...")

            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")

            # Try to convert audio to mp3, fallback to wav if ffmpeg not available
            try:
                wav_data = audio_data.get_wav_data()
                audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
                audio_segment.export(file_path, format="mp3", bitrate="128k")
                logging.info(f"Audio saved to {file_path} (MP3)")
            except Exception as conversion_error:
                logging.warning(f"MP3 conversion failed: {conversion_error}")
                # Fallback to WAV format
                wav_file_path = file_path.replace('.mp3', '.wav')
                with open(wav_file_path, 'wb') as f:
                    f.write(audio_data.get_wav_data())
                logging.info(f"Audio saved to {wav_file_path} (WAV fallback)")
                return wav_file_path

            return file_path

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None
        logging.error(f"An error occurred: {e}")

# Call the function with a valid filename
audio_filepath=r"patient_voice_test.mp3"
record_audio(audio_filepath)


import os
from groq import Groq

GROQ_API_KEY=os.environ.get("GROQ_API_KEY")
stt_model = "whisper-large-v3"

def transcribe_with_grok(stt_model, audio_filepath, GROQ_API_KEY):
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is required but not provided")
    
    client = Groq(api_key=GROQ_API_KEY)

    audio_file = open(audio_filepath,"rb")
    transcription =client.audio.transcriptions.create(
        model=stt_model,
        file= audio_file,
        language="en"
    )

    return transcription.text