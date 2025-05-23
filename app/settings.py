from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(override=True)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    # Playground Security
    PLAYGROUND_USERNAME: str = "playground"
    PLAYGROUND_PASSWORD: str = ""

    # Model to use prefixed by provider, i.e. "openai:gpt-4o"
    MODEL_NAME: str = ""
    IMAGE_MODEL_NAME: str = ""
    FORMAT_MODEL_NAME: str = ""

    # Non-Azure OpenAI
    OPENAI_API_KEY: str = ""

    # Azure OpenAI
    OPENAI_API_VERSION: str = ""
    AZURE_OPENAI_ENDPOINT: str = ""
    AZURE_OPENAI_API_KEY: str = ""

    # Ollama settings
    OLLAMA_BASIC_AUTH_USERNAME: str = ""
    OLLAMA_BASIC_AUTH_PASSWORD: str = ""
    OLLAMA_HOST: str = ""

    LANGFUSE_PUBLIC_KEY: str = ""
    LANGFUSE_SECRET_KEY: str = ""
    LANGFUSE_HOST: str = ""

    @property
    def langfuse_enabled(self):
        return bool(
            self.LANGFUSE_PUBLIC_KEY
            and self.LANGFUSE_SECRET_KEY
            and self.LANGFUSE_HOST
        )


settings = Settings()
