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
            "URL to fetch the public IP address from "
            "(default: https://icanhazip.com). This URL should return the IP address as plain text."
        ),
    ),
]
CONF.register_opts(resolvers_default_opts, group="resolvers.default")

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
