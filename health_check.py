#!/usr/bin/env python3
"""
AIMedAssistant Health Check Script
This script tests all components to verify the application is working correctly.
"""

import os
import sys
from dotenv import load_dotenv

def print_status(test_name, status, details=""):
    """Print test status with consistent formatting"""
    status_symbol = "✅" if status else "❌"
    print(f"{status_symbol} {test_name}")
    if details:
        print(f"   {details}")
    print()

def test_environment_setup():
    """Test environment variables and basic setup"""
    print("🔧 Testing Environment Setup...")
    
    # Load environment variables
    load_dotenv()
    
    # Check API keys
    groq_key = os.getenv("GROQ_API_KEY")
    elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
    
    print_status("Environment file loaded", True)
    print_status("GROQ_API_KEY present", bool(groq_key), f"Length: {len(groq_key) if groq_key else 0}")
    print_status("ELEVENLABS_API_KEY present", bool(elevenlabs_key), f"Length: {len(elevenlabs_key) if elevenlabs_key else 0}")
    
    return bool(groq_key and elevenlabs_key)

def test_module_imports():
    """Test if all required modules can be imported"""
    print("📦 Testing Module Imports...")
    
    modules_to_test = [
        ("gradio", "gradio"),
        ("groq", "groq"),
        ("speech_recognition", "speech_recognition"),
        ("gtts", "gtts"),
        ("elevenlabs", "elevenlabs"),
        ("pydub", "pydub"),
        ("PIL", "pillow"),
        ("numpy", "numpy"),
        ("pandas", "pandas"),
        ("requests", "requests"),
        ("python-dotenv", "dotenv")
    ]
    
    all_imports_successful = True
    
    for module_name, import_name in modules_to_test:
        try:
            __import__(import_name)
            print_status(f"Import {module_name}", True)
        except ImportError as e:
            print_status(f"Import {module_name}", False, str(e))
            all_imports_successful = False
    
    return all_imports_successful

def test_project_modules():
    """Test if project-specific modules can be imported"""
    print("🏗️ Testing Project Modules...")
    
    project_modules = [
        "mainfile",
        "patientvoice", 
        "Themedbot",
        "gradio_app"
    ]
    
    all_modules_successful = True
    
    for module in project_modules:
        try:
            __import__(module)
            print_status(f"Import {module}.py", True)
        except Exception as e:
            print_status(f"Import {module}.py", False, str(e))
            all_modules_successful = False
    
    return all_modules_successful

def test_file_structure():
    """Test if all required files exist"""
    print("📁 Testing File Structure...")
    
    required_files = [
        "mainfile.py",
        "gradio_app.py", 
        "patientvoice.py",
        "Themedbot.py",
        "Requirements.txt",
        "Pipfile",
        "Dockerfile",
        "start.sh",
        ".env",
        "README.md"
    ]
    
    all_files_present = True
    
    for file_name in required_files:
        exists = os.path.exists(file_name)
        print_status(f"File {file_name}", exists)
        if not exists:
            all_files_present = False
    
    return all_files_present

def test_api_connectivity():
    """Test API connectivity (without making actual calls)"""
    print("🌐 Testing API Configuration...")
    
    try:
        from groq import Groq
        groq_key = os.getenv("GROQ_API_KEY")
        if groq_key:
            client = Groq(api_key=groq_key)
            print_status("GROQ client initialization", True)
        else:
            print_status("GROQ client initialization", False, "No API key")
    except Exception as e:
        print_status("GROQ client initialization", False, str(e))
    
    try:
        from elevenlabs.client import ElevenLabs
        elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
        if elevenlabs_key:
            client = ElevenLabs(api_key=elevenlabs_key)
            print_status("ElevenLabs client initialization", True)
        else:
            print_status("ElevenLabs client initialization", False, "No API key")
    except Exception as e:
        print_status("ElevenLabs client initialization", False, str(e))

def test_gradio_interface():
    """Test if Gradio interface can be created (without launching)"""
    print("🖥️ Testing Gradio Interface...")
    
    try:
        import gradio as gr
        from gradio_app import process_inputs
        
        # Test interface creation
        iface = gr.Interface(
            fn=lambda x, y: ("test", "test", None),  # Mock function
            inputs=[
                gr.Audio(sources=["microphone"], type="filepath"),
                gr.Image(type="filepath"),
            ],
            outputs=[
                gr.Textbox(),
                gr.Textbox(),
                gr.Audio(),
            ],
            title="Test Interface"
        )
        print_status("Gradio interface creation", True)
        return True
    except Exception as e:
        print_status("Gradio interface creation", False, str(e))
        return False

def main():
    """Run all tests"""
    print("🩺 AIMedAssistant Health Check")
    print("=" * 50)
    
    test_results = []
    
    # Run all tests
    test_results.append(test_file_structure())
    test_results.append(test_environment_setup())
    test_results.append(test_module_imports())
    test_results.append(test_project_modules())
    test_api_connectivity()  # This doesn't return a boolean
    test_results.append(test_gradio_interface())
    
    # Summary
    print("📊 Test Summary")
    print("=" * 50)
    
    passed_tests = sum(test_results)
    total_tests = len(test_results)
    
    if passed_tests == total_tests:
        print("🎉 All critical tests passed! Your application should work correctly.")
        print("💡 If you have valid API keys, you can now run: python gradio_app.py")
    else:
        print(f"⚠️ {total_tests - passed_tests} out of {total_tests} tests failed.")
        print("🔍 Please review the failed tests above and fix the issues.")
    
    print(f"\n✅ Passed: {passed_tests}/{total_tests}")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)