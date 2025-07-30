from oslo_log import log as logging

LOG = logging.getLogger(__name__)


def setup(conf):
    logging.setup(conf, "dnswatch")
