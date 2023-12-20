import json
import typing as typ
from pathlib import Path

import jinja2
import requests
from clients.vllm.models import VllmChatRequest
from joblib import Memory
from transformers import AutoTokenizer


def query_vllm(prompt: str, url: str, **kwargs: typ.Any) -> str:
    """Call the generate function.."""
    m = VllmChatRequest(prompt=prompt, **kwargs)
    response = requests.post(url=f"{url}/generate", json=m.model_dump(exclude_none=True), timeout=10)
    response.raise_for_status()
    data = json.loads(response.content)
    return data["text"][0].replace(prompt, "").strip()


class VllmInterface:
    """Generic interface for vLLM supported models."""

    def __init__(
        self,
        name: str,
        endpoint: str,
        messages: list[dict[str, str]],
        cache_dir: str,
        reset_cache: bool = False,
        params: dict[str, typ.Any] = {},
    ) -> None:
        """Initialize client."""
        self.template = AutoTokenizer.from_pretrained(name)
        self.messages = messages
        self.params = params
        self.endpoint = endpoint
        self.url = f"http://{endpoint}/generate"
        cache_dir_abs = Path(cache_dir, name, "memory").resolve()
        memory = Memory(cache_dir_abs, verbose=0)
        if reset_cache:
            memory.clear(warn=False)
        self.fn = memory.cache(query_vllm)

    def __call__(self, batch: dict[str, typ.Any], **kwargs: typ.Any):
        """Generate a response with a vllm served model."""
        messages = self.format_messages(**batch)
        if self.template.chat_template is None:  # if foundation model
            prompt: str = "\n".join([msg["content"] for msg in messages])
        else:
            prompt: str = self.template.apply_chat_template(
                conversation=messages,
                tokenize=False,
                add_generation_prompt=True,  # type: ignore
            )
        return self.fn(prompt=prompt, url=self.endpoint, **self.params)  # type: ignore

    def format_messages(self, **input_variables: dict[str, typ.Any]) -> list[dict[str, str]]:
        """Render input variables based on prompt."""
        messages = []
        for msg in self.messages:
            role = msg["role"]
            content = msg["content"]
            template = jinja2.Template(content)
            content = template.render(**input_variables)
            messages.append({"role": role, "content": content})
        return messages
