
import streamlit as st
import google.generativeai as genai
import os
from google.api_core import exceptions
from dotenv import load_dotenv
import time
from gtts import gTTS
import tempfile

# Load environment variables
load_dotenv()

# Load the API key from the environment variable
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("Gemini API key not found. Please set the GEMINI_API_KEY environment variable.")
    st.stop()

# Configure the Gemini API
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')  # Initialize the model

MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

# Define language options for the feedback system
LANGUAGES = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Urdu": "ur",
    "Chinese (Simplified)": "zh-cn"
}

def simulate_emergency_scenario(scenario_type, user_input, lang_code):
    # Generate feedback based on a specific emergency simulation or a conversation
    prompt = f"Simulate a dispatcher response for the following emergency scenario: {scenario_type}. The user input is: {user_input}. Provide feedback on what could be improved."

    try:
        response = model.generate_content(f"{prompt}")
        return response.text
    except exceptions.GoogleAPIError as e:
        st.error(f"Failed to simulate the emergency scenario. Error: {str(e)}")
        return "There was an error in the simulation."

def generate_tts_audio(text, lang_code):
    # Generate TTS audio from the provided text and language code
    tts = gTTS(text=text, lang=lang_code)
    
    # Save the audio to a temporary file
    audio_path = "audio_output.mp3"
    tts.save(audio_path)
    
    return audio_path

def audio_player(audio_path):
    # Display an audio player in Streamlit
    audio_file = open(audio_path, "rb")
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/mp3")

def main():
    st.title("Emergency Dispatch Conversation with AI Feedback")

    # Select language for analysis and audio feedback
    language = st.selectbox("Select language for feedback:", list(LANGUAGES.keys()))
    lang_code = LANGUAGES[language]

    # Select the scenario type for simulation
    scenario_type = st.selectbox("Select scenario type:", ["Medical Emergency", "Fire Emergency", "Traffic Accident", "Natural Disaster"])

    # Input for user conversation or dispatcher's response
    user_input = st.text_area(f"Input conversation for the selected '{scenario_type}' scenario:")

    if user_input:
        with st.spinner("AI is generating feedback..."):
            feedback = simulate_emergency_scenario(scenario_type, user_input, lang_code)
            st.subheader("AI Feedback:")
            st.write(feedback)

            # Generate audio of the feedback
            audio_path = generate_tts_audio(feedback, lang_code)
            st.write("Listen to the feedback:")
            audio_player(audio_path)

    # Footer with "Made by Shan"
    st.markdown("---")
    st.markdown("<p style='text-align: center;'>😎 Made by Shan-Ul-Haq 😎</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()

