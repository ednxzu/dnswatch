from oslo_config import cfg

opts = [
    cfg.StrOpt(
        "zone",
        help=("Infomaniak DNS zone name to update. Example: example.com"),
    ),
    cfg.StrOpt(
        "record_name",
        help=(
            "DNS record name to update, without the zone prefix. "
            "Example: to update test.example.com in zone example.com, value is 'test'"
        ),
    ),
    cfg.StrOpt(
        "record_type",
        default="A",
        help="DNS record type (A, AAAA, etc.).",
    ),
    cfg.IntOpt(
        "ttl",
        default=300,
        help=("TTL (time-to-live) for the DNS record. Must be between 60 and 86400."),
    ),
]
