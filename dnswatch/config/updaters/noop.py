from oslo_config import cfg

opts = [
    cfg.StrOpt(
        "noop_marker",
        default="noop",
        help="No-op marker; this updater performs no updates.",
    )
]
