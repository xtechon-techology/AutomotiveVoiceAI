import streamlit as st
import base64


# Function to save audio from Base64
def save_audio_from_base64(base64_audio):
    try:
        st.write("Decoding and saving audio...")
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


# Title
st.title("Microphone Audio Recorder")

# Placeholder to display received Base64 data
audio_base64 = st.text_area("Received Base64 Audio Data (Debugging)", "")

# Display JavaScript Recorder
st.components.v1.html("""
    <script>
        let recorder, audioChunks;

        // Start Recording
        function startRecording() {
            alert("Starting recording...");
            navigator.mediaDevices.getUserMedia({ audio: true })
                .then(function (stream) {
                    recorder = new MediaRecorder(stream);
                    audioChunks = [];

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
                    alert("Recording started.");
                })
                .catch(function (err) {
                    console.error("Microphone access denied:", err);
                    alert("Please allow microphone access to use this feature.");
                });
        }

        // Stop Recording
        function stopRecording() {
            alert("Stopping recording...");
            if (recorder && recorder.state === "recording") {
                recorder.stop();
                alert("Recording stopped successfully.");
            } else {
                console.error("No active recording to stop.");
                alert("No active recording to stop.");
            }
        }

        // Listen for messages and forward data to Streamlit
        window.addEventListener("message", function (event) {
            if (event.data.type === "audio") {
                alert("Audio data received in Streamlit.");
                const textArea = parent.document.querySelector('textarea');
                textArea.value = event.data.data;
                textArea.dispatchEvent(new Event('input', { bubbles: true }));
            }
        });

        // Add buttons
        document.write(`
            <button onclick="startRecording()">Start Recording</button>
            <button onclick="stopRecording()">Stop Recording</button>
        `);
    </script>
""", height=300)

# Decode and save the audio if received
if audio_base64:
    save_audio_from_base64(audio_base64)
