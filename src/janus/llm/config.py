from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    api_key: SecretStr = Field(validation_alias="OPENAI_API_KEY", min_length=1)
    model_name: str = Field(
        default="gpt-4",
        validation_alias="OPENAI_MODEL",
        min_length=1,
    )
    base_url: str = Field(
        default="https://api.openai.com/v1",
        validation_alias="OPENAI_API_BASE",
    )
    temperature: float = Field(
        default=0.7,
        validation_alias="OPENAI_TEMPERATURE",
        ge=0,
        le=2,
    )
    max_tokens: int = Field(
        default=1500,
        validation_alias="OPENAI_MAX_TOKENS",
        gt=0,
    )
