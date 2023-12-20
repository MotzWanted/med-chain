import random
import typing as typ

import datasets
from components.loader.adapters.base import Adapter
from rich.console import Console

from .adapters import KNOWN_QUERY_ADAPTERS
from .utils import dict_to_rich_table, get_first_row

T = typ.TypeVar("T")

D = typ.TypeVar("D", bound=typ.Union[datasets.Dataset, datasets.DatasetDict])


def find_adapter(row: dict[str, typ.Any], verbose: bool = False) -> typ.Type[Adapter]:
    """Find an adapter for a row."""
    console = Console()
    for v in KNOWN_QUERY_ADAPTERS:
        if v.can_handle(row):
            translated_row = v.translate_row(row)
            if verbose:
                console.print(dict_to_rich_table(row, "Input data"))
                console.print(dict_to_rich_table(translated_row.model_dump(), "Output data"))
            return v
    raise ValueError(f"Could not find an adapter for row: `{row}`")


def load_dataset(
    name_or_path: str,
    split: str,
    subset: str | None = None,
    num_proc: int = 4,
    num_samples: int | None = None,
    seed: int | None = 42,
    verbose: bool = False,
    **kws: typ.Any,
) -> datasets.Dataset:
    """Load a multiple choice huggingface dataset."""
    data = datasets.load_dataset(name_or_path, subset, split=split, **kws)
    if isinstance(data, (datasets.DatasetDict, datasets.IterableDataset, datasets.IterableDatasetDict)):
        raise NotImplementedError(f"`{type(data)}` not supported.")

    row = get_first_row(data)
    adapter = find_adapter(row, verbose=verbose)

    if num_samples:
        random.seed(seed)
        indices = random.sample(range(len(data)), num_samples)
        data = data.select(indices)
    return adapter.translate(data, map_kwargs={"num_proc": num_proc})
