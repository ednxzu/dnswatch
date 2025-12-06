from unittest.mock import Mock, patch

import pytest

from dnswatch.resolvers.default.default_resolver import DefaultResolver


class TestDefaultResolver:
    @pytest.fixture
    def config_mock(self):
        class Config:
            url = "https://icanhazip.com"

        return Config()

    @patch("dnswatch.resolvers.default.default_resolver.requests.get")
    def test_get_ip_success(self, mock_get, config_mock):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "192.0.2.123"
        mock_get.return_value = mock_response

        resolver = DefaultResolver(config_mock)
        ip = resolver.get_ip()

        assert ip == "192.0.2.123"
        mock_get.assert_called_once_with("https://icanhazip.com", timeout=5)

    @patch("dnswatch.resolvers.default.default_resolver.requests.get")
    def test_get_ip_strips_whitespace(self, mock_get, config_mock):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "  203.0.113.42\n  "
        mock_get.return_value = mock_response

        resolver = DefaultResolver(config_mock)
        ip = resolver.get_ip()

        assert ip == "203.0.113.42"

    @patch("dnswatch.resolvers.default.default_resolver.requests.get")
    def test_get_ip_ipv6(self, mock_get, config_mock):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "2001:db8::1"
        mock_get.return_value = mock_response

        resolver = DefaultResolver(config_mock)
        ip = resolver.get_ip()

        assert ip == "2001:db8::1"

    @patch("dnswatch.resolvers.default.default_resolver.requests.get")
    def test_get_ip_invalid_format_raises_error(self, mock_get, config_mock):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "not_an_ip_address"
        mock_get.return_value = mock_response

        resolver = DefaultResolver(config_mock)
        with pytest.raises(ValueError, match="Invalid IP address received"):
            resolver.get_ip()

    @patch("dnswatch.resolvers.default.default_resolver.requests.get")
    def test_get_ip_empty_response_raises_error(self, mock_get, config_mock):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = ""
        mock_get.return_value = mock_response

        resolver = DefaultResolver(config_mock)
        with pytest.raises(ValueError, match="Invalid IP address received"):
            resolver.get_ip()

    @patch("dnswatch.resolvers.default.default_resolver.requests.get")
    def test_get_ip_malformed_ip_raises_error(self, mock_get, config_mock):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "512.278.780.999"
        mock_get.return_value = mock_response

        resolver = DefaultResolver(config_mock)
        with pytest.raises(ValueError, match="Invalid IP address received"):
            resolver.get_ip()

    @patch("dnswatch.resolvers.default.default_resolver.requests.get")
    def test_get_ip_http_error_raises(self, mock_get, config_mock):
        mock_get.side_effect = Exception("Connection failed")

        resolver = DefaultResolver(config_mock)
        with pytest.raises(Exception, match="Connection failed"):
            resolver.get_ip()

    @patch("dnswatch.resolvers.default.default_resolver.requests.get")
    def test_get_ip_uses_timeout(self, mock_get, config_mock):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "1.2.3.4"
        mock_get.return_value = mock_response

        resolver = DefaultResolver(config_mock)
        resolver.get_ip()

        mock_get.assert_called_once_with("https://icanhazip.com", timeout=5)
