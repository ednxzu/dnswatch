"""NoopUpdater for dnswatch.

A dummy updater that simulates DNS updates by logging actions
without performing any real changes.
"""

import logging
from oslo_config import cfg
from dnswatch.updaters.base import BaseUpdater
from dnswatch.resolvers.default import DefaultResolver

LOG = logging.getLogger(__name__)
CONF = cfg.CONF


class NoopUpdater(BaseUpdater):
    """A no-operation updater for testing and dry runs.

    Uses the DefaultResolver to simulate the currently set IP and logs
    the update action without performing any actual DNS update.
    """

    def __init__(self, config):
        super().__init__(config)
        self.resolver = DefaultResolver(config=CONF["resolvers.default"])

    def get_current_ip(self) -> str:
        ip = self.resolver.get_ip()
        LOG.info("[noop] Simulated current DNS IP: %s", ip)
        return ip

    def update(self, ip: str):
        LOG.info("[noop] Pretending to update DNS record to IP: %s", ip)
