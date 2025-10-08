import os
import gradio as gr
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from mainfile import encode_image, analyze_img_with_query
from patientvoice import record_audio, transcribe_with_grok
from Themedbot import text_to_speech_with_gtts, text_to_speech_with_elevenlabs

system_prompt = """
You have to act as a professional doctor, i know you are not but this is for learning purpose. 
What's in this image?. Do you find anything wrong with it medically? 
If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
Donot say 'In the image I see' but say 'With what I see, I think you have ....'
Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
Keep your answer concise (max 2 sentences). No preamble, start your answer right away please
"""

def process_inputs(audio_filepath, image_filepath):
    speech_to_text_output = ""
    
    # Get transcription if audio provided
    if audio_filepath:
        speech_to_text_output = transcribe_with_grok(GROQ_API_KEY=os.environ.get("GROQ_API_KEY"),
                                                     audio_filepath=audio_filepath,
                                                     stt_model="whisper-large-v3")
    
    # Process image if provided (prioritized)
    if image_filepath:
        if speech_to_text_output:
            combined_query = system_prompt + f" Additionally, the patient mentioned: '{speech_to_text_output}'"
        else:
            combined_query = system_prompt
            
        doctor_response = analyze_img_with_query(query=combined_query, 
                                               encoded_image=encode_image(image_filepath), 
                                               model="meta-llama/llama-4-scout-17b-16e-instruct")
    elif speech_to_text_output:
        doctor_response = f"Based on your description: {speech_to_text_output}, I recommend consulting with a healthcare professional for proper diagnosis."
    else:
        doctor_response = "Please provide either audio input or upload an image for analysis."
    
    # Generate audio response
    text_to_speech_with_gtts(doctor_response, "final.mp3")
    
    return speech_to_text_output, doctor_response, "final.mp3"

iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath", label="Record your symptoms"),
        gr.Image(type="filepath", label="Upload medical image"),
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio(label="Doctor's Voice Response"),
    ],
    title="AI Medical Assistant",
    description="Upload an image and/or record your symptoms to get medical advice",
)

iface.launch(share=True)