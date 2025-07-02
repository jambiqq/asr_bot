from fastapi import FastAPI, UploadFile, File
from app.asr import transcribe_audio

app = FastAPI()

@app.post("/transcribe/")
async def transcribe(file: UploadFile = File(...)):
    text = transcribe_audio(file.file)
    return {"transcription": text}

#uvicorn main:app --reload
