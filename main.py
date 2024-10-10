import io
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from TTS.api import TTS

app = FastAPI()

tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")

class InputSentence(BaseModel):
    sentence: str
    speaker: str
    language: str


@app.post("/generate")
async def generate_speech(input: InputSentence):
    try:
        audio_buffer = io.BytesIO()
        tts.tts_to_file(text=input.sentence, speaker=input.speaker, language=input.language, file_path=audio_buffer)
        audio_buffer.seek(0)

        return StreamingResponse(audio_buffer, media_type="audio/wav")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7773)