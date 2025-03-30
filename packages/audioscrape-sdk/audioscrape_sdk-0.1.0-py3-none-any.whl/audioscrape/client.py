from urllib.parse import urljoin

import requests

from .notifications import NotificationsAPI
from .search import SearchAPI


class Client:
    """Main Audioscrape API client"""

    BASE_URL = "https://www.audioscrape.com/api/"

    def __init__(self, api_key=None, base_url=None):
        """
        Initialize the Audioscrape API client.

        Args:
            api_key (str): Your Audioscrape API key
            base_url (str, optional): Override the default API base URL
        """
        if not api_key:
            raise ValueError("API key is required")

        self.api_key = api_key
        self.base_url = base_url or self.BASE_URL
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

        # Initialize API interfaces
        self.search = SearchAPI(self)
        self.notifications = NotificationsAPI(self)

    def request(self, method, endpoint, params=None, data=None, json=None):
        """
        Make a request to the Audioscrape API.

        Args:
            method (str): HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint (str): API endpoint path
            params (dict, optional): Query parameters
            data (dict, optional): Form data
            json (dict, optional): JSON body data

        Returns:
            dict: API response data

        Raises:
            requests.exceptions.HTTPError: On API errors
        """
        url = urljoin(self.base_url, endpoint)
        response = self.session.request(
            method=method, url=url, params=params, data=data, json=json
        )

        # Raise exceptions for HTTP errors
        response.raise_for_status()

        # Return JSON response if there is one, otherwise return empty dict
        if response.status_code != 204 and response.content:
            return response.json()
        return {}
