"""Configuration definitions for dnswatch components.

This module defines global and per-driver configuration options
using oslo.config.
"""

from oslo_config import cfg

CONF = cfg.CONF

default_opts = [
    cfg.StrOpt("resolver_driver", default="dnswatch.resolvers.default.DefaultResolver"),
    cfg.StrOpt("updater_driver", default="dnswatch.updaters.noop.NoopUpdater"),
    cfg.IntOpt("interval", default=300),
]
CONF.register_opts(default_opts)

resolvers_default_opts = [
    cfg.StrOpt(
        "url",
        default="https://icanhazip.com",
        help=(
            "URL to fetch the public IP address from (default: https://icanhazip.com). "
            "This URL should return the IP address as plain text."
        ),
    ),
]
CONF.register_opts(resolvers_default_opts, group="resolvers.default")

resolver_json_opts = [
    cfg.StrOpt(
        "url",
        default="https://api.ipify.org?format=json",
        help=(
            "URL to fetch the public IP address from (default: https://api.ipify.org?format=json). "
            "This URL should return a JSON object with the IP address as a field."
        ),
    ),
    cfg.StrOpt(
        "ip_field",
        default="ip",
        help=(
            "Field in the JSON response that contains the public IP address (default: 'ip'). "
            "This should match the key in the JSON object returned by the URL."
        ),
    ),
]
CONF.register_opts(resolver_json_opts, group="resolvers.json")

updaters_noop_opts = [
    cfg.StrOpt(
        "noop_marker",
        default="noop",
        help="Placeholder option; this driver takes no configuration.",
    )
]
CONF.register_opts(updaters_noop_opts, group="updaters.noop")

updaters_designate_opts = [
    cfg.StrOpt("zone_id", help="Designate zone ID to update"),
    cfg.StrOpt("record_name", help="DNS record name to update"),
    cfg.StrOpt("record_type", default="A", help="Record type (A, AAAA, etc.)"),
    cfg.IntOpt("ttl", default=300, help="TTL for the record"),
]
CONF.register_opts(updaters_designate_opts, group="updaters.designate")
