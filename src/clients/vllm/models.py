import pydantic


class VllmChatRequest(pydantic.BaseModel):
    """Vllm request."""

    prompt: str = pydantic.Field(..., description="The prompt to send to the model.")
    temperature: float | None = pydantic.Field(default=0.0, description="temperature")
    top_p: float | None = pydantic.Field(default=1.0, description="top p")
    n: int | None = pydantic.Field(default=1, description="number of completions")
    stop: str | None = pydantic.Field(default=None, description="stop token")
    max_tokens: int | None = pydantic.Field(default=512, description="max tokens")
    presence_penalty: float | None = pydantic.Field(default=0.0, description="presence penalty")
    frequency_penalty: float | None = pydantic.Field(default=0.0, description="frequency penalty")
