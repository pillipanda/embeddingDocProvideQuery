import os
import logging

from fastapi import FastAPI
from pydantic import BaseModel
from functools import lru_cache
from embedding_doc import prepare_paper_and_get_chromaDBClient

from config import Settings


@lru_cache()
def get_settings():
    return Settings()


logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

logger.info('⚠️ please wait until all paper get indexed ⚠️')
db = prepare_paper_and_get_chromaDBClient(get_settings())
logger.info('👏 all paper get indexed, enjoy it now  !🔥')
app = FastAPI()


@app.get("/")
def read_root():
    return "ask your paper/doc/file"


class Query(BaseModel):
    require_chunk_amount: int
    content: str


@app.post("/get_query_about_papers")
async def get_query_about_chunks(query: Query):
    docs = db.similarity_search(
        query=query.content, k=query.require_chunk_amount)

    ret = []
    for j in docs:
        file_name = os.path.basename(j.metadata['source'])
        page = j.metadata.get('page')
        content = j.page_content.replace(
            '\n', ' ').replace('<', '[').replace('>', ']')

        ret.append({
            'file': f'{file_name}-page {page}' if page else f'{file_name}',
            'paper':  content
        })

    return ret
