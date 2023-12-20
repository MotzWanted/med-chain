import typing

import pydantic
from components.loader import models
from components.loader.adapters import base
from typing_extensions import Self, Type

ANSWER_CHOICES_LETTERS = typing.Literal["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]


def _answer_to_int(x: int | ANSWER_CHOICES_LETTERS) -> int:
    """Convert an answer to an integer."""
    if isinstance(x, int):
        return x
    values = typing.get_args(ANSWER_CHOICES_LETTERS)
    if x not in values:
        raise ValueError(f"Invalid answer: `{x}`")
    return values.index(x)


class MedMcQaQueryModel(pydantic.BaseModel):
    """An input query model for MedMcQa."""

    id: str = pydantic.Field(..., description="id")
    question: str = pydantic.Field(..., description="question")
    opa: str = pydantic.Field(..., description="option a")
    opb: str = pydantic.Field(..., description="option b")
    opc: str = pydantic.Field(..., description="option c")
    opd: str = pydantic.Field(..., description="option d")
    cop: int = pydantic.Field(..., description="correct option")


class MedMcQaQueryAdapter(base.Adapter[MedMcQaQueryModel, models.MultipleChoiceModel]):
    """An adapter for multiple-choice datasets."""

    input_model = MedMcQaQueryModel
    output_model = models.MultipleChoiceModel

    @classmethod
    def translate_row(cls: Type[Self], row: dict[str, typing.Any]) -> models.MultipleChoiceModel:
        """Translate a row."""
        m = cls.input_model(**row)
        a_idx = _answer_to_int(m.cop)
        choices = [m.opa, m.opb, m.opc, m.opd]
        return cls.output_model(
            id=m.id,
            question=m.question,
            answers=choices,
            target=a_idx,
        )


class MedQaQueryModel(pydantic.BaseModel):
    """An input query model for MedQa."""

    uid: str = pydantic.Field(..., description="id")
    question: str = pydantic.Field(..., description="question")
    target: int = pydantic.Field(..., description="target")
    answers: list[str] = pydantic.Field(..., description="answers")


class MedQaQueryAdapter(base.Adapter[MedQaQueryModel, models.MultipleChoiceModel]):
    """An adapter for multiple-choice datasets."""

    input_model = MedQaQueryModel
    output_model = models.MultipleChoiceModel

    @classmethod
    def translate_row(cls: Type[Self], row: dict[str, typing.Any]) -> models.MultipleChoiceModel:
        """Translate a row."""
        m = cls.input_model(**row)
        a_idx = _answer_to_int(m.target)
        return cls.output_model(
            id=m.uid,
            question=m.question,
            answers=m.answers,
            target=a_idx,
        )
