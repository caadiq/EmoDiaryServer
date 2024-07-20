import io
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from emodiary.word_cloud import get_wordcloud, WordCloudRequest
from transformers import pipeline
from emodiary.emotion import emotionRequest, calculate_emotion_level
from fastapi.responses import JSONResponse


app = FastAPI()


sentiment_model = pipeline(model="WhitePeak/bert-base-cased-Korean-sentiment")

# model_name = 'WhitePeak/bert-base-cased-Korean-sentiment"'
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForSequenceClassification.from_pretrained(model_name)
#
# model.eval()
#
# # 감정 분석 파이프라인 생성하기
# emotion_analysis = pipeline("text-classification", model=model, tokenizer=tokenizer, top_k=None)

# result = emotion_analysis(text)
# print(result)
# print(result)
# print(result)
# print()
#
# result = emotion_analysis(text2)
# print(result)
# print(result)
# print(result)


@app.post("/api/emodiary/wordcloud")
async def wordcloud(request: WordCloudRequest):
    try:
        image_bytes = await get_wordcloud(request.content)
        return StreamingResponse(io.BytesIO(image_bytes), media_type="image/jpeg")
    except Exception as e:
        print(f"Error occurred while getting wordcloud: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/emodiary/sentiment")
async def sentiment(request: emotionRequest):
    try:
        result = sentiment_model(request.content)
        if isinstance(result, list) and len(result) > 0:
            result_data = result[0]
            emotionLevel = calculate_emotion_level(result_data)
            response = {
                "label": result_data["label"],
                "score": result_data["score"],
                "emotion": emotionLevel
            }
            return JSONResponse(content=response)
        else:
            return JSONResponse(content={"error": "No result returned from model."})
    except Exception as e:
        print(f"Error occurred while getting sentiment: {e}")
        raise HTTPException(status_code=400, detail=str(e))
