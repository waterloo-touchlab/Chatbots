# Mansplain Study Repository

This repository supports a research study examining gender dynamics and perceived tone in chatbot interactions. The study includes three different chatbot conditions—**Compassionate**, **Default**, and **Mansplain**—each implemented as a standalone Gradio app. 

A transcription tool is also included to assist with converting participant recordings into text using Whisper and Streamlit.

---

## Overview

- **Chatbot Conditions**: Each folder under study/ contains one condition of the chatbot experiment, implemented using [Gradio](https://www.gradio.app/). Each app includes logic for interactive conversations and stores chat logs to a local folder named data/.

- **Transcription Tool**: A separate tool is included to assist researchers in transcribing audio responses from participants. This tool is built with [Streamlit](https://streamlit.io/) and uses [OpenAI Whisper](https://github.com/openai/whisper) for transcription.

---


Running the Apps

Chatbot Conditions
In each app.py file, set your OpenAI API key:
openai.api_key = "your-openai-api-key"

Each chatbot condition is a separate Gradio app. To run one:

Replace mansplain with default or compassionate to run the others.

Conversation logs are saved under the respective data/ folder as CSVs

Logs are tied to participants via a query parameter (?id=participant123)



Transcription Tool
streamlit run transcribe.py
This launches a web-based UI for uploading participant audio and generating transcripts using Whisper.

📄 Conversation Logging
Each app logs conversations as CSV files named after the user ID (e.g., participant123.csv)

Logs include role-labeled entries (system, user, assistant) and timestamps

Files are stored in data/ inside the corresponding condition folder

