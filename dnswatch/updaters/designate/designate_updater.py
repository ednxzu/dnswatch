"""OpenStack Designate updater driver.

This updater manages DNS recordsets in OpenStack Designate,
allowing querying and updating of DNS records.
"""

from dnswatch.updaters.base import BaseUpdater
from openstack import connection
from openstack.dns.v2 import recordset as _rs
from oslo_log import log as logging

LOG = logging.getLogger(__name__)


class OpenStackDesignateUpdater(BaseUpdater):
    """Updater that manages DNS records using OpenStack Designate."""

    def __init__(self, config):
        super().__init__(config)
        self.zone_id = config.zone_id
        self.record_name = config.record_name
        self.record_type = config.record_type
        self.ttl = config.ttl

        self.conn = connection.from_config()

        # Normalize record name to a fully qualified domain name (FQDN)
        if not self.record_name.endswith("."):
            zone = self.conn.dns.get_zone(self.zone_id)
            zone_name = zone.name
            if not zone_name.endswith("."):
                zone_name += "."
            self.record_name = f"{self.record_name}.{zone_name}"
            LOG.debug(
                "[designate] Normalized record name to FQDN: %s", self.record_name
            )

    def get_current_ip(self) -> str | None:
        """Return the current IP set in the Designate record, or None if not found."""
        LOG.debug("[designate] Fetching record from Designate")

        record = self.conn.dns.find_recordset(
            name_or_id=self.record_name,
            zone=self.zone_id,
            type=self.record_type,
            ignore_missing=True,
        )

        if record and record.records:
            LOG.debug(
                "[designate] Found record: %s with IPs: %s",
                record.id,
                record.records,
            )
            return record.records[0]

        LOG.debug("[designate] Recordset for %s not found", self.record_name)
        return None

    def update(self, ip: str):
        """Update or create the DNS recordset with the given IP."""
        LOG.debug("[designate] Updating record %s to %s", self.record_name, ip)

        record = self.conn.dns.find_recordset(
            name_or_id=self.record_name,
            zone=self.zone_id,
            type=self.record_type,
            ignore_missing=True,
        )

        if record:
            LOG.info("[designate] Updating existing recordset: %s", record.id)
            record_to_update = _rs.Recordset(
                id=record.id,
                zone_id=self.zone_id,
                records=[ip],
                ttl=self.ttl,
            )
            self.conn.dns.update_recordset(record_to_update)
        else:
            LOG.info(
                "[designate] Creating new recordset for %s with ip %s",
                self.record_name,
                ip,
            )
            self.conn.dns.create_recordset(
                self.zone_id,
                name=self.record_name,
                type=self.record_type,
                records=[ip],
                ttl=self.ttl,
            )
