import os
import pathlib
import re
from pathlib import Path

import pydantic

DEFAULT_CACHE_DIR = str(pathlib.Path(os.environ.get("DEFAULT_CACHE_DIR", "~/.cache/medical-reasoning")).expanduser())


class ModelConfig(pydantic.BaseModel):
    """Class representing a model."""

    name: str = pydantic.Field(..., description="The name of the model.")
    endpoint: str = pydantic.Field(default="localhost:8080", description="The endpoint of the model.")
    cache_dir: str = pydantic.Field(default=DEFAULT_CACHE_DIR, description="The directory to save model responses")
    reset_cache: bool = pydantic.Field(default=False, description="Whether to reset the cache of the model.")

    @pydantic.field_validator("cache_dir", mode="after")
    def validate_cache_dir(cls, v: str) -> str:
        """Validate the cache directory."""
        return str(Path(v).resolve())

    @pydantic.field_validator("endpoint")
    def validate_endpoint(cls, v: str) -> str:
        """Validate the endpoint."""
        if not re.match(r"^[a-zA-Z0-9.-]+:\d+$", v):
            raise ValueError("Endpoint must be in the format 'host:port'")
        return v
