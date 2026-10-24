# Medical Chatbot

A health-focused educational chatbot built with FastAPI, LangGraph, OpenRouter, Pinecone, and Tavily. It combines a curated medical knowledge base with live web research to answer user questions with source-backed responses, image understanding, and conversational memory.

## Overview

This project is designed for medical education and research support, not diagnosis or emergency care. The assistant:

- searches a local PDF-backed medical knowledge base stored in Pinecone
- uses the web when a question is current, missing context, or low-confidence
- analyzes uploaded medical images with a vision-capable model
- supports voice transcription and speech synthesis APIs
- keeps a per-conversation thread for follow-up questions
- exposes a browser UI and REST API endpoints

## Key Features

- PDF ingestion and semantic retrieval for medical reference content
- RAG pipeline with Pinecone vector search and OpenRouter LLMs
- Web search fallback for current guidance using Tavily
- Image input analysis for visible medical features only
- Voice input/output support via OpenRouter transcription and TTS endpoints
- Persistent memory using SQLite checkpointers for conversation continuity
- FastAPI server with a simple frontend in the browser

## Project Structure

- `app/main.py` — FastAPI application and API routes
- `app/agent.py` — LangGraph reasoning flow and routing logic
- `app/knowledge.py` — Pinecone index creation and similarity search
- `app/config.py` — environment configuration and settings
- `ingest.py` — PDF chunking and embedding ingestion
- `templates/index.html` — UI entry point
- `static/` — frontend assets and browser logic
- `data/` — source PDF files used for indexing

## Requirements

- Python 3.11+
- OpenRouter API key
- Pinecone API key
- Optional: Tavily API key for live web background search
- A source PDF in `data/` for ingestion

## Installation

### Recommended: uv

```bash
uv venv --python 3.11
.venv\Scripts\activate
uv pip install -r requirements.txt
```

### Alternative: venv + pip

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root with the required values:

```env
OPENROUTER_API_KEY=your_openrouter_key
PINECONE_API_KEY=your_pinecone_key
TAVILY_API_KEY=your_tavily_key

# Optional overrides
PINECONE_INDEX=medical-chatbot
OPENAI_ROUTER_CHAT_MODEL=openai/gpt-4.1-mini
OPENAI_ROUTER_EMBED_MODEL=openai/text-embedding-3-small
OPENAI_ROUTER_VISION_MODEL=openai/gpt-4o-mini
API_TOKEN=
ALLOWED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
```

Notes:

- `OPENROUTER_API_KEY` is the primary setting.
- `OPENAI_ROUTER_API_KEY` and `OPENAI_API_KEY` are also accepted for compatibility with older environments.
- If you do not provide `TAVILY_API_KEY`, the app still works with the PDF knowledge base, but web research fallback is disabled.
- The default Pinecone index name is `medical-chatbot`.

## Ingesting Medical Content

The project uses a PDF as the primary source document. The ingestion script chunks the text, embeds it, and stores the vectors in Pinecone.

```bash
python ingest.py --pdf data/Medical_book.pdf
```

Important: the source file name in the repository is `data/Medical_book.pdf` (capital `M`). If the file is renamed, pass the correct path to the script.

## Running the App

Start the FastAPI server:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Then open:

- http://127.0.0.1:8000

The browser UI includes:

- chat input
- image upload or camera capture
- microphone input
- read-aloud support for generated answers

## API Endpoints

### Health check

```bash
curl http://127.0.0.1:8000/api/health
```

### Chat API

```bash
curl -X POST http://127.0.0.1:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What symptoms should I monitor for a possible respiratory infection?",
    "history": []
  }'
```

### Image analysis

The API accepts a Base64 data URL in `image_data` when sending chat requests.

### Transcription and speech synthesis

If `API_TOKEN` is configured in `.env`, include the same Authorization header your deployment expects when calling the protected routes.

```bash
curl -X POST "http://127.0.0.1:8000/api/transcribe" \
  -H "Authorization: <your-token-header>" \
  -F "file=@voice.webm"

curl -X POST http://127.0.0.1:8000/api/speak \
  -H "Content-Type: application/json" \
  -H "Authorization: <your-token-header>" \
  -d '{"text":"This is a test of the medical assistant voice output."}'
```

## Usage Examples

### Ask a question

1. Open the app in the browser.
2. Type a question such as: "What are the common warning signs of dehydration?"
3. The system retrieves relevant PDF excerpts and may use web links if the query is current or low-confidence.

### Upload an image

1. Click the image button or use the camera.
2. Attach a JPEG, PNG, or WebP image under 5 MB.
3. The assistant describes only visible, objective, medical-relevant features without diagnosing.

### Continue a conversation

The app stores conversation state using a `X-Conversation-ID` header or generates one automatically for the current session thread.

## Important Safety Notes

- This application is for educational purposes and should not replace professional clinical judgment.
- Do not use it for emergency decision-making.
- For severe symptoms such as chest pain, stroke symptoms, severe shortness of breath, severe bleeding, or altered consciousness, seek emergency medical care immediately.
- The uploaded PDF is historical and should be treated as educational context, not current clinical policy.

## Troubleshooting

- If you get a Pinecone error, ensure the index exists and your `PINECONE_API_KEY` is valid.
- If ingestion fails, confirm that the file exists and the path is correct.
- If the app reports missing API keys, verify the values in `.env` and restart the server.
- If the browser UI does not load, make sure the app is running on the expected port and `ALLOWED_ORIGINS` matches your app origin.

## License

This project is intended for educational and internal research use. Review the repository's licensing terms before production deployment or redistribution.

