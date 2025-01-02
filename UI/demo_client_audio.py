import streamlit as st
import base64


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


# Display JavaScript recorder
st.title("Microphone Audio Recorder")
st.components.v1.html("""
    <script>
        let audioContext;
        let recorder;
        let audioChunks = [];

        function startRecording() {
            alert("Attempting to start recording...");
            navigator.mediaDevices.getUserMedia({ audio: true })
                .then(function (stream) {
                    alert("Microphone access granted.");
                    audioContext = new (window.AudioContext || window.webkitAudioContext)();
                    recorder = new MediaRecorder(stream);
                    audioChunks = []; // Reset audio chunks

                    recorder.ondataavailable = function (event) {
                        alert("Data available from recorder.");
                        audioChunks.push(event.data);
                    };

                    recorder.onstop = function () {
                        alert("Recording stopped. Processing audio...");
                        let audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                        let reader = new FileReader();
                        reader.onloadend = function () {
                            let base64Audio = reader.result;
                            alert("Audio converted to Base64. Sending to Streamlit...");
                            window.parent.postMessage({ type: "audio", data: base64Audio }, "*");
                        };
                        reader.readAsDataURL(audioBlob);
                    };

                    recorder.start();
                    alert("Recording started...");
                })
                .catch(function (err) {
                    console.error("Microphone access denied:", err);
                });
        }

        function stopRecording() {
            alert("Attempting to stop recording...");
            if (recorder && recorder.state === "recording") {
                recorder.stop();
                alert("Recording stopped successfully.");
            } else {
                console.error("No active recording to stop.");
            }
        }
    </script>
    <button onclick="startRecording()">Start Recording</button>
    <button onclick="stopRecording()">Stop Recording</button>
""", height=300)

# Listen for audio data from JavaScript
audio_base64 = st.experimental_get_query_params().get("audio_base64")

if audio_base64:
    st.write("Audio data received in Streamlit.")
    save_audio_from_base64(audio_base64)
