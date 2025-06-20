import streamlit as st
import os
import csv
import tempfile
from datetime import datetime
from audio_recorder_streamlit import audio_recorder 
from openai import OpenAI 


# --- Config ---

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set up a folder to save logs
log_folder = "conversation_logs"
os.makedirs(log_folder, exist_ok=True)

# Streamlit UI 
st.set_page_config(page_title="Transcription Service")
st.title("🎙️ Audio Transcriber")

# Session state initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_log" not in st.session_state:
    st.session_state.conversation_log = []

if "session_id" not in st.session_state:
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.session_state.session_id = f"session_{now}"

# Save conversation to CSV
def save_conversation_to_csv(conversation_log, csv_name):
    file_path = os.path.join(log_folder, csv_name)
    file_exists = os.path.exists(file_path)
    with open(file_path, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["role", "message"])
        for msg in conversation_log:
            writer.writerow([msg["role"], msg["message"]])

# Log and save a message
def log_message(role, content):
    st.session_state.messages.append({"role": role, "content": content})
    st.session_state.conversation_log.append({"role": role, "message": content})
    save_conversation_to_csv(st.session_state.conversation_log, f"{st.session_state.session_id}.csv")

# Record and transcribe audio
audio = audio_recorder("Click to record", "Recording...")
if audio:
    st.audio(audio, format="audio/wav")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
        temp_audio_file.write(audio)
        temp_path = temp_audio_file.name

    with st.spinner("Transcribing..."):
        with open(temp_path, "rb") as f:
            transcription = client.audio.transcriptions.create(model="whisper-1", file=f)
        user_text = transcription.text
        st.markdown("### You said:")
        st.success(user_text)

    log_message("user", user_text)

# Display conversation history
if len(st.session_state.messages) > 1:
    st.markdown("---")
    st.markdown("## Conversation History")
    for msg in st.session_state.messages[1:]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
