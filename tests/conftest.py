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
