"""
Pytest configuration and fixtures for dnswatch tests.

Provides reusable pytest fixtures such as default_resolver_config
to setup configuration objects for testing resolver components.
"""

import pytest
from oslo_config import cfg


@pytest.fixture
def default_resolver_config():
    conf = cfg.ConfigOpts()
    conf.register_opts([cfg.StrOpt("url")], group="resolvers.default")
    conf.register_group(cfg.OptGroup("resolvers.default"))
    conf["resolvers.default"].url = "http://example.com"
    return conf["resolvers.default"]
