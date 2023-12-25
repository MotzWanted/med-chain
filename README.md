🌟 Official repository for the paper [Can large language models reason about medical questions?](https://arxiv.org/abs/2207.08143) (Version 3)

[![PWC](https://img.shields.io/endpoint.svg?url=https://paperswithcode.com/badge/can-large-language-models-reason-about/question-answering-on-medqa-usmle)](https://paperswithcode.com/sota/question-answering-on-medqa-usmle?p=can-large-language-models-reason-about)
[![PWC](https://img.shields.io/endpoint.svg?url=https://paperswithcode.com/badge/can-large-language-models-reason-about/multiple-choice-question-answering-mcqa-on-21)](https://paperswithcode.com/sota/multiple-choice-question-answering-mcqa-on-21?p=can-large-language-models-reason-about)
[![PWC](https://img.shields.io/endpoint.svg?url=https://paperswithcode.com/badge/can-large-language-models-reason-about/question-answering-on-pubmedqa)](https://paperswithcode.com/sota/question-answering-on-pubmedqa?p=can-large-language-models-reason-about)


## Table of Contents

- [Introduction](#introduction)
  - [Repository Update and Legacy Code](#repository-update-and-legacy-code)
- [Setup](#setup)
  - [Install Poetry](#install-poetry)
  - [Install Dependencies](#install-dependencies)
  - [Install vLLM](#install-vllm)
- [Usage](#usage)
  - [Instantiate Model](#instantiate-model)
  - [Running One Experiment](#running-one-experiment)
  - [Running a Group of Experiments](#running-a-group-of-experiments)
- [Abstract](#abstract)
- [Citation](#citation)
- [Acknowledgments](#acknowledgments)

## Introduction

Welcome to the official codebase supporting the research paper [Can large language models reason about medical questions?](https://arxiv.org/abs/2207.08143) version 3.

### Repository Update and Legacy Code

**New Repository (`med-chain`):** With the latest version of our paper, we have transitioned to using open-source large language models. This shift marks a significant update in our research methodology and the tools we use. The relevant code and resources are available in the `med-chain` repository.

**Legacy Repository (`medical-reasoning`):** Earlier versions of our research, including work with OpenAI GPT-3.5, are documented in the `medical-reasoning` repository. This repository includes all the relevant code and data from our earlier research phases. The repository is available at [https://github.com/vlievin/medical-reasoning](https://github.com/vlievin/medical-reasoning).


## Setup

<details>
<summary>Install poetry</summary>

Detailed steps to get the development environment up and running.

### Install Poetry

```shell
curl -sSL https://install.python-poetry.org | python3 -
```

</details>
<details>
<summary>Install dependencies</summary>

```shell
poetry install
```

</details>

<details>
<summary>Install vLLM</summary>

```shell
bash scripts/install_vllm.sh 3.11
```

</details>

## Usage

### Instantiate Model
Instantiate open-source model using [vLLM](https://docs.vllm.ai/en/latest/index.html)
```shell
bash scripts/init_vllm.sh <args>
# Example
bash scripts/init_vllm.sh 
```
[Supported models](https://docs.vllm.ai/en/latest/models/supported_models.html)

Use `poetry run` to load and run using the `poetry` environment.

### Running One Experiment

```shell
poetry run experiment <args>
# Example
poetry run experiment engine=code dataset.name=medqa_us dataset.subset=10
```

### Running a Group of Experiments

```shell
poetry run experiment --multirun <args>
# Example
poetry run experiment --multirun dataset=medqa,medmcqa
```

## with `Poe`
```shell
poetry run poe multi-medqa <args>
# Example
poetry run poe multi-medqa model=llama-2-7b
```

## Abstract

> Although large language models (LLMs) often produce impressive outputs, it remains unclear how they perform in real-world scenarios requiring strong reasoning skills and expert domain knowledge. We set out to investigate whether GPT-3.5 (Codex and InstructGPT) can be applied to answer and reason about difficult real-world-based questions. We utilize two multiple-choice medical exam questions (USMLE and MedMCQA) and a medical reading comprehension dataset (PubMedQA). We investigate multiple prompting scenarios: Chain-of-Thought (CoT, think step-by-step), zero- and few-shot (prepending the question with question-answer exemplars) and retrieval augmentation (injecting Wikipedia passages into the prompt). For a subset of the USMLE questions, a medical expert reviewed and annotated the model's CoT. We found that InstructGPT can often read, reason and recall expert knowledge. Failure are primarily due to lack of knowledge and reasoning errors and trivial guessing heuristics are observed, e.g.\ too often predicting labels A and D on USMLE. Sampling and combining many completions overcome some of these limitations. Using 100 samples, Codex 5-shot CoT not only gives close to well-calibrated predictive probability but also achieves human-level performances on the three datasets. USMLE: 60.2%, MedMCQA: 57.5% and PubMedQA: 78.2%.

## Citation

```
@misc{https://doi.org/10.48550/arxiv.2207.08143,
  doi = {10.48550/ARXIV.2207.08143},
  url = {https://arxiv.org/abs/2207.08143},
  author = {Liévin, Valentin and Hother, Christoffer Egeberg and Winther, Ole},
  keywords = {Computation and Language (cs.CL), Artificial Intelligence (cs.AI), Machine Learning (cs.LG), FOS: Computer and information sciences, FOS: Computer and information sciences, I.2.1; I.2.7},
  title = {Can large language models reason about medical questions?},
  publisher = {arXiv},
  year = {2022},
  copyright = {arXiv.org perpetual, non-exclusive license}
}
```


## Acknowledgments

> We thank OpenAI for granting access to the Codex private beta program. We acknowledge EuroHPC Joint Undertaking for awarding us access to MeluXina at LuxProvide, Luxembourg. 
