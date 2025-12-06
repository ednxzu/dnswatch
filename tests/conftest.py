import pytest
from oslo_config import cfg


@pytest.fixture(scope="session", autouse=True)
def setup_resolvers_default_group():
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
    return cfg.CONF["resolvers.default"]


@pytest.fixture(scope="session", autouse=True)
def setup_resolvers_json_group():
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

    conf["resolvers.json"].url = "https://api.ipify.org?format=json"
    conf["resolvers.json"].ip_field = "ip"

    yield


@pytest.fixture
def json_resolver_config():
    return cfg.CONF["resolvers.json"]
