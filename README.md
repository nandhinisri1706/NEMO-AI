# NEMO AI – Personal AI Assistant
<img width="754" height="620" alt="image" src="https://github.com/user-attachments/assets/7130584b-2b9b-491d-8a84-3c1e3a091a5b" />


NEMO AI is a locally running AI-powered chatbot built using Python, Streamlit, and Ollama. It provides an interactive chat experience with conversation history, theme switching, and intelligent AI responses.

The application uses a locally hosted Gemma 3 1B model through Ollama while presenting NEMO AI as its own assistant identity.

## Features

- **AI Chat:** Interact with NEMO AI and receive real-time responses.
- **Multiple Conversations:** Create and manage separate chat sessions.
- **Chat History:** Automatically saves conversations locally.
- **Dark and Light Themes:** Switch between themes using the top-right theme toggle.
- **Prompt Suggestions:** Choose predefined suggestions to start conversations.
- **Streaming Responses:** View AI responses as they are generated.
- **Persistent Storage:** Stores chat history and theme preferences locally.
- **Local AI Processing:** Runs the AI model through Ollama.
<img width="1269" height="587" alt="image" src="https://github.com/user-attachments/assets/54533a30-b961-4364-a467-5bec91227df3" />

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | User interface |
| Ollama | Local AI model execution |
| Gemma 3 1B | Language model |
| JSON | Chat history and settings storage |

## Project Structure

```text
NEMO-AI/
│
├── app.py
├── requirements.txt
├── chat_history.json
├── nemo_settings.json
└── README.md
```

Note: The JSON files are automatically created when the application runs.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_REPOSITORY_URL
```

### 2. Navigate to the Project Directory

```bash
cd NEMO-AI
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Ollama

Download and install Ollama:

https://ollama.com/

### 5. Download the AI Model

```bash
ollama pull gemma3:1b
```

### 6. Run the Application

```bash
python -m streamlit run app.py
```

The application will open in your browser at:

```text
http://localhost:8501
```

## Requirements

- Python
- Streamlit
- Ollama
- Gemma 3 1B model

## Configuration

The application uses the following default model:

```python
MODEL = "gemma3:1b"
```

Chat conversations are stored in:

```text
chat_history.json
```

Theme preferences are stored in:

```text
nemo_settings.json
```

## Future Enhancements

- User authentication and account management
- Advanced conversational memory
- Chat export functionality
- File upload and document analysis
- Voice input and output
- Custom AI model selection
- Improved response generation

## Author

**Nandhini Sri**

## License

This project is developed for educational and personal development purposes.
