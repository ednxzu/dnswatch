import logging

from oslo_config import cfg

from dnswatch.resolvers.default import DefaultResolver
from dnswatch.updaters.base import BaseUpdater

LOG = logging.getLogger(__name__)
CONF = cfg.CONF


class NoopUpdater(BaseUpdater):
    def __init__(self, config):
        super().__init__(config)
        self.resolver = DefaultResolver(config=CONF["resolvers.default"])

    def get_current_ip(self) -> str:
        ip = self.resolver.get_ip()
        LOG.info("[noop] Simulated current DNS IP: %s", ip)
        return ip

    def update(self, ip: str):
        LOG.info("[noop] Pretending to update DNS record to IP: %s", ip)
