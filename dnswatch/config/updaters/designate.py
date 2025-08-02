"""
Designate updater configuration options for dnswatch.

Configuration for interacting with OpenStack Designate DNS service,
including zone ID, DNS record details, and TTL settings.
"""

from oslo_config import cfg

opts = [
    cfg.StrOpt(
        "zone_id",
        help="OpenStack Designate Zone ID to update.",
    ),
    cfg.StrOpt(
        "record_name",
        help="DNS record name to update.",
    ),
    cfg.StrOpt(
        "record_type",
        default="A",
        help="DNS record type (A, AAAA, etc.).",
    ),
    cfg.IntOpt(
        "ttl",
        default=300,
        help="TTL (time-to-live) for the DNS record.",
    ),
]

group = cfg.OptGroup("updaters.designate", title="Designate Updater Options")
