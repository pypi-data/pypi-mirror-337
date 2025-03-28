import json

from openai import OpenAI
from typing import List
import image_article_comprehension.utils as utils
import os

openai_client = OpenAI()

cache_dir = "/Users/nieqi/Documents/embedding_cache"


class EmbeddingCache:
    def __init__(self, model: str, text: str, embedding: List[float]):
        self.model = model
        self.text = text
        self.embedding = embedding

    @classmethod
    def from_json(cls, data: json):
        return cls(
            model=data['model'],
            text=data['text'],
            embedding=data['embedding']
        )


def get_embedding_cache(model, text):
    text_md5 = utils.md5_str(text)
    cache_path = f"{cache_dir}/{model}/{text_md5}.json"
    if os.path.exists(cache_path):
        cache = json.load(open(cache_path, 'r'))
        if cache.get("text") == text:
            embedding_cache = EmbeddingCache.from_json(cache)
            print(f"{model} , {text} , cache hint")
            return embedding_cache

    return None


def save_embedding_cache(model, text, embedding):
    text_md5 = utils.md5_str(text)
    cache_path = f"{cache_dir}/{model}/{text_md5}.json"
    data = {
        "model": model,
        "text": text,
        "embedding": embedding
    }
    utils.save(data, cache_path)


def get_embedding(text):
    # https://platform.openai.com/docs/pricing
    model = "text-embedding-3-small"
    cache = get_embedding_cache(model, text)

    if cache is not None:
        return cache.embedding

    response = openai_client.embeddings.create(
        model=model,
        input=text,
        encoding_format="float"
    )
    embedding = response.data[0].embedding
    save_embedding_cache(model, text, embedding)

    return embedding


if __name__ == "__main__":
    text = "打工"
    embedding = get_embedding(text)
    print(embedding)
    pass
