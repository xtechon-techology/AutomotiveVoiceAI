import azure.cognitiveservices.speech as speechsdk
from configs.config import azure_congnitive_services_config


def recognize_speech_continuously():
    """
    Continuously listens to the microphone and returns recognized speech as text.
    """
    # Configure speech settings
    speech_config = speechsdk.SpeechConfig(
        subscription=azure_congnitive_services_config["speech_service_key"],
        region=azure_congnitive_services_config["speech_service_region"]
    )
    speech_config.speech_recognition_language = "en-US"

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )

    print("Speak into your microphone. Say 'stop listening' to end.")
    recognized_text = []
    is_listening = True

    def handle_recognized(evt):
        nonlocal is_listening
        print(f"Recognized: {evt.result.text}")
        recognized_text.append(evt.result.text)

        # Stop listening if a specific phrase is recognized
        if "stop listening" in evt.result.text.lower():
            print("Stop command recognized. Ending recognition.")
            is_listening = False
            speech_recognizer.stop_continuous_recognition()

    def handle_canceled(evt):
        print(f"Speech recognition canceled: {evt.result.cancellation_details.reason}")
        if evt.result.cancellation_details.error_details:
            print(f"Error details: {evt.result.cancellation_details.error_details}")
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
        print("\nManual interruption received, stopping recognition.")
        speech_recognizer.stop_continuous_recognition()

    return " ".join(recognized_text)


if __name__ == "__main__":
    result = recognize_speech_continuously()
    print("\nFinal Recognized Text:")
    print(result)
