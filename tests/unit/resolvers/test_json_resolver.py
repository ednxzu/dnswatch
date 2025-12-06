from unittest.mock import Mock, patch

import pytest

from dnswatch.resolvers.json.json_resolver import JsonResolver


class TestJsonResolver:
    @pytest.fixture
    def config_mock(self):
        class Config:
            url = "https://api.ipify.org?format=json"
            ip_field = "ip"

        return Config()

    @patch("dnswatch.resolvers.json.json_resolver.requests.get")
    def test_get_ip_success(self, mock_get, config_mock):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"ip": "192.0.2.123"}
        mock_get.return_value = mock_response

        resolver = JsonResolver(config_mock)
        ip = resolver.get_ip()

        assert ip == "192.0.2.123"
        mock_get.assert_called_once_with("https://api.ipify.org?format=json", timeout=5)

    @patch("dnswatch.resolvers.json.json_resolver.requests.get")
    def test_get_ip_ipv6(self, mock_get, config_mock):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"ip": "2001:db8::1"}
        mock_get.return_value = mock_response

        resolver = JsonResolver(config_mock)
        ip = resolver.get_ip()

        assert ip == "2001:db8::1"

    @patch("dnswatch.resolvers.json.json_resolver.requests.get")
    def test_get_ip_custom_field_name(self, mock_get, config_mock):
        config_mock.ip_field = "address"
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"address": "203.0.113.42"}
        mock_get.return_value = mock_response

        resolver = JsonResolver(config_mock)
        ip = resolver.get_ip()

        assert ip == "203.0.113.42"

    @patch("dnswatch.resolvers.json.json_resolver.requests.get")
    def test_get_ip_missing_field_raises_error(self, mock_get, config_mock):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"not_ip": "192.0.2.123"}
        mock_get.return_value = mock_response

        resolver = JsonResolver(config_mock)
        with pytest.raises(ValueError, match="IP field 'ip' not found in response"):
            resolver.get_ip()

    @patch("dnswatch.resolvers.json.json_resolver.requests.get")
    def test_get_ip_invalid_ip_format_raises_error(self, mock_get, config_mock):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"ip": "invalid_ip"}
        mock_get.return_value = mock_response

        resolver = JsonResolver(config_mock)
        with pytest.raises(ValueError, match="Invalid IP address received"):
            resolver.get_ip()

    @patch("dnswatch.resolvers.json.json_resolver.requests.get")
    def test_get_ip_http_error_raises(self, mock_get, config_mock):
        mock_get.side_effect = Exception("Connection failed")

        resolver = JsonResolver(config_mock)
        with pytest.raises(Exception, match="Connection failed"):
            resolver.get_ip()

    @patch("dnswatch.resolvers.json.json_resolver.requests.get")
    def test_get_ip_uses_timeout(self, mock_get, config_mock):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"ip": "1.2.3.4"}
        mock_get.return_value = mock_response

        resolver = JsonResolver(config_mock)
        resolver.get_ip()

        mock_get.assert_called_once_with("https://api.ipify.org?format=json", timeout=5)
