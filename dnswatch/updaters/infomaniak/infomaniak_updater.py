from oslo_log import log as logging

from dnswatch.clients.infomaniak.infomaniak_dns_client import InfomaniakDnsClient
from dnswatch.updaters.base import BaseUpdater

LOG = logging.getLogger(__name__)


class InfomaniakUpdater(BaseUpdater):
    def __init__(self, config):
        super().__init__(config)
        self.zone = config.zone
        self.record_name = config.record_name
        self.record_type = config.record_type
        self.ttl = config.ttl
        self.client = InfomaniakDnsClient()

    def get_current_ip(self) -> str | None:
        LOG.debug("[infomaniak] Fetching record from Infomaniak API")

        record = self.client.get_record(
            zone=self.zone, record=self.record_name, record_type=self.record_type
        )

        if record:
            ip_addr = record.get("target")
            LOG.debug(
                "[infomaniak] Found record for %s in %s with IP: %s",
                self.record_name,
                self.zone,
                ip_addr,
            )
            return ip_addr

        return None

    def update(self, ip: str):
        LOG.debug("[infomaniak] Updating record %s in %s to %s", self.record_name, self.zone, ip)

        record = self.client.get_record(
            zone=self.zone, record=self.record_name, record_type=self.record_type
        )

        if record:
            record_id = record.get("id")
            LOG.info(
                "[infomaniak] Updating existing record: %s with id %s", self.record_name, record_id
            )
            self.client.update_record(
                zone=self.zone,
                record_id=record_id,
                target=ip,
                ttl=self.ttl,
                record_type=self.record_type,
            )
        else:
            LOG.info(
                "[infomaniak] Creating new record for %s in zone %s with ip %s",
                self.record_name,
                self.zone,
                ip,
            )
            self.client.create_record(
                zone=self.zone,
                record=self.record_name,
                target=ip,
                ttl=self.ttl,
                record_type=self.record_type,
            )
