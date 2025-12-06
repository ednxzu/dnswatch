"""
Unit tests for the NoopUpdater updater class in dnswatch.
"""

from unittest.mock import MagicMock, patch

import pytest

from dnswatch.updaters.noop.noop_updater import NoopUpdater


class TestNoopUpdater:
    """Unit tests for NoopUpdater."""

    @pytest.fixture
    def noop_config(self):
        """Provide empty config for NoopUpdater."""
        return {}

    @patch("dnswatch.updaters.noop.noop_updater.DefaultResolver")
    @patch("dnswatch.updaters.noop.noop_updater.LOG")
    def test_get_current_ip_logs_and_returns_ip(self, mock_log, mock_resolver_cls, noop_config):
        """Test that get_current_ip returns IP and logs appropriately."""
        mock_resolver = MagicMock()
        mock_resolver.get_ip.return_value = "1.2.3.4"
        mock_resolver_cls.return_value = mock_resolver

        updater = NoopUpdater(noop_config)
        ip = updater.get_current_ip()

        mock_resolver.get_ip.assert_called_once()
        assert ip == "1.2.3.4"
        mock_log.info.assert_called_with("[noop] Simulated current DNS IP: %s", "1.2.3.4")

    @patch("dnswatch.updaters.noop.noop_updater.LOG")
    def test_update_logs_ip(self, mock_log, noop_config):
        """Test that update logs the new IP."""
        updater = NoopUpdater(noop_config)
        updater.update("5.6.7.8")
        mock_log.info.assert_called_with(
            "[noop] Pretending to update DNS record to IP: %s", "5.6.7.8"
        )
