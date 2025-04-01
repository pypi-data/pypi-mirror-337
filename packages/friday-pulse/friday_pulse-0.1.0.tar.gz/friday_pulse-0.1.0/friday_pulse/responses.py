from typing import TypedDict


class ResultDate(TypedDict):
    """Represents a typed dictionary structure for holding date-related results."""

    date: str
    question_count: int


class Topic(TypedDict):
    """Represents a typed dictionary structure for holding topics."""

    code: str
    name: str


class Result(TypedDict):
    """Represents a typed dictionary structure for holding results."""

    sample_date: str
    score: int
    response_rate: int
    response_count: int
    total_count: int
    topic: Topic
