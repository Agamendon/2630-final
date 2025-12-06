"""
FastAPI server for chatbot backend
Uses Grok API for generating responses
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Chatbot Backend Server")

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Grok API configuration
GROK_API_URL = "https://api.x.ai/v1/chat/completions"
GROK_API_KEY = os.getenv("GROK_API_KEY")


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "Chatbot backend server is running"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint that forwards messages to Grok API
    """
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    if not GROK_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="GROK_API_KEY environment variable is not set"
        )
    
    try:
        # Call Grok API
        headers = {
            "Authorization": f"Bearer {GROK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": request.message
                }
            ],
            "model": "grok-beta",  # or "grok-2" depending on available models
            "stream": False
        }
        
        response = requests.post(
            GROK_API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Grok API error: {response.text}"
            )
        
        data = response.json()
        
        # Extract the response from Grok API
        # Grok API returns choices[0].message.content
        if "choices" in data and len(data["choices"]) > 0:
            grok_response = data["choices"][0]["message"]["content"]
            return ChatResponse(response=grok_response)
        else:
            raise HTTPException(
                status_code=500,
                detail="Unexpected response format from Grok API"
            )
            
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to communicate with Grok API: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    import ssl
    
    # SSL certificate paths
    cert_path = "certs/localhost-cert.pem"
    key_path = "certs/localhost-key.pem"
    
    # Check if certificates exist
    import os
    if os.path.exists(cert_path) and os.path.exists(key_path):
        # Create SSL context for HTTPS
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(cert_path, key_path)
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=4000,
            ssl_keyfile=key_path,
            ssl_certfile=cert_path
        )
    else:
        print("Warning: SSL certificates not found!")
        print("Run './generate_cert.sh' to generate self-signed certificates.")
        print("Starting server without HTTPS...")
        uvicorn.run(app, host="0.0.0.0", port=4000)

