import io
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from gtts import gTTS

app = FastAPI()

class InputSentence(BaseModel):
    sentence: str
    language: str = "ko"

@app.post("/generate")
async def generate_speech(input: InputSentence):
    try:
        audio_buffer = io.BytesIO()
        tts = gTTS(text=input.sentence, lang=input.language)
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)

        return StreamingResponse(audio_buffer, media_type="audio/mp3")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7773)