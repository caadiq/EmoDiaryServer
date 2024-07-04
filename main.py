import io
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from emodiary.word_cloud import get_wordcloud, WordCloudRequest

app = FastAPI()


@app.post("/api/emodiary/wordcloud")
async def wordcloud(request: WordCloudRequest):
    try:
        image_bytes = await get_wordcloud(request.content)
        return StreamingResponse(io.BytesIO(image_bytes), media_type="image/jpeg")
    except Exception as e:
        print(f"Error occurred while getting wordcloud: {e}")
        raise HTTPException(status_code=400, detail=str(e))
