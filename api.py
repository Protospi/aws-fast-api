# api.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import openai

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

app = FastAPI()

# Allow CORS (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with allowed origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers
from routes.chat import router as chat_router
from routes.summary import router as summary_router
from routes.title import router as title_router
from routes.transcription import router as transcription_router

# Include routers
app.include_router(chat_router)
app.include_router(summary_router)
app.include_router(title_router)
app.include_router(transcription_router)

# Root endpoint
@app.get("/")
async def index():
    try:
        # Define system prompt
        systemPrompt = "Your default system prompt here."

        # Make a request to the OpenAI Chat Completion API
        completion = openai.ChatCompletion.create(
            model='gpt-4',
            messages=[
                {'role': 'system', 'content': systemPrompt},
                {'role': 'user', 'content': 'Olá'}
            ]
        )

        # Extract the assistant's reply
        assistant_reply = completion.choices[0].message.content

        # Return the reply
        return {"message": assistant_reply}

    except Exception as e:
        # Handle exceptions and return an error message
        raise HTTPException(status_code=500, detail=str(e))

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
