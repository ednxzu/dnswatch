"""
Default configuration options for dnswatch.

Includes default resolver/updater drivers and
the update interval setting.
"""

from oslo_config import cfg

opts = [
    cfg.StrOpt(
        "resolver_driver",
        default="dnswatch.resolvers.default.DefaultResolver",
        help="The import path of the resolver driver to use. "
        "For example: 'dnswatch.resolvers.default.DefaultResolver' or "
        "'dnswatch.resolvers.json.JsonResolver'.",
    ),
    cfg.StrOpt(
        "updater_driver",
        default="dnswatch.updaters.noop.NoopUpdater",
        help="The import path of the updater driver to use. "
        "For example: 'dnswatch.updaters.noop.NoopUpdater' or "
        "'dnswatch.updaters.designate.DesignateUpdater'.",
    ),
    cfg.IntOpt(
        "interval",
        default=300,
        help="Time in seconds between periodic IP resolution and DNS update runs.",
    ),
]
