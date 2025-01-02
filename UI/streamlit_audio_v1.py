import streamlit as st
import base64
from azure.storage.blob import BlobServiceClient

# Azure Blob Storage configuration
STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=automotivestorage;AccountKey=OIKjIkzgC/c+sPLrUappeuJO8/felfUV2YTuiiX1s0nlTUH9IuhEjnhnlbw9DyJmU+KNjzsLxlWD+AStLINdqA==;EndpointSuffix=core.windows.net"
CONTAINER_NAME = "audiocontainer"

# Initialize the Azure Blob Service client
blob_service_client = BlobServiceClient.from_connection_string(STORAGE_CONNECTION_STRING)

# Function to save audio from Base64
def save_audio_from_base64(base64_audio):
    st.write("Saving audio from Base64...")
    try:
        # Remove the "data:audio/wav;base64," prefix if present
        audio_data = base64_audio.split(",")[1]
        audio_bytes = base64.b64decode(audio_data)

        # Save to file
        file_path = "user_audio.wav"
        with open(file_path, "wb") as audio_file:
            audio_file.write(audio_bytes)

        st.success(f"Audio file saved at: {file_path}")
        return file_path
    except Exception as e:
        st.error(f"Error saving audio: {e}")
        return None

# Function to save the uploaded audio file
def save_uploaded_audio(uploaded_file):
    try:
        # Save the uploaded file to a path
        file_path = "user_audio.wav"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())
        st.success(f"Audio file saved at: {file_path}")
        return file_path
    except Exception as e:
        st.error(f"Error saving audio: {e}")
        return None

# Function to upload file to Azure Blob Storage
def upload_to_azure(file_path):
    try:
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=file_path)

        # Upload the file
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

        st.success(f"File uploaded to Azure Blob Storage: {file_path}")
        blob_url = blob_client.url
        st.write("Blob URL:", blob_url)
        return blob_url
    except Exception as e:
        st.error(f"Error uploading file to Azure: {e}")
        return None

# Main application logic
audio_value = st.audio_input("Record a voice message")

if audio_value:
    st.audio(audio_value)

    # Save audio value to file
    file_path = save_uploaded_audio(audio_value)

    if file_path:
        # Upload to Azure Blob Storage
        blob_url = upload_to_azure(file_path)
        if blob_url:
            st.write("File successfully uploaded and accessible at:", blob_url)
