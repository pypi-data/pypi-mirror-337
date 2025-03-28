import requests
import json

class ApiClient:
    """
    A scraper class to interact with a scraping service API.
    """

    def __init__(self, api_key):
        """
        Initialize the scraper with an API key.

        :param api_key: Your API key for the scraping service.
        """
        if not api_key:
            raise ValueError("API key is required")
        self.api_key = api_key
        self.base_url = 'https://apinew.livescraper.com/'
        # self.base_url = 'http://localhost:4000/'

    def _make_request(self, endpoint, queries, language=None, region=None, dropduplicates=None, enrichment=None, fields=None):
        """
        Internal helper method to make API requests.
        """
        if queries is None:
            queries = []
        if fields is None:
            fields = []

        queries_json = json.dumps(queries)
        fields_json = json.dumps(fields) if fields else None

        try:
            response = requests.get(
                f"{self.base_url}{endpoint}",
                params={
                    "key": self.api_key,
                    "queries": queries_json,
                    "language": language,
                    "region": region,
                    "dropduplicates": dropduplicates,
                    "enrichment": enrichment,
                    "fields": fields_json,
                },
            )
            response.raise_for_status()
            return response.json()
        
        except requests.HTTPError as http_err:
            try:
                error_json = response.json()
                if "error" in error_json:
                    error_message = json.dumps(error_json["error"], indent=4)
                else:
                    error_message = response.text
            except json.JSONDecodeError:
                error_message = response.text
            raise RuntimeError(f"Failed to fetch data: {error_message}") from http_err

        except requests.RequestException as req_err:
            raise RuntimeError(f"Request failed: {str(req_err)}") from req_err

    def google_maps_search(self, queries, language=None, region=None, dropduplicates=None, enrichment=None, fields=None):
        """Search Google Maps for places."""
        return self._make_request("api/v1/task/map", queries, language, region, dropduplicates, enrichment, fields)

    def google_review_search(self, queries, language=None, region=None, dropduplicates=None, enrichment=None, fields=None):
        """Search Google for reviews."""
        return self._make_request("api/v1/task/review", queries, language, region, dropduplicates, enrichment, fields)

    def google_email_search(self, queries, language=None, region=None, dropduplicates=None, enrichment=None, fields=None):
        """Search Google for emails."""
        return self._make_request("api/v1/task/email", queries, language, region, dropduplicates, enrichment, fields)
