from pydantic import BaseModel

class emotionRequest(BaseModel):
    content: str

def calculate_emotion_level(result_data):
    emtionLevel = " "
    if(result_data["label"] == "LABEL_1"):
        if(float(result_data["score"]) >= 0.9):
            emtionLevel = "Very Good"
        elif(float(result_data["score"]) >= 0.8):
            emtionLevel = "Good"
        else:
            emtionLevel = "Neutral"
    else:
        if(float(result_data["score"]) >= 0.9):
            emtionLevel = "Very Bad"
        elif(float(result_data["score"]) >= 0.8):
            emtionLevel = "Bad"
        else:
            emtionLevel = "Neutral"
    return emtionLevel