"""Main entry point for the dnswatch application.

Initializes configuration and logging, loads resolver and updater drivers,
and runs the main loop to detect and apply public IP changes.
"""

import time
from oslo_config import cfg
from oslo_log import log as logging

from dnswatch import config, log  # pylint: disable=unused-import
from dnswatch.utils import load_driver, infer_group, get_version

CONF = cfg.CONF
LOG = logging.getLogger(__name__, "dnswatch")


def main():
    """Run the dnswatch daemon loop."""
    logging.register_options(CONF)
    CONF(project="dnswatch")
    log.setup(CONF)

    LOG.info("Starting dnswatch version %s", get_version())

    resolver_group = infer_group(CONF.resolver_driver)
    updater_group = infer_group(CONF.updater_driver)

    resolver = load_driver(CONF.resolver_driver, CONF[resolver_group])
    updater = load_driver(CONF.updater_driver, CONF[updater_group])

    LOG.info("Using resolver: %s", CONF.resolver_driver)
    LOG.info("Update interval: %s seconds", CONF.interval)

    while True:
        try:
            current_ip = updater.get_current_ip()
            LOG.debug(f"Current IP: {current_ip}")
            new_ip = resolver.get_ip()
            if new_ip != current_ip:
                updater.update(new_ip)
                LOG.info(f"IP changed: {current_ip} -> {new_ip}")
                current_ip = new_ip
            else:
                LOG.debug("IP unchanged")
        except Exception as exc:  # pylint: disable=broad-exception-caught
            LOG.error("Error during update cycle: %s", exc, exc_info=True)

        time.sleep(CONF.interval)
