from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

from janus.llm.config import LLMConfig


class LLMClient:
    def __init__(self, config: LLMConfig | None = None) -> None:
        self.config = config or LLMConfig()
        self.client = OpenAI(
            api_key=self.config.api_key.get_secret_value(),
            base_url=self.config.base_url,
        )

    def chat(self, messages: list[ChatCompletionMessageParam]) -> str:
        response = self.client.chat.completions.create(
            model=self.config.model_name,
            messages=messages,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
        )

        if not response.choices:
            raise RuntimeError("The LLM provider returned no completion choices.")

        content = response.choices[0].message.content
        if content is None:
            raise RuntimeError("The LLM provider returned a completion without text.")

        return content