"""
Default resolver configuration options for dnswatch.

Defines the URL endpoint to fetch the public IP address.
The URL must return a plain-text IP.
"""

from oslo_config import cfg

opts = [
    cfg.StrOpt(
        "url",
        default="https://icanhazip.com",
        help=(
            "URL to fetch the public IP address. "
            "Must return a plain-text IP (default: https://icanhazip.com)."
        ),
    )
]

group = cfg.OptGroup("resolvers.default", title="Default Resolver Options")
