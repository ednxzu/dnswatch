import time

from oslo_config import cfg
from oslo_log import log as logging

from dnswatch import log
from dnswatch.config import register_opts
from dnswatch.utils import get_version, infer_group, load_driver

CONF = cfg.CONF
LOG = logging.getLogger("dnswatch")


def main():
    register_opts(CONF)

    logging.register_options(CONF)
    CONF(project="dnswatch")
    log.setup(CONF)

    LOG.info("Starting dnswatch version %s", get_version())

    resolver_group = infer_group(CONF.resolver_driver)
    updater_group = infer_group(CONF.updater_driver)

    resolver = load_driver(CONF.resolver_driver, CONF[resolver_group])
    updater = load_driver(CONF.updater_driver, CONF[updater_group])

    LOG.info("Using resolver: %s", CONF.resolver_driver)
    LOG.info("Using updater: %s", CONF.updater_driver)
    LOG.info("Update interval: %s seconds", CONF.interval)

    while True:
        try:
            current_ip = updater.get_current_ip()
            LOG.debug("Current IP: %s", current_ip)
            new_ip = resolver.get_ip()
            if new_ip != current_ip:
                updater.update(new_ip)
                LOG.info("IP changed: %s -> %s", current_ip, new_ip)
            else:
                LOG.debug("IP unchanged")
        except Exception as exc:
            LOG.error("Error during update cycle: %s", exc, exc_info=True)

        time.sleep(CONF.interval)
