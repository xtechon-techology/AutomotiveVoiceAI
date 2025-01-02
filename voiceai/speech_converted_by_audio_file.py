import azure.cognitiveservices.speech as speechsdk
from configs.config import azure_congnitive_services_config


def get_audio_translation_from_file(download_file_path):
    # Configure speech settings
    speech_config = speechsdk.SpeechConfig(
        subscription=azure_congnitive_services_config["speech_service_key"],
        region=azure_congnitive_services_config["speech_service_region"]
    )
    speech_config.speech_recognition_language = "en-US"

    # Configure audio input from the downloaded .wav file
    audio_config = speechsdk.audio.AudioConfig(filename=download_file_path)
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )

    speech_recognition_result = speech_recognizer.recognize_once_async().get()
    print(speech_recognition_result.text)
    return speech_recognition_result.text


if __name__ == "__main__":
    downloaded_file_path = "/Users/vishald/Documents/DWL/AutomotiveVoiceAI/downloaded_user_audio_1735831105.wav"
    user_query = get_audio_translation_from_file(downloaded_file_path)
    print(f"User Query: {user_query}")


