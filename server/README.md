# Chatbot Backend Server

FastAPI server that provides a chat endpoint using Grok API.

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set up environment variables:

```bash
cp .env.example .env
```

Then edit `.env` and add your Grok API key:

```
GROK_API_KEY=your_actual_api_key_here
```

You can get a Grok API key from https://console.x.ai/

3. Load environment variables (optional, but recommended):

```bash
# Install python-dotenv if not already installed
pip install python-dotenv
```

Then update `main.py` to load from .env file:

```python
from dotenv import load_dotenv
load_dotenv()
```

## HTTPS Setup

The server uses HTTPS by default. First, generate self-signed SSL certificates:

### Option 1: Using the shell script (Unix/macOS/Linux)

```bash
chmod +x generate_cert.sh
./generate_cert.sh
```

### Option 2: Using Python script (Cross-platform)

```bash
python generate_cert.py
```

This will create SSL certificates in the `certs/` directory. The server will automatically use HTTPS if certificates are found, otherwise it will fall back to HTTP.

## Running the Server

### Option 1: Using uvicorn directly

```bash
# With HTTPS (if certificates exist)
uvicorn main:app --host 0.0.0.0 --port 4000 --ssl-keyfile certs/localhost-key.pem --ssl-certfile certs/localhost-cert.pem

# Without HTTPS
uvicorn main:app --host 0.0.0.0 --port 4000
```

### Option 2: Using Python

```bash
python main.py
```

The server will run on `https://localhost:4000` (or `http://localhost:4000` if certificates are not found)

## API Endpoints

### GET /

Health check endpoint

### POST /chat

Chat endpoint that forwards messages to Grok API

**Request:**

```json
{
  "message": "Hello, how are you?"
}
```

**Response:**

```json
{
  "response": "I'm doing well, thank you for asking!"
}
```

## Testing

You can test the endpoint using curl:

```bash
# With HTTPS (skip certificate verification for self-signed certs)
curl -k -X POST https://localhost:4000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!"}'

# With HTTP (if certificates not found)
curl -X POST http://localhost:4000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!"}'
```

Or use the chatbot client in the `chatbot-software` folder.
