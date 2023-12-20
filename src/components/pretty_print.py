import contextlib
import typing as typ
from copy import copy
from numbers import Number

import datasets
import rich
from omegaconf import DictConfig, OmegaConf, open_dict
from rich.syntax import Syntax
from rich.table import Table
from rich.tree import Tree


def print_as_table(dataset: datasets.Dataset, num_samples: int = 10, seed: int = 42) -> Table:
    """Pretty print a random subset of a dataset in a table form."""
    num_samples = min(num_samples, len(dataset))

    subset = dataset.shuffle(seed=seed).select(range(num_samples))

    table = Table(show_header=True, header_style="bold magenta")
    for column_name in dataset.column_names:
        table.add_column(column_name, style="dim")

    for item, _ in enumerate(subset):
        row_data = [str(subset[item][col]) for col in dataset.column_names]
        table.add_row(*row_data)

    return table


def print_config(
    config: DictConfig,
    fields: typ.Optional[typ.Sequence[str]] = None,
    resolve: bool = True,
    exclude: typ.Optional[typ.Sequence[str]] = None,
) -> None:
    """Prints content of DictConfig using Rich library and its tree structure.

    Args:
        config (DictConfig): Configuration composed by Hydra.
        fields (Sequence[str], optional): Determines which main fields from config will
        be printed and in what order.
        resolve (bool, optional): Whether to resolve reference fields of DictConfig.
        exclude (Sequence[str], optional): Determines which fields from config will be excluded.
        :param exclude:
    """
    style = "dim"
    tree = Tree(":gear: CONFIG", style=style, guide_style=style)
    if exclude is None:
        exclude = []

    fields = fields or list(config.keys())  # type: ignore
    fields = list(filter(lambda x: x not in exclude, fields))  # type: ignore

    with open_dict(config):
        base_config = {}
        for field in copy(fields):
            if isinstance(config.get(field), (bool, str, Number)):
                base_config[field] = config.get(field)
                fields.remove(field)
        config["__root__"] = base_config
    fields = ["__root__"] + fields

    for field in fields:
        branch = tree.add(field, style=style, guide_style=style)

        config_section = config.get(field)
        branch_content = str(config_section)
        if isinstance(config_section, DictConfig):
            with contextlib.suppress(Exception):
                branch_content = OmegaConf.to_yaml(config_section, resolve=resolve)

        branch.add(Syntax(branch_content, "yaml", indent_guides=True, word_wrap=True))

    rich.print(tree)
