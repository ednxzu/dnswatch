from unittest.mock import MagicMock, patch

import pytest

from dnswatch.updaters.noop.noop_updater import NoopUpdater


class TestNoopUpdater:
    @pytest.fixture
    def config_mock(self):
        return {}

    @patch("dnswatch.updaters.noop.noop_updater.CONF")
    @patch("dnswatch.updaters.noop.noop_updater.DefaultResolver")
    def test_init_creates_resolver(self, mock_resolver_cls, mock_conf, config_mock):
        mock_conf.__getitem__.return_value = {"url": "https://icanhazip.com"}

        updater = NoopUpdater(config_mock)

        mock_resolver_cls.assert_called_once_with(config=mock_conf.__getitem__.return_value)
        assert updater.resolver == mock_resolver_cls.return_value

    @patch("dnswatch.updaters.noop.noop_updater.CONF")
    @patch("dnswatch.updaters.noop.noop_updater.DefaultResolver")
    def test_get_current_ip_returns_ip_from_resolver(
        self, mock_resolver_cls, mock_conf, config_mock
    ):
        mock_conf.__getitem__.return_value = {"url": "https://icanhazip.com"}
        mock_resolver = MagicMock()
        mock_resolver.get_ip.return_value = "1.2.3.4"
        mock_resolver_cls.return_value = mock_resolver

        updater = NoopUpdater(config_mock)
        ip = updater.get_current_ip()

        assert ip == "1.2.3.4"
        mock_resolver.get_ip.assert_called_once()

    @patch("dnswatch.updaters.noop.noop_updater.CONF")
    @patch("dnswatch.updaters.noop.noop_updater.DefaultResolver")
    def test_update_does_nothing(self, mock_resolver_cls, mock_conf, config_mock):
        mock_conf.__getitem__.return_value = {"url": "https://icanhazip.com"}

        updater = NoopUpdater(config_mock)
        updater.update("5.6.7.8")
