"""JSON Resolver module for dnswatch
This module implements a resolver that fetches the public IP address
from a specified JSON endpoint.
"""

import requests
import ipaddress
from oslo_log import log as logging
from dnswatch.resolvers.base import BaseResolver

LOG = logging.getLogger(__name__)


class JsonResolver(BaseResolver):
    """Resolves the public IP address from a JSON response."""

    def __init__(self, config):
        super().__init__(config)
        self.url = config.url
        self.ip_field = config.ip_field
        LOG.debug(
            "[json resolver] Initialized with URL: %s and IP field: %s",
            self.url,
            self.ip_field,
        )

    def get_ip(self) -> str:
        try:
            LOG.debug("[json resolver] Fetching IP from %s", self.url)
            response = requests.get(self.url, timeout=5)
            response.raise_for_status()
            data = response.json()
            ip = data.get(self.ip_field)
            if not ip:
                raise ValueError(f"IP field '{self.ip_field}' not found in response")
            try:
                ipaddress.ip_address(ip)
            except ValueError as exc:
                LOG.error("[json resolver] Invalid IP format: '%s'", ip)
                raise ValueError("Invalid IP address received: '{ip}'") from exc

            LOG.debug("[json resolver] Received valid IP: %s", ip)
            return ip
        except Exception:
            LOG.exception("[default resolver] Failed to get IP from %s", self.url)
            raise
