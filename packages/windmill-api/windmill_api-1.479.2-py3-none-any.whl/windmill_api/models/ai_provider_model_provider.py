from enum import Enum


class AIProviderModelProvider(str, Enum):
    ANTHROPIC = "anthropic"
    CUSTOMAI = "customai"
    DEEPSEEK = "deepseek"
    GOOGLEAI = "googleai"
    GROQ = "groq"
    MISTRAL = "mistral"
    OPENAI = "openai"
    OPENROUTER = "openrouter"
    TOGETHERAI = "togetherai"

    def __str__(self) -> str:
        return str(self.value)
