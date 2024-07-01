import io
from collections import Counter
from pathlib import Path

from konlpy.tag import Okt
from pydantic import BaseModel
from wordcloud import WordCloud


class WordCloudRequest(BaseModel):
    content: str


async def get_wordcloud(content: str):
    okt = Okt()
    sentences_tag = okt.pos(content)

    noun_adj_list = [word for word, tag in sentences_tag if tag in ['Noun', 'Adjective']]

    counts = Counter(noun_adj_list)
    tags = counts.most_common(70)

    font_path = Path(__file__).resolve().parent.parent / 'fonts' / 'nanum_square_neo_bold.ttf'
    wc = WordCloud(font_path=str(font_path), background_color="#FAFAFA", max_font_size=70)
    cloud = wc.generate_from_frequencies(dict(tags))

    image_stream = io.BytesIO()
    cloud.to_image().save(image_stream, format='JPEG')
    image_stream.seek(0)
    return image_stream.read()
