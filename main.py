import os
import tempfile

import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from emodiary.word_cloud import get_wordcloud

app = FastAPI()
load_dotenv()


class CustomContentClass(BaseModel):
    content: str
    diaryId: int


print(os.getenv("AWS_ACCESS_KEY_ID"))
print(os.getenv("AWS_SECRET_ACCESS_KEY"))
print(os.getenv("REGION_NAME"))
print(os.getenv("BUCKET_NAME"))


@app.post("/api/emodiary/wordcloud")
async def wordcloud(request: CustomContentClass):
    try:
        print(f"Processing word cloud for diaryId: {request.diaryId}")
        image_bytes = await get_wordcloud(request.content)

        # 임시 파일에 이미지 바이트 데이터 저장
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file_name = tmp_file.name
            tmp_file.write(image_bytes)
            tmp_file.flush()

        # 임시 파일을 S3에 업로드
        bucket_name = os.getenv("BUCKET_NAME")
        object_name = f"diary/{request.diaryId}.jpg"
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("REGION_NAME"),
        )
        try:
            s3_client.upload_file(tmp_file_name, bucket_name, object_name,ExtraArgs={'ACL': 'public-read','ContentType': 'image/jpeg'})
        except NoCredentialsError:
            return {"success": False, "url": f"Credentials not available"}
        except FileNotFoundError:
            return {"success": False, "url": f"The file was not found"}

        # 임시 파일 삭제
        os.remove(tmp_file_name)

        return {"success": True, "url": f"https://{bucket_name}.s3.amazonaws.com/{object_name}"}


    except Exception as e:
        print(f"Error occurred while getting wordcloud: {e}")
        raise HTTPException(status_code=400, detail=str(e))
