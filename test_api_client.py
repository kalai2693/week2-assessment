
from unittest.mock import Mock, patch

from api_client import fetch_all


@patch("api_client.requests.get")
def test_fetch_all_pagination(mock_get):
    first = Mock()
    first.status_code = 200
    first.json.return_value = [{"id": i} for i in range(100)]
    first.headers = {}

    second = Mock()
    second.status_code = 200
    second.json.return_value = [{"id": 101}]
    second.headers = {}

    mock_get.side_effect = [first, second]

    result = fetch_all("https://example.test/items", token="test-token")

    assert len(result) == 101
    assert mock_get.call_count == 2


@patch("api_client.requests.get")
def test_fetch_all_refreshes_token_after_401(mock_get):
    unauthorized = Mock()
    unauthorized.status_code = 401
    unauthorized.headers = {}

    success = Mock()
    success.status_code = 200
    success.json.return_value = [{"id": 1}]
    success.headers = {}

    mock_get.side_effect = [unauthorized, success]

    refresh = Mock(return_value="new-token")
    result = fetch_all(
        "https://example.test/items",
        token="old-token",
        refresh_token_func=refresh,
    )

    assert result == [{"id": 1}]
    refresh.assert_called_once_with()


@patch("api_client.time.sleep")
@patch("api_client.requests.get")
def test_fetch_all_retries_after_rate_limit(mock_get, mock_sleep):
    limited = Mock()
    limited.status_code = 429
    limited.headers = {"Retry-After": "2"}

    success = Mock()
    success.status_code = 200
    success.json.return_value = [{"id": 1}]
    success.headers = {}

    mock_get.side_effect = [limited, success]

    result = fetch_all("https://example.test/items", token="test-token")

    assert result == [{"id": 1}]
    mock_sleep.assert_called_once_with(2)
    assert mock_get.call_count == 2
