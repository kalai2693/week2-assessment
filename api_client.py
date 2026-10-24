
import time
import requests


def fetch_all(url, token, refresh_token_func=None):
    """Fetch all pages from an API using offset pagination."""

    results = []
    offset = 0
    limit = 100
    current_token = token

    while True:
        headers = {"Authorization": f"Bearer {current_token}"}
        params = {"limit": limit, "offset": offset}

        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=30
        )

        # Refresh the token once if the API returns 401
        if response.status_code == 401 and refresh_token_func:
            current_token = refresh_token_func()
            headers = {"Authorization": f"Bearer {current_token}"}
            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=30
            )

        # Wait and retry if rate limited
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", "2"))
            time.sleep(retry_after)
            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=30
            )

        response.raise_for_status()
        page = response.json()

        if not isinstance(page, list):
            raise ValueError("Expected the API to return a list")

        results.extend(page)

        if len(page) < limit:
            break

        offset += limit

    return results
