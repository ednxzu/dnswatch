"""Default IP resolver using a configurable HTTP endpoint."""

import requests
import ipaddress
from oslo_log import log as logging
from dnswatch.resolvers.base import BaseResolver
from dnswatch.log import LOG

LOG = logging.getLogger(__name__)


class DefaultResolver(BaseResolver):
    """Resolves the public IP address from a remote URL."""

    def __init__(self, config):
        super().__init__(config)
        self.url = config.url
        LOG.debug(f"[default resolver] Initialized with URL: {self.url}")

    def get_ip(self) -> str:
        LOG.debug(f"[default resolver] Fetching IP from {self.url}")
        try:
            response = requests.get(self.url, timeout=5)
            response.raise_for_status()
            ip = response.text.strip()

            try:
                ipaddress.ip_address(ip)
            except ValueError as exc:
                LOG.error(f"[default resolver] Invalid IP format: '{ip}'")
                raise ValueError(f"Invalid IP address received: '{ip}'") from exc

            LOG.debug(f"[default resolver] Received valid IP: {ip}")
            return ip
        except Exception:
            LOG.exception(f"[default resolver] Failed to get IP from {self.url}")
            raise
