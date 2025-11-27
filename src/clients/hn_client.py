import requests
from typing import Any, Dict, List, Optional

HN_BASE = "https://hacker-news.firebaseio.com/v0"


class HackerNewsClient:
    """Client for interacting with the Hacker News API."""

    def __init__(self, base_url: str = HN_BASE, timeout: int = 10):
        """
        initialise the client

        Args:
            base_url: HN API URL
            timeout: timeout time in seconds
        """
        self.base_url = base_url
        self.timeout = timeout

    def _get(self, path: str) -> Any:
        """
        Get request to the API path
        Args:
            path: API path
        
        Returns:
            Parsed JSON response
        
        Raises:
            HTTPError if the request fails

        """
        url = f"{self.base_url}/{path}.json"
        r = requests.get(url, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def top_story_ids(self, limit: int = 60) -> List[int]:
        """
        Fetch IDs for the top stories

        Args:
            limit: Max number of IDs (default to 60)
        
        Returns:
            List of IDs.
        """
        return self._get("topstories")[:limit]

    def get_item(self, item_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve item by ID

        Args:
            item_id: story ID
        
        Returns:
            Item dict (or None if not foudn)
        """
        return self._get(f"item/{item_id}")
