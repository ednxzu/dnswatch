import time
from oslo_config import cfg
from oslo_log import log as logging

from dnswatch import config, log

from dnswatch.utils import load_driver, infer_group

CONF = cfg.CONF
LOG = logging.getLogger(__name__, "dnswatch")


def main():
    logging.register_options(CONF)
    CONF(project="dnswatch")
    log.setup(CONF)

    LOG.info("dnswatch is starting up")

    resolver_group = infer_group(CONF.resolver_driver)
    updater_group = infer_group(CONF.updater_driver)

    # Load driver (calls register_opts internally)
    resolver = load_driver(CONF.resolver_driver, CONF[resolver_group])
    updater = load_driver(CONF.updater_driver, CONF[updater_group])

    LOG.info(f"Using resolver: {CONF.resolver_driver}")
    LOG.info(f"Update interval: {CONF.interval} seconds")

    while True:
        try:
            current_ip = updater.get_current_ip()
            LOG.debug(f"Current IP: {current_ip}")
            new_ip = resolver.get_ip()
            if new_ip != current_ip:
                LOG.info(f"IP changed: {current_ip} -> {new_ip}")
                current_ip = new_ip
            else:
                LOG.debug("IP unchanged")
        except Exception as e:
            LOG.error(f"Error during update cycle: {e}", exc_info=True)

        time.sleep(CONF.interval)
