from oslo_log import log as logging
import requests
from dnswatch.resolvers.base import BaseResolver
from dnswatch.log import LOG

LOG = logging.getLogger(__name__)


class DefaultResolver(BaseResolver):
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
            LOG.debug(f"[default resolver] Received IP: {ip}")
            return ip
        except Exception as e:
            LOG.exception(f"[default resolver] Failed to get IP from {self.url}")
            raise
