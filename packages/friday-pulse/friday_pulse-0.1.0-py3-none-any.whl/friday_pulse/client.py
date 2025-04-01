from typing import Any

import requests

from friday_pulse.responses import Result, ResultDate


class FridayPulseClient:
    """This class provides a client for interacting with the FridayPulse API.

    The class facilitates communication with the FridayPulse service via HTTP
    requests. It enables users to authenticate using a bearer token and interact
    with specific API endpoints such as retrieving available result dates and
    fetching results for a given date.
    """

    def __init__(self, bearer_token: str):
        """A class for managing a bearer token used for authentication in API requests.

        Handles the initialization of a secure bearer token used to interact with
        systems requiring such authentication mechanisms. This class ensures the token
        is stored appropriately to be utilized in relevant requests or operations.
        """
        self._bearer_token = bearer_token

    def _request(self, url: str) -> Any:
        """Sends a GET request to the specified URL, appending it to the base URL.

        The request incorporates an Authorization header containing a Bearer token.
        Returns the JSON response received from the external service.
        """
        response = requests.get(
            "https://app.fridaypulse.com/" + url,
            headers={"Authorization": f"Bearer {self._bearer_token}"},
        )
        response.raise_for_status()

        return response.json()

    def results_dates(self) -> list[ResultDate]:
        """Retrieves the results dates from the API."""
        response: list[ResultDate] = self._request("api/v1/info/results-dates")
        return response

    def results(self, date: str) -> list[Result]:
        """Retrieves results for a given date from the API."""
        response: list[Result] = self._request(f"api/v1/results?date={date}")
        return response
