"""
No-op updater configuration options for dnswatch.

This updater performs no actual DNS updates and can be used for testing or debugging.
"""

from oslo_config import cfg

opts = [
    cfg.StrOpt(
        "noop_marker",
        default="noop",
        help="No-op marker; this updater performs no updates.",
    )
]

group = cfg.OptGroup("updaters.noop", title="Noop Updater Options")
