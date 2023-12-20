from components.loader.adapters.base import Adapter
from typing_extensions import Type

from .mcqa import (
    MedMcQaQueryAdapter,
    MedQaQueryAdapter,
)

KNOWN_QUERY_ADAPTERS: list[Type[Adapter]] = [
    MedQaQueryAdapter,
    MedMcQaQueryAdapter,
]
