from collections.abc import Mapping, Sequence
from typing import Any
from orienter.configuration import configuration

import requests


class API:

    def __init__(self, api_key: str, api_endpoint: str):
        self.api_key = api_key
        self.api_endpoint = api_endpoint

    @staticmethod
    def _handle_response(response: requests.Response):
        if 200 <= response.status_code < 300:
            return
        raise RuntimeError(f"API returned a {response.status_code} status code. Content: {response.text}")

    def _get_auth_headers(self):
        return {"ContentType": "application/json", "x-szos-api-key": self.api_key}

    def clubs(self) -> Sequence[Mapping[str: Any]]:
        response = requests.get(f"{self.api_endpoint}/clubs", headers=self._get_auth_headers())
        self._handle_response(response)
        return response.json()

    def club_registrations(self, club_id) -> Sequence[Mapping[str: Any]]:
        '''
        Returns a list of all active competition registrations for the selected club.
        :param club_id:
        '''
        response = requests.get(f"{self.api_endpoint}/clubs/{club_id}/registrations", headers=self._get_auth_headers())
        self._handle_response(response)
        return response.json()

    def competitions(self) -> Sequence[Mapping[str: Any]]:
        '''
        Returns a list of all upcoming competitions.
        '''
        response = requests.get(f"{self.api_endpoint}/competitions", headers=self._get_auth_headers(), params={"count": 30})
        self._handle_response(response)
        return response.json()

    def competition_details(self, competition_id) -> Mapping[str: Any]:
        '''
        Returns detailed information about the competition and its settings.
        :param competition_id:
        '''
        response = requests.get(f"{self.api_endpoint}/competitions/{competition_id}", headers=self._get_auth_headers())
        self._handle_response(response)
        return response.json()


    def competition_registrations(self, competition_id, club_id) -> Sequence[Mapping[str: Any]]:
        '''
        Returns a list of registrations for the specific competition for the given club.
        :param competition_id:
        :param club_id:
        '''
        response = requests.get(f"{self.api_endpoint}/competitions/{competition_id}/entries",
                                params={"club_id": club_id}, headers=self._get_auth_headers())
        self._handle_response(response)
        return response.json()

    def create_registration(self, competition_id, request_body: Mapping[str: Any]) -> Mapping[str: Any]:
        '''
        Registers a runner for a specific competition and returns entry ID and the runner's ID in the entry.
        :param competition_id:
        :param request_body:
        '''
        response = requests.post(f"{self.api_endpoint}/competitions/{competition_id}/entries/save",
                                 json=request_body, headers=self._get_auth_headers())
        self._handle_response(response)
        return response.json()

    def delete_runner(self, competition_id, request_body: Mapping[str: Any]):
        '''
        Deletes a runner from the race registration.
        :param competition_id:
        :param request_body:
        '''
        response = requests.post(f"{self.api_endpoint}/competitions/{competition_id}/entries/delete",
                                 json=request_body, headers=self._get_auth_headers())
        self._handle_response(response)

    def event_results(self, competition_id, event_id) -> Sequence[Mapping[str: Any]]:
        '''
        Returns the list of results for a specific event of the competition.
        :param competition_id:
        :param event_id:
        :return:
        '''
        response = requests.get(f"{self.api_endpoint}/competitions/{competition_id}/results/{event_id}",
                                headers=self._get_auth_headers())
        self._handle_response(response)
        return response.json()

    def runner_details(self, runner_id) -> Sequence[Mapping[str: Any]]:
        '''
        Returns details about the specified runner.
        :param runner_id:
        '''
        response = requests.get(f"{self.api_endpoint}/runners/{runner_id}",
                                headers=self._get_auth_headers())
        self._handle_response(response)
        return response.json()

    def runner_results(self, runner_id, date_from, date_to) -> Sequence[Mapping[str: Any]]:
        '''
        Returns results achieved in the specified time window by the specified runner.
        :param runner_id:
        :param date_from:
        :param date_to:
        '''
        response = requests.get(f"{self.api_endpoint}/runners/{runner_id}/results",
                                params={"date_from" : date_from, "date_to" : date_to}, headers=self._get_auth_headers())
        self._handle_response(response)
        return response.json()

    def registration_details(self, registration_id) -> Sequence[Mapping[str: Any]]:
        '''
        Returns detailed information about the registration.
        :param registration_id:
        '''
        response = requests.get(f"{self.api_endpoint}/registrations/{registration_id}",
                                headers=self._get_auth_headers())
        self._handle_response(response)
        return response.json()

    def available_categories(self, registration_id, event_id) -> Sequence[int]:
        '''
        Returns a list of categories which are available to the runner.
        :param registration_id:
        :param event_id:
        '''
        response = requests.get(f"{self.api_endpoint}/registrations/{registration_id}/categories/{event_id}",
                                headers=self._get_auth_headers())
        self._handle_response(response)
        return response.json()

    def get_lists(self, list_id) -> Sequence[Mapping[str: Any]]:
        '''
        Returns the list of data from the selected directory
        :param list_id:
        '''
        response = requests.get(f"{self.api_endpoint}/lists/{list_id}",
                                headers=self._get_auth_headers())
        self._handle_response(response)
        return response.json()

