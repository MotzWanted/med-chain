import hashlib
import json
import pathlib
import typing as typ
from datetime import datetime

import datasets
import hydra
import loguru
from clients.pipes import ParallelResponseGenerator
from clients.vllm.client import VllmInterface
from components.evaluator.exact_match import ExactMatchAdapter
from components.evaluator.interface import compute_metrics, dump_subset_to_json
from components.models import ModelConfig
from components.pretty_print import print_as_table, print_config
from datasets.utils.logging import disable_progress_bar
from hydra.utils import instantiate
from omegaconf import DictConfig, OmegaConf
from rich.progress import BarColumn, Progress

disable_progress_bar()


@hydra.main(
    config_path="configs",
    config_name="main",
    version_base=None,
)
def run(config: DictConfig) -> None:
    """Run experiment."""
    experiment_dir, results_file = setup_experiment_dir(config)
    write_config_to_file(config, experiment_dir)

    loguru.logger.info("Instantiating dataset...")
    dset: datasets.Dataset = instantiate(config.dataset)
    messages: list[dict[str, str]] = instantiate(config.prompt)

    loguru.logger.info("Instantiating model...")
    model_config: ModelConfig = instantiate(config.model)
    params = {"temperature": config.temperature}
    model = VllmInterface(messages=messages, params=params, **model_config.model_dump())

    average_metrics = {}
    with Progress(
        "[progress.description]{task.description}", BarColumn(), "[progress.percentage]{task.percentage:>3.0f}%"
    ) as progress:
        progress.add_task("Self-Consistency...", total=config.self_consistency)
        metrics = []
        predictions = []
        for _ in range(config.self_consistency):
            dset = dset.map(
                ParallelResponseGenerator(model),
                batched=True,
                batch_size=config.batch_size,
                num_proc=config.num_proc,
                remove_columns=dset.column_names,
                desc="Calling model...",
            )
            dset = dset.map(
                ExactMatchAdapter(target_column="target", answers_column="answers", prediction_column="completion"),
                batched=True,
                batch_size=config.batch_size,
                num_proc=config.num_proc,
                remove_columns=dset.column_names,
                desc="Performing exact match...",
            )
            progress.console.print(print_as_table(dset))
            predictions.append(dset["prediction"])
            dump_subset_to_json(dataset=dset, save_dir=f"{experiment_dir}/responses")

            metrics.append(
                compute_metrics(
                    dataset=dset,
                    metrics=config.metrics,
                    prediction_field="prediction",
                    reference_field="target",
                )
            )
            summed_metrics = {key: sum(d[key] for d in metrics) for key in metrics[0]}
            average_metrics = {key: value / len(metrics) for key, value in summed_metrics.items()}
            progress.console.print(f"Metrics: `{average_metrics}`")

    with open(results_file, "w") as f:
        f.write(
            json.dumps(
                {
                    "avg_metrics": average_metrics,
                    "metrics": metrics,
                    "targets": dset["target"],
                    "predictions": predictions,
                }
            )
        )


def setup_experiment_dir(config: DictConfig) -> typ.Tuple[str, pathlib.Path]:
    """Create the result file and the output directory."""
    date = datetime.now().strftime("%Y-%m-%d")  # noqa: DTZ005
    model_name = config.model.name.replace("/", "_")
    identifier = hashlib.sha256(str(config).encode()).hexdigest()

    output_dir = pathlib.Path(config.system.work_dir, model_name, config.dataset.name_or_path, str(date), identifier)
    result_file = output_dir / "results.json"
    result_file.parent.mkdir(parents=True, exist_ok=True)
    return str(output_dir), result_file


def write_config_to_file(config: DictConfig, save_dir: str) -> None:
    """Write and print the config to a file."""
    with open(f"{save_dir}/config.yaml", "w") as f:
        f.write(OmegaConf.to_yaml(config))
    print_config(config)


if __name__ == "__main__":
    run()  # type: ignore
