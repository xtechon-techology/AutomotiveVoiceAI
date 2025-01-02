from fnmatch import translate

import streamlit as st

from utils.storage_util import save_streamlit_audio_to_local_file, upload_to_azure, get_downloaded_blob_file
from voiceai.speech_converted_by_audio_file import get_audio_translation_from_file

# Main application logic
audio_value = st.audio_input("Record a voice message")
blob_url = None
file_path = None
if audio_value:
    st.audio(audio_value)

    # Save audio value to file
    file_path = save_streamlit_audio_to_local_file(audio_value)
    st.write("File saved at:", file_path)
    if file_path:
        # Upload to Azure Blob Storage
        blob_url = upload_to_azure(file_path)
        if blob_url:
            st.write("File successfully uploaded and accessible at:", blob_url)

download = st.button("Download")
downloaded_file_name = None
if download:
    downloaded_file_name = get_downloaded_blob_file(file_path)
    st.write("File downloaded successfully:", downloaded_file_name)

translate = st.button("Translate")

if translate:
    st.write("Translation in progress...")
    question = get_audio_translation_from_file(downloaded_file_name)
    st.write("Translated question:", question)