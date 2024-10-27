# routes/summary.py

from fastapi import APIRouter, HTTPException
from models import ChatRequest, Message
import openai
from dotenv import load_dotenv

client = openai.OpenAI()
load_dotenv()

router = APIRouter()

@router.post("/summary")
async def summarize(chat_request: ChatRequest):
    try:
        # Define system prompt
        systemPrompt = """
            Resuma a conversa entre um terapeuta e um paciente. 
            Ofereça alguns conselhos úteis ao paciente.
        """.encode('utf-8')

        messages = chat_request.messages

        # Filter out system messages
        messages = [msg for msg in messages if msg.role != 'system']

        # Insert the system prompt as the first message
        messages.insert(0, Message(role='system', content=systemPrompt))

        # Convert messages to the format expected by OpenAI API
        openai_messages = [{'role': msg.role, 'content': msg.content} for msg in messages]

        # Make a request to the OpenAI Chat Completion API
        completion = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=openai_messages
        )

        summary = completion.choices[0].message.content

        # Return the summary
        return {'summary': summary}

    except Exception as e:
        # Handle exceptions and return an error message
        raise HTTPException(status_code=500, detail=str(e))
