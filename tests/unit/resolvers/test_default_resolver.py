from unittest.mock import Mock, patch

import pytest

from dnswatch.resolvers.default.default_resolver import DefaultResolver


class TestDefaultResolver:
    def test_get_ip_success(self, default_resolver_config):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "192.0.2.123"

        with patch(
            "dnswatch.resolvers.default.default_resolver.requests.get",
            return_value=mock_response,
        ):
            resolver = DefaultResolver(default_resolver_config)
            ip = resolver.get_ip()
            assert ip == "192.0.2.123"

    def test_get_ip_failure(self, default_resolver_config):
        with patch(
            "dnswatch.resolvers.default.default_resolver.requests.get",
            side_effect=Exception("oops"),
        ):
            resolver = DefaultResolver(default_resolver_config)
            with pytest.raises(Exception, match="oops"):
                resolver.get_ip()

    def test_get_ip_trailing_whitespace(self, default_resolver_config):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "203.0.113.42\n"

        with patch(
            "dnswatch.resolvers.default.default_resolver.requests.get",
            return_value=mock_response,
        ):
            resolver = DefaultResolver(default_resolver_config)
            ip = resolver.get_ip()
            assert ip == "203.0.113.42"

    def test_get_ip_ipv6(self, default_resolver_config):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "2001:db8::1"

        with patch(
            "dnswatch.resolvers.default.default_resolver.requests.get",
            return_value=mock_response,
        ):
            resolver = DefaultResolver(default_resolver_config)
            ip = resolver.get_ip()
            assert ip == "2001:db8::1"

    def test_get_ip_malformed(self, default_resolver_config):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "not_an_ip_address"

        with patch(
            "dnswatch.resolvers.default.default_resolver.requests.get",
            return_value=mock_response,
        ):
            resolver = DefaultResolver(default_resolver_config)
            with pytest.raises(ValueError, match="Invalid IP address received"):
                resolver.get_ip()

    def test_get_ip_empty_response(self, default_resolver_config):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = ""

        with patch(
            "dnswatch.resolvers.default.default_resolver.requests.get",
            return_value=mock_response,
        ):
            resolver = DefaultResolver(default_resolver_config)
            with pytest.raises(ValueError, match="Invalid IP address received"):
                resolver.get_ip()

    def test_get_ip_invalid_format(self, default_resolver_config):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "512.278.780.999"

        with patch(
            "dnswatch.resolvers.default.default_resolver.requests.get",
            return_value=mock_response,
        ):
            resolver = DefaultResolver(default_resolver_config)
            with pytest.raises(ValueError, match="Invalid IP address received"):
                resolver.get_ip()
