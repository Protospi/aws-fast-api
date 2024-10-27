# routes/transcription.py

from fastapi import APIRouter, HTTPException, UploadFile, File
from werkzeug.utils import secure_filename
import os
import openai

router = APIRouter()

client = openai.OpenAI()

@router.post("/transcription")
async def transcription(file: UploadFile = File(...)):
    try:
        # Ensure the file is provided
        if not file:
            raise HTTPException(status_code=400, detail="No file uploaded")

        # Save the file temporarily
        filename = secure_filename(file.filename)
        temp_path = os.path.join('temp', filename)
        os.makedirs('temp', exist_ok=True)

        # Read file content and save
        with open(temp_path, 'wb') as f:
            content = await file.read()
            f.write(content)

        # Open the file and send it to OpenAI
        with open(temp_path, 'rb') as audio_file:
            transcription = client.audio.transcriptions.create(
                model='whisper-1',
                file=audio_file
            )

        # Clean up the temporary file
        # os.remove(temp_path)
        print(transcription,flush=True)

        # Return the transcription
        return {'transcription': transcription}

    except Exception as e:
        # Handle exceptions and return an error message
        raise HTTPException(status_code=500, detail=str(e))
