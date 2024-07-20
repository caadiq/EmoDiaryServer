from pydantic import BaseModel

class emotionRequest(BaseModel):
    content: str

def calculate_emotion_level(result_data):
    emtionLevel = 0
    if(result_data["label"] == "LABEL_1"):
        if(float(result_data["score"]) >= 0.9):
            emtionLevel = 5
        elif(float(result_data["score"]) >= 0.8):
            emtionLevel = 4
        else:
            emtionLevel = 3
    else:
        if(float(result_data["score"]) >= 0.9):
            emtionLevel = 1
        elif(float(result_data["score"]) >= 0.8):
            emtionLevel = 2
        else:
            emtionLevel = 3
    return emtionLevel