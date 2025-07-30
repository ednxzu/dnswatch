import logging
from oslo_config import cfg
from dnswatch.updaters.base import BaseUpdater
from dnswatch.resolvers.default import DefaultResolver

LOG = logging.getLogger(__name__)
CONF = cfg.CONF


class NoopUpdater(BaseUpdater):
    def __init__(self, config):
        super().__init__(config)
        self.resolver = DefaultResolver(config=CONF["resolvers.default"])

    def get_current_ip(self) -> str:
        ip = self.resolver.get_ip()
        LOG.info(f"[noop] Simulated current DNS IP: {ip}")
        return ip

    def update(self, ip: str):
        LOG.info(f"[noop] Pretending to update DNS record to IP: {ip}")
