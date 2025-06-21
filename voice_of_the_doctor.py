import os
from gtts import gTTS

def text_to_speech_with_gtts_old(input_text,output_filepath):
    language="en"

    audioobj= gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)

input_text="Hi this is ai with hassan"
text_to_speech_with_gtts_old(input_text=input_text, output_filepath="gtts_testing.mp3")

import elevenlabs
from elevenlabs.client import ElevenLabs

from dotenv import load_dotenv
load_dotenv()


api_key = os.getenv("ELEVENLABS_API_KEY")
if not api_key:
    raise EnvironmentError("ELEVENLABS_API_KEY not found in environment variables.")

client = ElevenLabs(api_key=api_key)

def text_to_speech_with_elevenlabs_old(input_text, output_filepath):
    audio=client.generate(
        text= input_text ,
        voice= "Aria",
        output_format= "mp3_22050_32",
        model="eleven_turbo_v2"
    )
    elevenlabs.save(audio, output_filepath)

#text_to_speech_with_elevenlabs_old(input_text, output_filepath="elevenlabs_testing.mp3")

#next one
import subprocess
import platform

def text_to_speech_with_gtts(input_text,output_filepath):
    language="en"

    audioobj= gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)
    os_name = platform.system()
    try:
        if os_name == "Darwin": #macOS
            subprocess.run(['afplay',output_filepath])
        elif os_name == "Windows": #windows
            # Convert mp3 to wav before playing
            wav_filepath = output_filepath.replace(".mp3", ".wav")
            subprocess.run([r'C:\Users\user\Desktop\ffmpeg-7.1.1-essentials_build\bin\ffmpeg.exe', '-y', '-i', output_filepath, wav_filepath])

            # Play the WAV file
            subprocess.run(['powershell','-c',f'(New-Object Media.Soundplayer "{wav_filepath}").PlaySync();'])
        elif os_name == "Linux":
            subprocess.run(['aplay',output_filepath])
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

input_text="Hi this is ai with hassan Autoplay testing"
#text_to_speech_with_gtts(input_text=input_text, output_filepath="gtts_testing_autoplay.mp3")

def text_to_speech_with_elevenlabs(input_text, output_filepath):

    audio=client.generate(
        text= input_text ,
        voice= "Aria",
        output_format= "mp3_22050_32",
        model="eleven_turbo_v2"
    )
    elevenlabs.save(audio, output_filepath)

    os_name = platform.system()
    try:
        if os_name == "Darwin": #macOS
            subprocess.run(['afplay',output_filepath])
        elif os_name == "Windows": #windows
            # Convert mp3 to wav before playing
            wav_filepath = output_filepath.replace(".mp3", ".wav")
            subprocess.run([r'C:\Users\user\Desktop\ffmpeg-7.1.1-essentials_build\bin\ffmpeg.exe', '-y', '-i', output_filepath, wav_filepath])
            # Play the WAV file
            subprocess.run(['powershell','-c',f'(New-Object Media.Soundplayer "{wav_filepath}").PlaySync();'])
        elif os_name == "Linux":
            subprocess.run(['aplya',output_filepath])
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

#text_to_speech_with_elevenlabs(input_text, output_filepath="elevenlabs_testing_autoplay.mp3")

