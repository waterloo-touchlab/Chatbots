# 🧠 Mansplain Study Repository

This repository supports a research study examining **gender dynamics** and **perceived tone** in chatbot interactions. The study includes three different chatbot conditions:

- **Compassionate**
- **Default**
- **Mansplain**

Each condition is implemented as a standalone [Gradio](https://www.gradio.app/) app.

A separate **transcription tool** is also included for converting participant recordings into text using [Whisper](https://github.com/openai/whisper) and [Streamlit](https://streamlit.io/).

---

## 📁 Overview

### Chatbot Conditions

- Located under the `study/` directory.
- Each folder (`mansplain/`, `default/`, `compassionate/`) includes an `app.py` file implementing a standalone Gradio app.
- Conversations are logged as `.csv` files in a local `data/` folder inside each condition's directory.

### 📝 Transcription Tool

- A separate tool (`transcribe.py`) is included to transcribe participant audio.
- Built using **Streamlit** and integrates **OpenAI Whisper** for automatic speech-to-text.

---

## ⚙️ Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Install required libraries:
  ```bash
  pip install openai gradio streamlit
  pip install git+https://github.com/openai/whisper.git

## Running the Apps

### Chatbot Conditions

**Set your OpenAI API key** in the `condition.py` files:


openai.api_key = "your-openai-api-key"

## Deployment with NGINX and systemd

To run the apps as background services and serve them using NGINX:

### 🖥 Restarting All Services

Use the following commands to restart the services:

```bash
  sudo systemctl restart nginx
  sudo systemctl restart study-condition1
  sudo systemctl restart study-condition2
  sudo systemctl restart study-condition3
