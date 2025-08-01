"""
Pytest configuration and fixtures for dnswatch tests.

Provides reusable pytest fixtures such as default_resolver_config
to setup configuration objects for testing resolver components.
"""

import pytest
from oslo_config import cfg


@pytest.fixture(scope="session", autouse=True)
def setup_resolvers_default_group():
    """Ensure 'resolvers.default' group and 'url' option are registered globally."""
    group = cfg.OptGroup(name="resolvers.default")

    conf = cfg.CONF
    try:
        conf.register_group(group)
    except cfg.DuplicateOptGroupError:
        pass

    try:
        conf.register_opts([cfg.StrOpt("url")], group=group)
    except cfg.DuplicateOptError:
        pass

    conf["resolvers.default"].url = "http://example.com"

    yield


@pytest.fixture
def default_resolver_config():
    """Return the global 'resolvers.default' config group for use in tests."""
    return cfg.CONF["resolvers.default"]


@pytest.fixture(scope="session", autouse=True)
def setup_resolvers_json_group():
    """Ensure 'resolvers.json' group and its options are registered globally."""
    group = cfg.OptGroup(name="resolvers.json")

    conf = cfg.CONF
    try:
        conf.register_group(group)
    except cfg.DuplicateOptGroupError:
        pass

    opts = [
        cfg.StrOpt(
            "url",
            default="https://api.ipify.org?format=json",
            help="URL to fetch the public IP address from (default: https://api.ipify.org?format=json).",
        ),
        cfg.StrOpt(
            "ip_field",
            default="ip",
            help="Field in the JSON response containing the IP address (default: 'ip').",
        ),
    ]

    try:
        conf.register_opts(opts, group=group)
    except cfg.DuplicateOptError:
        pass

    # Optionally, set defaults here or rely on registered defaults
    conf["resolvers.json"].url = "https://api.ipify.org?format=json"
    conf["resolvers.json"].ip_field = "ip"

    yield


@pytest.fixture
def json_resolver_config():
    """Return the global 'resolvers.json' config group for use in tests."""
    return cfg.CONF["resolvers.json"]
