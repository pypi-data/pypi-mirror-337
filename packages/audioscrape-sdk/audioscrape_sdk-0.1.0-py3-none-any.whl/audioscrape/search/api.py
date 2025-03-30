class SearchAPI:
    """Client for accessing the Audioscrape Search API"""

    def __init__(self, client):
        """
        Initialize the Search API client.

        Args:
            client (Client): The Audioscrape client instance
        """
        self.client = client

    def search(self, query, limit=20, offset=0):
        """
        Search podcast transcriptions for specific terms or phrases.

        Args:
            query (str): The search query to find in transcriptions
            limit (int, optional): Maximum number of results to return (default: 20)
            offset (int, optional): Number of results to skip for pagination (default: 0)

        Returns:
            dict: Search results with matching podcast segments
        """
        params = {"q": query, "limit": limit, "offset": offset}

        return self.client.request("GET", "search", params=params)
