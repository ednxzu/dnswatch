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
        help="URL to fetch the public IP address from (default: https://icanhazip.com). This url should return the IP address as plain text.",
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
