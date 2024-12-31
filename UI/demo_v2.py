import streamlit as st
import azure.cognitiveservices.speech as speechsdk
from configs.config import azure_congnitive_services_config


def recognize_speech_continuously_streamlit():
    """
    Continuously listens to the microphone and returns recognized speech as text.
    """
    # Configure speech settings
    speech_config = speechsdk.SpeechConfig(
        subscription=azure_congnitive_services_config["speech_service_key"],
        region=azure_congnitive_services_config["speech_service_region"],
    )
    speech_config.speech_recognition_language = "en-US"

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )

    recognized_text = []
    is_listening = True

    def handle_recognized(evt):
        nonlocal is_listening
        st.write(f"Recognized: {evt.result.text}")
        recognized_text.append(evt.result.text)

        # Stop listening if a specific phrase is recognized
        if "stop listening" in evt.result.text.lower():
            st.write("Stop command recognized. Ending recognition.")
            is_listening = False
            speech_recognizer.stop_continuous_recognition()

    def handle_canceled(evt):
        st.write(
            f"Speech recognition canceled: {evt.result.cancellation_details.reason}"
        )
        if evt.result.cancellation_details.error_details:
            st.write(f"Error details: {evt.result.cancellation_details.error_details}")
        nonlocal is_listening
        is_listening = False

    # Connect event handlers
    speech_recognizer.recognized.connect(handle_recognized)
    speech_recognizer.canceled.connect(handle_canceled)

    # Start continuous recognition
    speech_recognizer.start_continuous_recognition()

    try:
        while is_listening:
            pass  # Keeps the script running until recognition stops
    except KeyboardInterrupt:
        st.write("\nManual interruption received, stopping recognition.")
        speech_recognizer.stop_continuous_recognition()

    return " ".join(recognized_text)


# Streamlit App Interface
st.title("Azure Speech-to-Text Streamlit App")

if st.button("Start Listening"):
    st.write("Speak into your microphone. Say 'stop listening' to end.")
    result = recognize_speech_continuously_streamlit()
    st.write("\n**Final Recognized Text:**")
    st.write(result)
