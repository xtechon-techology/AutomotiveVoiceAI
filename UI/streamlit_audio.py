import streamlit as st
import base64

audio_value = st.audio_input("Record a voice message")



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

if audio_value:
    st.audio(audio_value)
    # Save audio value to file
    file_path = save_uploaded_audio(audio_value)
    st.write("File path: ", file_path)


