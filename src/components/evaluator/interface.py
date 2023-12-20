import typing as typ

import datasets
import evaluate
import loguru
from clients.pipes import DumpReponsesToJson


def compute_metrics(
    dataset: datasets.Dataset,
    metrics: list[str],
    prediction_field: str,
    reference_field: str | None = None,
) -> dict[str, float]:
    """Evaluate a metric and log the result."""
    evaluators = [evaluate.load(metric) for metric in metrics]
    results = {}
    for evaluator in evaluators:
        computed_metric = evaluator.compute(
            predictions=dataset[prediction_field], references=dataset[reference_field] if reference_field else None
        )
        if computed_metric:
            results.update(computed_metric)
        else:
            loguru.logger.warning(f"Couldn't evaluate `{evaluator.name}` for dataset: `{dataset.features}`")

    return results


def dump_subset_to_json(
    dataset: datasets.Dataset, save_dir: str, num_samples: int = 100, seed: int = 42, **kws: typ.Any
) -> None:
    """Dump a subset of a dataset to json files."""
    num_samples = min(num_samples, len(dataset))
    subset = dataset.shuffle(seed=seed).select(range(num_samples))

    subset.map(
        DumpReponsesToJson(save_dir=save_dir),
        batched=True,
        desc="Dumping responses to json...",
        **kws,
    )
