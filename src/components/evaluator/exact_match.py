import re
import typing as typ

import datasets
import pydantic
from datasets import fingerprint


class ExactMatchModel(pydantic.BaseModel):
    """A model for ExactMatch."""

    predictions: list[str] = pydantic.Field(..., description="The column name containing the predictions.")
    answers: list[list[str]] = pydantic.Field(..., description="The column name containing the answer(s).")


class ExactMatchAdapter:
    """A pipeline that evaluates the predicton to a multiple choice query based on ExactMatch."""

    def __init__(
        self, prediction_column: str, answers_column: str, target_column: str, single_answer: bool = True
    ) -> None:
        self.prediction_column = prediction_column
        self.answers_column = answers_column
        self.target_column = target_column
        self.single_answer = single_answer
        self.symbols = "ABCDEFGHIJ"

    def _find_answer_index(self, prediction: str, answers: list[str]) -> typ.Union[int, list[int]]:
        symbols_regex = rf"\b[{self.symbols}]\b"
        answers_regex = "|".join(re.escape(answer) for answer in answers)
        symbol_matches = re.findall(symbols_regex, prediction)
        exact_matches = re.findall(answers_regex, prediction, re.IGNORECASE)

        if self.single_answer:
            if symbol_matches:
                return self.symbols.index(symbol_matches[0])
            if exact_matches:
                return next(
                    (
                        answers.index(answer)
                        for answer in answers
                        if answer.lower() in (match.lower() for match in exact_matches)
                    ),
                    -1,
                )
            return -1
        indices = []
        for match in symbol_matches:
            indices.append(self.symbols.index(match))
        for match in exact_matches:
            index = next((answers.index(answer) for answer in answers if answer.lower() == match.lower()), None)
            if index is not None:
                indices.append(index)
        return indices or [-1]

    def _extract_prediction(self, prediction: str, answers: list[str]) -> typ.Union[int, list[int]]:
        # Simplify the method to focus on extracting prediction
        return self._find_answer_index(prediction, answers)

    def __call__(self, batch: dict[str, list[typ.Any]]) -> dict[str, list[typ.Any]]:
        """Perform ExactMatch prediction on batch."""
        model = ExactMatchModel(predictions=batch[self.prediction_column], answers=batch[self.answers_column])
        batch["prediction"] = [
            self._extract_prediction(prediction, answers)
            for prediction, answers in zip(model.predictions, model.answers)
        ]
        return batch


@fingerprint.hashregister(ExactMatchAdapter)
def _hash_fetch_from_ds(hasher: datasets.fingerprint.Hasher, obj: ExactMatchAdapter) -> str:
    """Register the _IsIdxIn class to work with datasets.map()."""
    return hasher.hash(
        {
            "cls": obj.__class__,
        }
    )
