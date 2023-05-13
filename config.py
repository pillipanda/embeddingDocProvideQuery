from pydantic import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str
    embedding_chunk_size: int = 4000
    embedding_chunk_overlap: int = 500

    class Config:
        env_file = ".env"


settings = Settings()
