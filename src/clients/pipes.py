import hashlib
import json
import typing as typ
from pathlib import Path

from clients.vllm.client import VllmInterface


class ParallelResponseGenerator:
    """A HuggingFace approach to parallelize the querying of a LLM."""

    def __init__(
        self,
        client: VllmInterface,
    ) -> None:
        """Initialize the class."""
        self.client = client

    def __getstate__(self) -> object:
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state: dict[str, typ.Any]) -> None:
        self.__dict__.update(state)

    def __call__(self, batch: dict[str, list[typ.Any]]) -> dict[str, list[typ.Any]]:
        """Call the client in parallel."""
        batch_length = len(next(iter(batch.values())))
        responses = []
        for i in range(batch_length):
            sample = {key: batch[key][i] for key in batch}
            responses.append(self.client(sample))
        return {**batch, "completion": responses}


class DumpReponsesToJson:
    """A pipeline to dump responses to json."""

    def __init__(self, save_dir: str) -> None:
        self.save_dir = Path(
            save_dir,
            "responses",
        ).resolve()

    def __getstate__(self) -> object:
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state: dict[str, typ.Any]) -> None:
        self.__dict__.update(state)

    def __call__(self, batch: dict[str, list[typ.Any]], **kws: typ.Any) -> dict[str, list[typ.Any]]:
        """Dump each sample in a batch to a json file."""
        batch_length = len(next(iter(batch.values())))
        for i in range(batch_length):
            sample = {key: batch[key][i] for key in batch}
            self.dump_to_json(sample)
        return batch

    def dump_to_json(self, sample: dict[str, typ.Any]) -> None:
        """Dump a sample to a json file."""
        sample_string = json.dumps(sample, sort_keys=True)
        file_name = hashlib.sha256(sample_string.encode()).hexdigest()
        path_to_file = Path(self.save_dir, f"{file_name}.json")

        path_to_file.parent.mkdir(parents=True, exist_ok=True)
        with open(path_to_file, "w") as file:
            json.dump(sample, file)
