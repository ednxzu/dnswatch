"""
Unit tests for the JsonResolver class.

Tests cover successful IP retrieval, handling of invalid IPs,
exceptions during HTTP requests, and whitespace trimming.
"""

import pytest
from unittest.mock import patch, Mock
from dnswatch.resolvers.json.json_resolver import JsonResolver


def test_get_ip_success(json_resolver_config):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"ip": "192.0.2.123"}

    with patch(
        "dnswatch.resolvers.json.json_resolver.requests.get",
        return_value=mock_response,
    ):
        resolver = JsonResolver(json_resolver_config)
        ip = resolver.get_ip()
        assert ip == "192.0.2.123"


def test_get_ip_missing_field(json_resolver_config):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"not_ip": "192.0.2.123"}

    with patch(
        "dnswatch.resolvers.json.json_resolver.requests.get",
        return_value=mock_response,
    ):
        resolver = JsonResolver(json_resolver_config)
        with pytest.raises(ValueError, match="IP field 'ip' not found in response"):
            resolver.get_ip()


def test_get_ip_invalid_ip_format(json_resolver_config):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"ip": "invalid_ip"}

    with patch(
        "dnswatch.resolvers.json.json_resolver.requests.get",
        return_value=mock_response,
    ):
        resolver = JsonResolver(json_resolver_config)
        with pytest.raises(ValueError, match="Invalid IP address received"):
            resolver.get_ip()


def test_get_ip_http_error(json_resolver_config):
    with patch(
        "dnswatch.resolvers.json.json_resolver.requests.get",
        side_effect=Exception("HTTP failure"),
    ):
        resolver = JsonResolver(json_resolver_config)
        with pytest.raises(Exception, match="HTTP failure"):
            resolver.get_ip()


def test_get_ip_ipv6(json_resolver_config):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"ip": "2001:db8::1"}

    with patch(
        "dnswatch.resolvers.json.json_resolver.requests.get",
        return_value=mock_response,
    ):
        resolver = JsonResolver(json_resolver_config)
        ip = resolver.get_ip()
        assert ip == "2001:db8::1"
