#pip install fastapi uvicorn openai tiktoken
import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import tiktoken
from pydantic import BaseModel
from typing import List, Dict, Optional, Union

class APIGateway:
    def __init__(self):
        # Initialize OpenAI client
        self.openai_client = OpenAI(
            api_key=os.getenv('OPENAI_API_KEY')
        )
        
        # Create FastAPI app
        self.app = FastAPI(
            title="OpenAI API Gateway",
            description="Passthrough gateway for OpenAI API with additional features"
        )
        
        # Add CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Add routes
        self.setup_routes()
    
    def setup_routes(self):
        # Chat Completion Route
        @self.app.post("/v1/chat/completions")
        async def create_chat_completion(request: Request):
            try:
                # Parse incoming request
                body = await request.json()
                
                # Validate and forward request to OpenAI
                response = self.openai_client.chat.completions.create(**body)
                
                return response
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        # Embeddings Route
        @self.app.post("/v1/embeddings")
        async def create_embeddings(request: Request):
            try:
                body = await request.json()
                response = self.openai_client.embeddings.create(**body)
                return response
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        # Token Counting Utility Route
        @self.app.post("/utils/token-count")
        async def count_tokens(request: Request):
            try:
                body = await request.json()
                text = body.get('text', '')
                model = body.get('model', 'gpt-3.5-turbo')
                
                # Use tiktoken for accurate token counting
                encoding = tiktoken.encoding_for_model(model)
                token_count = len(encoding.encode(text))
                
                return {"token_count": token_count}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        # Rate Limiting and Usage Tracking Route
        @self.app.post("/v1/usage")
        async def check_usage(request: Request):
            try:
                # Placeholder for usage tracking
                # In a real implementation, you'd track API usage
                return {
                    "total_tokens_used": 0,
                    "requests_remaining": float('inf'),
                    "rate_limit_status": "ok"
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

# Middleware for authentication and logging
class AuthenticationMiddleware:
    async def __call__(self, request: Request, call_next):
        # Optional authentication logic
        api_key = request.headers.get('Authorization')
        if not api_key:
            raise HTTPException(status_code=401, detail="No API key provided")
        
        # Add your authentication validation logic here
        
        response = await call_next(request)
        return response

# Configuration and Startup
def create_api_gateway():
    gateway = APIGateway()
    
    # Optional: Add custom middleware
    gateway.app.middleware('http')(AuthenticationMiddleware())
    
    return gateway

# Deployment helper
def run_gateway():
    import uvicorn
    gateway = create_api_gateway()
    uvicorn.run(gateway.app, host="0.0.0.0", port=8000)

# Example of how to use the gateway
if __name__ == "__main__":
    run_gateway()
