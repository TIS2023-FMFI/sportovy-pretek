from collections.abc import Mapping, Sequence
from typing import Any

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
        response = requests.get(f"{self.api_endpoint}/competitions", headers=self._get_auth_headers(), count=30)
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
