import gradio as gr
import os
from PIL import Image
import io
import base64

# Import our modules with error handling
try:
    from mainfile import encode_image, get_image_analysis
    print("✓ Successfully imported mainfile")
except ImportError as e:
    print(f"✗ Failed to import mainfile: {e}")
    
    # Fallback function
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def get_image_analysis(base64_image):
        return "Image analysis not available - mainfile import failed"

try:
    from Themedbot import text_to_speech_with_gtts, text_to_speech_with_elevenlabs
    print("✓ Successfully imported Themedbot")
except ImportError as e:
    print(f"✗ Failed to import Themedbot: {e}")
    
    # Fallback function  
    def text_to_speech_with_gtts(text, filepath):
        print(f"TTS not available: {text}")
    
    def text_to_speech_with_elevenlabs(text, filepath):
        print(f"ElevenLabs TTS not available: {text}")

# Server-safe audio processing (no PyAudio dependency)
def process_audio_text(audio_text):
    """Process text input instead of audio for server deployment"""
    if not audio_text or audio_text.strip() == "":
        return "Please enter your symptoms or concerns in the text box."
    
    try:
        # Get GROQ API key
        groq_api_key = os.getenv('GROQ_API_KEY')
        if not groq_api_key:
            print("Warning: GROQ_API_KEY not found")
            return "API configuration error. Please check environment variables."
        
        # For server deployment, we'll just echo back the text for now
        # In production, you would add your medical analysis logic here
        response = f"Thank you for describing your symptoms: '{audio_text}'. Based on your input, I recommend consulting with a healthcare professional for proper diagnosis and treatment."
        
        # Generate audio response (will fall back to gTTS if ElevenLabs not available)
        try:
            output_file = "response_audio.mp3"
            text_to_speech_with_elevenlabs(response, output_file)
            return response, output_file
        except Exception as audio_error:
            print(f"Audio generation failed: {audio_error}")
            return response, None
            
    except Exception as e:
        print(f"Error processing text: {e}")
        return f"Error processing your input: {str(e)}", None

def process_image_analysis(image):
    """Process uploaded image for medical analysis"""
    if image is None:
        return "Please upload an image for analysis."
    
    try:
        # Save the uploaded image temporarily
        temp_image_path = "temp_uploaded_image.jpg"
        image.save(temp_image_path)
        
        # Encode and analyze the image
        base64_image = encode_image(temp_image_path)
        analysis_result = get_image_analysis(base64_image)
        
        # Generate audio response
        try:
            output_file = "image_analysis_audio.mp3"
            text_to_speech_with_elevenlabs(analysis_result, output_file)
            return analysis_result, output_file
        except Exception as audio_error:
            print(f"Audio generation failed: {audio_error}")
            return analysis_result, None
            
    except Exception as e:
        print(f"Error analyzing image: {e}")
        return f"Error analyzing image: {str(e)}", None
    finally:
        # Clean up temporary file
        if os.path.exists("temp_uploaded_image.jpg"):
            os.remove("temp_uploaded_image.jpg")

def create_interface():
    """Create the Gradio interface for server deployment"""
    
    with gr.Blocks(title="AI Medical Assistant") as app:
        gr.Markdown("# 🏥 AI Medical Assistant")
        gr.Markdown("Describe your symptoms or upload medical images for analysis.")
        
        with gr.Tab("Text Input"):
            with gr.Row():
                with gr.Column():
                    text_input = gr.Textbox(
                        label="Describe your symptoms",
                        placeholder="Please describe your symptoms, concerns, or medical questions...",
                        lines=4
                    )
                    text_submit = gr.Button("Analyze Symptoms", variant="primary")
                
                with gr.Column():
                    text_output = gr.Textbox(label="Medical Analysis", lines=8)
                    audio_output = gr.Audio(label="Audio Response", visible=True)
            
            text_submit.click(
                fn=process_audio_text,
                inputs=[text_input],
                outputs=[text_output, audio_output]
            )
        
        with gr.Tab("Image Analysis"):
            with gr.Row():
                with gr.Column():
                    image_input = gr.Image(label="Upload Medical Image", type="pil")
                    image_submit = gr.Button("Analyze Image", variant="primary")
                
                with gr.Column():
                    image_output = gr.Textbox(label="Image Analysis", lines=8)
                    image_audio_output = gr.Audio(label="Audio Response", visible=True)
            
            image_submit.click(
                fn=process_image_analysis,
                inputs=[image_input],
                outputs=[image_output, image_audio_output]
            )
        
        gr.Markdown("⚠️ **Disclaimer**: This is an AI assistant for educational purposes only. Always consult qualified healthcare professionals for medical advice.")
    
    return app

if __name__ == "__main__":
    # Check environment variables
    groq_key = os.getenv('GROQ_API_KEY')
    eleven_key = os.getenv('ELEVENLABS_API_KEY')
    
    print("=== AI Medical Assistant Server ===")
    print(f"GROQ API Key: {'✓ Set' if groq_key else '✗ Missing'}")
    print(f"ElevenLabs API Key: {'✓ Set' if eleven_key else '✗ Missing'}")
    
    if not groq_key:
        print("Warning: GROQ_API_KEY not found. Some features may not work.")
    
    # Create and launch the app
    app = create_interface()
    
    # Launch on all interfaces for EC2 deployment
    app.launch(
        server_name="0.0.0.0",  # Listen on all interfaces
        server_port=7860,       # Standard Gradio port
        share=False,            # Don't create public link
        debug=True              # Enable debug mode
    )