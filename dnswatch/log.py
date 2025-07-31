"""Logging setup for the dnswatch application.

This module configures oslo.log and provides a shared logger instance.
"""

from oslo_log import log as logging

LOG = logging.getLogger(__name__)


def setup(conf):
    """Configure oslo.log with the given configuration."""
    logging.setup(conf, "dnswatch")
