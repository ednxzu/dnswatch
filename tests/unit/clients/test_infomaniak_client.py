import os
from unittest.mock import Mock, patch

import pytest
import requests

from dnswatch.clients.infomaniak.infomaniak_dns_client import InfomaniakDnsClient


class TestInfomaniakDnsClient:
    # ========================================================================
    # __init__() tests
    # ========================================================================

    def test_client_init_no_token(self):
        """Test client initialization fails without token."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="API token is required"):
                InfomaniakDnsClient()

    def test_client_init_with_token_param(self):
        """Test client initialization with token parameter."""
        client = InfomaniakDnsClient(api_token="test-token-123")
        assert client.api_token == "test-token-123"
        assert "Bearer test-token-123" in client.api_headers["Authorization"]

    def test_client_init_with_env_var(self):
        """Test client initialization with environment variable."""
        with patch.dict(os.environ, {"INFOMANIAK_API_TOKEN": "env-token-456"}):
            client = InfomaniakDnsClient()
            assert client.api_token == "env-token-456"

    # ========================================================================
    # get_record() tests
    # ========================================================================

    @patch("dnswatch.clients.infomaniak.infomaniak_dns_client.requests.request")
    def test_get_record_success(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": "success",
            "data": [
                {
                    "id": 28071664,
                    "source": "console",
                    "type": "A",
                    "ttl": 3600,
                    "target": "10.4.38.128",
                    "updated_at": 1756120027,
                }
            ],
        }
        mock_request.return_value = mock_response

        with patch.dict(os.environ, {"INFOMANIAK_API_TOKEN": "fake-token-for-testing"}):
            client = InfomaniakDnsClient()

        record = client.get_record("example.com", "console", "A")

        assert record is not None
        assert record["id"] == 28071664
        assert record["target"] == "10.4.38.128"
        assert record["source"] == "console"
        assert record["type"] == "A"
        assert record["ttl"] == 3600

        mock_request.assert_called_once()
        call_kwargs = mock_request.call_args.kwargs
        assert "filter[source]" in call_kwargs["params"]
        assert call_kwargs["params"]["filter[source]"] == "console"

    @patch("dnswatch.clients.infomaniak.infomaniak_dns_client.requests.request")
    def test_get_record_not_found(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": "success",
            "data": [],
        }
        mock_request.return_value = mock_response

        with patch.dict(os.environ, {"INFOMANIAK_API_TOKEN": "fake-token"}):
            client = InfomaniakDnsClient()

        record = client.get_record("example.com", "nonexistent", "A")

        assert record is None

    @patch("dnswatch.clients.infomaniak.infomaniak_dns_client.requests.request")
    def test_get_record_multiple_results(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": "success",
            "data": [
                {
                    "id": 1,
                    "source": "test",
                    "type": "A",
                    "target": "1.1.1.1",
                    "ttl": 300,
                },
                {
                    "id": 2,
                    "source": "test",
                    "type": "A",
                    "target": "2.2.2.2",
                    "ttl": 300,
                },
            ],
        }
        mock_request.return_value = mock_response

        with patch.dict(os.environ, {"INFOMANIAK_API_TOKEN": "fake-token"}):
            client = InfomaniakDnsClient()

        record = client.get_record("example.com", "test", "A")

        assert record["id"] == 1
        assert record["target"] == "1.1.1.1"

    @patch("dnswatch.clients.infomaniak.infomaniak_dns_client.requests.request")
    def test_get_record_401_unauthorized(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            response=mock_response
        )
        mock_request.return_value = mock_response

        with patch.dict(os.environ, {"INFOMANIAK_API_TOKEN": "fake-token"}):
            client = InfomaniakDnsClient()

        with pytest.raises(ValueError, match="Invalid Infomaniak API token"):
            client.get_record("example.com", "test", "A")

    @patch("dnswatch.clients.infomaniak.infomaniak_dns_client.requests.request")
    def test_get_record_403_forbidden(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            response=mock_response
        )
        mock_request.return_value = mock_response

        with patch.dict(os.environ, {"INFOMANIAK_API_TOKEN": "fake-token"}):
            client = InfomaniakDnsClient()

        with pytest.raises(
            ValueError, match="No permission to send GET to route 2/zones/example.com/records"
        ):
            client.get_record("example.com", "test", "A")

    @patch("dnswatch.clients.infomaniak.infomaniak_dns_client.requests.request")
    def test_get_record_404_zone_not_found(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            response=mock_response
        )
        mock_request.return_value = mock_response

        with patch.dict(os.environ, {"INFOMANIAK_API_TOKEN": "fake-token"}):
            client = InfomaniakDnsClient()

        with pytest.raises(requests.exceptions.HTTPError):
            client.get_record("nonexistent.com", "test", "A")

    @patch("dnswatch.clients.infomaniak.infomaniak_dns_client.requests.request")
    def test_get_record_429_rate_limit(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            response=mock_response
        )
        mock_request.return_value = mock_response

        with patch.dict(os.environ, {"INFOMANIAK_API_TOKEN": "fake-token"}):
            client = InfomaniakDnsClient()

        with pytest.raises(requests.exceptions.HTTPError):
            client.get_record("example.com", "test", "A")

    @patch("dnswatch.clients.infomaniak.infomaniak_dns_client.requests.request")
    def test_get_record_timeout(self, mock_request):
        mock_request.side_effect = requests.exceptions.Timeout()

        with patch.dict(os.environ, {"INFOMANIAK_API_TOKEN": "fake-token"}):
            client = InfomaniakDnsClient()

        with pytest.raises(requests.exceptions.Timeout):
            client.get_record("example.com", "test", "A")

    @patch("dnswatch.clients.infomaniak.infomaniak_dns_client.requests.request")
    def test_get_record_connection_error(self, mock_request):
        mock_request.side_effect = requests.exceptions.ConnectionError()

        with patch.dict(os.environ, {"INFOMANIAK_API_TOKEN": "fake-token"}):
            client = InfomaniakDnsClient()

        with pytest.raises(requests.exceptions.ConnectionError):
            client.get_record("example.com", "test", "A")

    # ========================================================================
    # create_record() tests
    # ========================================================================

    @patch("dnswatch.clients.infomaniak.infomaniak_dns_client.requests.request")
    def test_create_record_success(self, mock_request):
        """Test successful record creation."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": "success",
            "data": {
                "id": 12345,
                "source": "test",
                "type": "A",
                "target": "1.2.3.4",
                "ttl": 300,
                "updated_at": 1234567890,
            },
        }
        mock_request.return_value = mock_response

        with patch.dict(os.environ, {"INFOMANIAK_API_TOKEN": "fake-token"}):
            client = InfomaniakDnsClient()

        record = client.create_record("example.com", "test", "1.2.3.4", ttl=300, record_type="A")

        assert record is not None
        assert record["id"] == 12345
        assert record["source"] == "test"
        assert record["target"] == "1.2.3.4"
        assert record["ttl"] == 300

        mock_request.assert_called_once()
        call_kwargs = mock_request.call_args.kwargs
        assert call_kwargs["method"] == "POST"
        assert "2/zones/example.com/records" in call_kwargs["url"]
        assert call_kwargs["json"] == {
            "source": "test",
            "target": "1.2.3.4",
            "ttl": 300,
            "type": "A",
        }

    @patch("dnswatch.clients.infomaniak.infomaniak_dns_client.requests.request")
    def test_create_record_with_defaults(self, mock_request):
        """Test record creation with default TTL and type."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": "success",
            "data": {
                "id": 12345,
                "source": "test",
                "type": "A",
                "target": "1.2.3.4",
                "ttl": 300,
                "updated_at": 1234567890,
            },
        }
        mock_request.return_value = mock_response

        with patch.dict(os.environ, {"INFOMANIAK_API_TOKEN": "fake-token"}):
            client = InfomaniakDnsClient()

        record = client.create_record("example.com", "test", "1.2.3.4")

        assert record is not None
        call_kwargs = mock_request.call_args.kwargs
        assert call_kwargs["json"]["ttl"] == 3600
        assert call_kwargs["json"]["type"] == "A"

    @patch("dnswatch.clients.infomaniak.infomaniak_dns_client.requests.request")
    def test_create_record_invalid_ttl_too_low(self, mock_request):
        """Test that TTL below 60 raises ValueError."""
        with patch.dict(os.environ, {"INFOMANIAK_API_TOKEN": "fake-token"}):
            client = InfomaniakDnsClient()

        with pytest.raises(ValueError, match="ttl must be between 60 and 86400"):
            client.create_record("example.com", "test", "1.2.3.4", ttl=59)

        mock_request.assert_not_called()

    @patch("dnswatch.clients.infomaniak.infomaniak_dns_client.requests.request")
    def test_create_record_invalid_ttl_too_high(self, mock_request):
        """Test that TTL above 86400 raises ValueError."""
        with patch.dict(os.environ, {"INFOMANIAK_API_TOKEN": "fake-token"}):
            client = InfomaniakDnsClient()

        with pytest.raises(ValueError, match="ttl must be between 60 and 86400"):
            client.create_record("example.com", "test", "1.2.3.4", ttl=86401)

        mock_request.assert_not_called()

    @patch("dnswatch.clients.infomaniak.infomaniak_dns_client.requests.request")
    def test_create_record_api_failure(self, mock_request):
        """Test that API failure raises ValueError."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": "error", "error": "Invalid zone"}
        mock_request.return_value = mock_response

        with patch.dict(os.environ, {"INFOMANIAK_API_TOKEN": "fake-token"}):
            client = InfomaniakDnsClient()

        with pytest.raises(ValueError, match="Failed to create record: Invalid zone"):
            client.create_record("example.com", "test", "1.2.3.4")

    @patch("dnswatch.clients.infomaniak.infomaniak_dns_client.requests.request")
    def test_create_record_http_error(self, mock_request):
        """Test that HTTP errors are raised."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            response=mock_response
        )
        mock_request.return_value = mock_response

        with patch.dict(os.environ, {"INFOMANIAK_API_TOKEN": "fake-token"}):
            client = InfomaniakDnsClient()

        with pytest.raises(requests.exceptions.HTTPError):
            client.create_record("example.com", "test", "1.2.3.4")

    # ========================================================================
    # update_record() tests
    # ========================================================================

    @patch("dnswatch.clients.infomaniak.infomaniak_dns_client.requests.request")
    def test_update_record_all_fields(self, mock_request):
        """Test updating all fields of a record."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": "success",
            "data": {
                "id": 12345,
                "source": "test",
                "type": "A",
                "target": "5.6.7.8",
                "ttl": 600,
                "updated_at": 1234567890,
            },
        }
        mock_request.return_value = mock_response

        with patch.dict(os.environ, {"INFOMANIAK_API_TOKEN": "fake-token"}):
            client = InfomaniakDnsClient()

        record = client.update_record(
            "example.com", "12345", target="5.6.7.8", ttl=600, record_type="A"
        )

        assert record is not None
        assert record["target"] == "5.6.7.8"
        assert record["ttl"] == 600

        mock_request.assert_called_once()
        call_kwargs = mock_request.call_args.kwargs
        assert call_kwargs["method"] == "PUT"
        assert "2/zones/example.com/records/12345" in call_kwargs["url"]
        assert call_kwargs["json"] == {"target": "5.6.7.8", "ttl": 600, "type": "A"}

    @patch("dnswatch.clients.infomaniak.infomaniak_dns_client.requests.request")
    def test_update_record_only_target(self, mock_request):
        """Test updating only the target field."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": "success",
            "data": {
                "id": 12345,
                "source": "test",
                "type": "A",
                "target": "5.6.7.8",
                "ttl": 300,
                "updated_at": 1234567890,
            },
        }
        mock_request.return_value = mock_response

        with patch.dict(os.environ, {"INFOMANIAK_API_TOKEN": "fake-token"}):
            client = InfomaniakDnsClient()

        record = client.update_record("example.com", "12345", target="5.6.7.8")

        assert record is not None
        call_kwargs = mock_request.call_args.kwargs
        assert call_kwargs["json"] == {"target": "5.6.7.8"}

    @patch("dnswatch.clients.infomaniak.infomaniak_dns_client.requests.request")
    def test_update_record_only_ttl(self, mock_request):
        """Test updating only the TTL field."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": "success",
            "data": {
                "id": 12345,
                "source": "test",
                "type": "A",
                "target": "1.2.3.4",
                "ttl": 600,
                "updated_at": 1234567890,
            },
        }
        mock_request.return_value = mock_response

        with patch.dict(os.environ, {"INFOMANIAK_API_TOKEN": "fake-token"}):
            client = InfomaniakDnsClient()

        record = client.update_record("example.com", "12345", ttl=600)

        assert record is not None
        call_kwargs = mock_request.call_args.kwargs
        assert call_kwargs["json"] == {"ttl": 600}

    @patch("dnswatch.clients.infomaniak.infomaniak_dns_client.requests.request")
    def test_update_record_no_fields(self, mock_request):
        """Test that updating with no fields raises ValueError."""
        with patch.dict(os.environ, {"INFOMANIAK_API_TOKEN": "fake-token"}):
            client = InfomaniakDnsClient()

        with pytest.raises(ValueError, match="Must provide at least one field to update"):
            client.update_record("example.com", "12345")

        mock_request.assert_not_called()

    @patch("dnswatch.clients.infomaniak.infomaniak_dns_client.requests.request")
    def test_update_record_invalid_ttl(self, mock_request):
        """Test that invalid TTL raises ValueError."""
        with patch.dict(os.environ, {"INFOMANIAK_API_TOKEN": "fake-token"}):
            client = InfomaniakDnsClient()

        with pytest.raises(ValueError, match="ttl must be between 60 and 86400"):
            client.update_record("example.com", "12345", ttl=30)

        mock_request.assert_not_called()

    @patch("dnswatch.clients.infomaniak.infomaniak_dns_client.requests.request")
    def test_update_record_api_failure(self, mock_request):
        """Test that API failure raises ValueError."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": "error", "error": "Record not found"}
        mock_request.return_value = mock_response

        with patch.dict(os.environ, {"INFOMANIAK_API_TOKEN": "fake-token"}):
            client = InfomaniakDnsClient()

        with pytest.raises(ValueError, match="Failed to update record: Record not found"):
            client.update_record("example.com", "12345", target="5.6.7.8")

    @patch("dnswatch.clients.infomaniak.infomaniak_dns_client.requests.request")
    def test_update_record_http_404(self, mock_request):
        """Test that 404 (record not found) raises HTTPError."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            response=mock_response
        )
        mock_request.return_value = mock_response

        with patch.dict(os.environ, {"INFOMANIAK_API_TOKEN": "fake-token"}):
            client = InfomaniakDnsClient()

        with pytest.raises(requests.exceptions.HTTPError):
            client.update_record("example.com", "99999", target="5.6.7.8")

    # ========================================================================
    # _make_api_request() edge cases for 100% coverage
    # ========================================================================

    @patch("dnswatch.clients.infomaniak.infomaniak_dns_client.requests.request")
    def test_make_api_request_invalid_method(self, mock_request):
        """Test that invalid HTTP method raises ValueError."""
        with patch.dict(os.environ, {"INFOMANIAK_API_TOKEN": "fake-token"}):
            client = InfomaniakDnsClient()

        with pytest.raises(ValueError, match="Invalid method"):
            client._make_api_request("INVALID", "2/zones/test")

        mock_request.assert_not_called()

    @patch("dnswatch.clients.infomaniak.infomaniak_dns_client.requests.request")
    def test_make_api_request_connection_error(self, mock_request):
        """Test that ConnectionError is handled properly."""
        mock_request.side_effect = requests.exceptions.ConnectionError("Network down")

        with patch.dict(os.environ, {"INFOMANIAK_API_TOKEN": "fake-token"}):
            client = InfomaniakDnsClient()

        with pytest.raises(requests.exceptions.ConnectionError):
            client._make_api_request("GET", "2/zones/test")

    @patch("dnswatch.clients.infomaniak.infomaniak_dns_client.requests.request")
    def test_make_api_request_generic_request_exception(self, mock_request):
        """Test that generic RequestException is handled properly."""
        mock_request.side_effect = requests.exceptions.RequestException("Generic error")

        with patch.dict(os.environ, {"INFOMANIAK_API_TOKEN": "fake-token"}):
            client = InfomaniakDnsClient()

        with pytest.raises(requests.exceptions.RequestException):
            client._make_api_request("GET", "2/zones/test")
