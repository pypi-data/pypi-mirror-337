import pytest
import responses

from friday_pulse.client import FridayPulseClient


@pytest.fixture
def results_dates() -> responses.RequestsMock:
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            "https://app.fridaypulse.com/api/v1/info/results-dates",
            json=[{"date": "2025-01-16", "question_count": 10}],
            status=200,
        )
        yield


@pytest.fixture
def results() -> responses.RequestsMock:
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            "https://app.fridaypulse.com/api/v1/results?date=2025-01-16",
            json=[
                {
                    "sample_date": "2025-01-16",
                    "score": 99,
                    "response_rate": 88,
                    "response_count": 89,
                    "total_count": 135,
                    "topic": {"code": "tinker", "name": "bell"},
                }
            ],
            status=200,
        )
        yield


def test_results_dates(results_dates: responses.RequestsMock) -> None:
    client = FridayPulseClient("FooBar")
    response = client.results_dates()

    assert response == [{"date": "2025-01-16", "question_count": 10}]


def test_results(results: responses.RequestsMock) -> None:
    client = FridayPulseClient("TinkerBell")
    response = client.results("2025-01-16")

    assert response == [
        {
            "sample_date": "2025-01-16",
            "score": 99,
            "response_rate": 88,
            "response_count": 89,
            "total_count": 135,
            "topic": {"code": "tinker", "name": "bell"},
        }
    ]
