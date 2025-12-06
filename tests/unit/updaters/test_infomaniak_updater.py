from unittest.mock import MagicMock, patch

import pytest

from dnswatch.updaters.infomaniak.infomaniak_updater import InfomaniakUpdater


class TestInfomaniakUpdater:
    @pytest.fixture
    def config_mock(self):
        class Config:
            zone = "example.com"
            record_name = "test"
            record_type = "A"
            ttl = 300

        return Config()

    @patch("dnswatch.updaters.infomaniak.infomaniak_updater.InfomaniakDnsClient")
    def test_init_stores_config_values(self, mock_client_cls, config_mock):
        updater = InfomaniakUpdater(config_mock)

        assert updater.zone == "example.com"
        assert updater.record_name == "test"
        assert updater.record_type == "A"
        assert updater.ttl == 300
        mock_client_cls.assert_called_once()

    @patch("dnswatch.updaters.infomaniak.infomaniak_updater.InfomaniakDnsClient")
    def test_init_creates_client(self, mock_client_cls, config_mock):
        mock_client = MagicMock()
        mock_client_cls.return_value = mock_client

        updater = InfomaniakUpdater(config_mock)

        assert updater.client == mock_client
        mock_client_cls.assert_called_once_with()

    @patch("dnswatch.updaters.infomaniak.infomaniak_updater.InfomaniakDnsClient")
    def test_get_current_ip_returns_ip_when_record_exists(self, mock_client_cls, config_mock):
        mock_client = MagicMock()
        mock_client.get_record.return_value = {
            "id": 12345,
            "source": "test",
            "target": "1.2.3.4",
            "type": "A",
            "ttl": 300,
        }
        mock_client_cls.return_value = mock_client

        updater = InfomaniakUpdater(config_mock)
        ip = updater.get_current_ip()

        assert ip == "1.2.3.4"
        mock_client.get_record.assert_called_once_with(
            zone="example.com", record="test", record_type="A"
        )

    @patch("dnswatch.updaters.infomaniak.infomaniak_updater.InfomaniakDnsClient")
    def test_get_current_ip_returns_none_when_record_not_found(self, mock_client_cls, config_mock):
        mock_client = MagicMock()
        mock_client.get_record.return_value = None
        mock_client_cls.return_value = mock_client

        updater = InfomaniakUpdater(config_mock)
        ip = updater.get_current_ip()

        assert ip is None
        mock_client.get_record.assert_called_once_with(
            zone="example.com", record="test", record_type="A"
        )

    @patch("dnswatch.updaters.infomaniak.infomaniak_updater.InfomaniakDnsClient")
    def test_get_current_ip_returns_none_when_target_missing(self, mock_client_cls, config_mock):
        mock_client = MagicMock()
        mock_client.get_record.return_value = {
            "id": 12345,
            "source": "test",
            "type": "A",
        }
        mock_client_cls.return_value = mock_client

        updater = InfomaniakUpdater(config_mock)
        ip = updater.get_current_ip()

        assert ip is None

    @patch("dnswatch.updaters.infomaniak.infomaniak_updater.InfomaniakDnsClient")
    def test_update_existing_record(self, mock_client_cls, config_mock):
        mock_client = MagicMock()
        mock_client.get_record.return_value = {
            "id": 12345,
            "source": "test",
            "target": "1.2.3.4",
            "type": "A",
            "ttl": 300,
        }
        mock_client_cls.return_value = mock_client

        updater = InfomaniakUpdater(config_mock)
        updater.update("5.6.7.8")

        mock_client.get_record.assert_called_once_with(
            zone="example.com", record="test", record_type="A"
        )
        mock_client.update_record.assert_called_once_with(
            zone="example.com",
            record_id=12345,
            target="5.6.7.8",
            ttl=300,
            record_type="A",
        )
        mock_client.create_record.assert_not_called()

    @patch("dnswatch.updaters.infomaniak.infomaniak_updater.InfomaniakDnsClient")
    def test_update_uses_config_ttl(self, mock_client_cls, config_mock):
        config_mock.ttl = 600
        mock_client = MagicMock()
        mock_client.get_record.return_value = {
            "id": 12345,
            "source": "test",
            "target": "1.2.3.4",
            "type": "A",
            "ttl": 300,
        }
        mock_client_cls.return_value = mock_client

        updater = InfomaniakUpdater(config_mock)
        updater.update("5.6.7.8")

        mock_client.update_record.assert_called_once_with(
            zone="example.com",
            record_id=12345,
            target="5.6.7.8",
            ttl=600,
            record_type="A",
        )

    @patch("dnswatch.updaters.infomaniak.infomaniak_updater.InfomaniakDnsClient")
    def test_update_uses_config_record_type(self, mock_client_cls, config_mock):
        config_mock.record_type = "AAAA"
        mock_client = MagicMock()
        mock_client.get_record.return_value = {
            "id": 12345,
            "source": "test",
            "target": "2001:db8::1",
            "type": "AAAA",
            "ttl": 300,
        }
        mock_client_cls.return_value = mock_client

        updater = InfomaniakUpdater(config_mock)
        updater.update("2001:db8::2")

        mock_client.get_record.assert_called_once_with(
            zone="example.com", record="test", record_type="AAAA"
        )
        mock_client.update_record.assert_called_once_with(
            zone="example.com",
            record_id=12345,
            target="2001:db8::2",
            ttl=300,
            record_type="AAAA",
        )

    @patch("dnswatch.updaters.infomaniak.infomaniak_updater.InfomaniakDnsClient")
    def test_update_creates_new_record_when_not_found(self, mock_client_cls, config_mock):
        mock_client = MagicMock()
        mock_client.get_record.return_value = None
        mock_client_cls.return_value = mock_client

        updater = InfomaniakUpdater(config_mock)
        updater.update("5.6.7.8")

        mock_client.get_record.assert_called_once_with(
            zone="example.com", record="test", record_type="A"
        )
        mock_client.create_record.assert_called_once_with(
            zone="example.com",
            record="test",
            target="5.6.7.8",
            ttl=300,
            record_type="A",
        )
        mock_client.update_record.assert_not_called()

    @patch("dnswatch.updaters.infomaniak.infomaniak_updater.InfomaniakDnsClient")
    def test_update_create_uses_all_config_params(self, mock_client_cls, config_mock):
        config_mock.zone = "test.com"
        config_mock.record_name = "api"
        config_mock.record_type = "AAAA"
        config_mock.ttl = 600

        mock_client = MagicMock()
        mock_client.get_record.return_value = None
        mock_client_cls.return_value = mock_client

        updater = InfomaniakUpdater(config_mock)
        updater.update("2001:db8::1")

        mock_client.create_record.assert_called_once_with(
            zone="test.com",
            record="api",
            target="2001:db8::1",
            ttl=600,
            record_type="AAAA",
        )

    @patch("dnswatch.updaters.infomaniak.infomaniak_updater.InfomaniakDnsClient")
    def test_update_handles_record_with_missing_id(self, mock_client_cls, config_mock):
        mock_client = MagicMock()
        mock_client.get_record.return_value = {
            "source": "test",
            "target": "1.2.3.4",
            "type": "A",
        }
        mock_client_cls.return_value = mock_client

        updater = InfomaniakUpdater(config_mock)
        updater.update("5.6.7.8")

        mock_client.update_record.assert_called_once_with(
            zone="example.com",
            record_id=None,  # .get("id") returns None
            target="5.6.7.8",
            ttl=300,
            record_type="A",
        )
