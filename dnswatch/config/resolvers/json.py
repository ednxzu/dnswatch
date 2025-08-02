"""
JSON resolver configuration options for dnswatch.

Defines the URL endpoint to fetch the public IP address in JSON format,
and the JSON field name where the IP address is located.
"""

from oslo_config import cfg

opts = [
    cfg.StrOpt(
        "url",
        default="https://api.ipify.org?format=json",
        help=(
            "URL to fetch the public IP address as JSON "
            "(default: https://api.ipify.org?format=json)."
        ),
    ),
    cfg.StrOpt(
        "ip_field",
        default="ip",
        help=(
            "Field name in the JSON response containing the IP address "
            "(default: 'ip')."
        ),
    ),
]

group = cfg.OptGroup("resolvers.json", title="JSON Resolver Options")
