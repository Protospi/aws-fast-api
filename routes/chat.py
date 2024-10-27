# routes/chat.py

from fastapi import APIRouter, HTTPException
from models import ChatRequest, Message
import openai
from dotenv import load_dotenv

client = openai.OpenAI()
load_dotenv()

router = APIRouter()

@router.post("/chat")
async def chat(chat_request: ChatRequest):
    try:
        # Define system prompt
        systemPrompt = """
            Você vai atuar como um psicólogo, e o primeiro passo é conhecer seu cliente. 
            Pergunte ao usuário seu nome e qual estilo de análise ele prefere: 
            1. Freudiano: Foca no inconsciente e na interpretação dos sonhos, explorando como experiências passadas moldam o comportamento atual. 
            2. Lacaniano: Enfatiza a linguagem e a relação com o outro, explorando como o desejo e a falta influenciam a psique. 
            3. Junguiano: Concentra-se na individuação e nos arquétipos, buscando compreender o eu através da mitologia e do simbolismo. 
            Depois que o usuário escolher um estilo de análise, inicie a conversa simulando uma sessão de terapia com Freud, Lacan ou Jung, 
            fazendo perguntas abertas que incentivem a reflexão e a autoexploração. 
            Utilize uma abordagem educada e descontraída, mantendo as mensagens curtas e acessíveis. 
            Conduza o diálogo como um psicólogo experiente que está lá para ajudar o cliente a entender melhor a si mesmo.
        """.encode('utf-8')

        messages = chat_request.messages
        # print(messages,flush=True)

        # Ensure the system prompt is included as the first message
        if not any(msg.role == 'system' for msg in messages):
            messages.insert(0, Message(role='system', content=systemPrompt))

        # Convert messages to the format expected by OpenAI API
        openai_messages = [{'role': msg.role, 'content': msg.content} for msg in messages]
        # print(openai_messages,flush=True)

        # Make a request to the OpenAI Chat Completion API
        completion = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=openai_messages
        )

        # Extract the assistant's reply
        assistant_reply = completion.choices[0].message.content
        
        # Append the assistant's reply to the messages
        messages.append(Message(role='assistant', content=assistant_reply))
        # print(messages,flush=True)

        # Return the assistant's reply and updated messages
        return {'messages': [msg.model_dump() for msg in messages]}

    except Exception as e:
        # Handle exceptions and return an error message
        raise HTTPException(status_code=500, detail=str(e))
