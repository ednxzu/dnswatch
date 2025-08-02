"""
Unit tests for the OpenStackDesignateUpdater class.
"""

import pytest
from unittest.mock import MagicMock, patch
from openstack.dns.v2 import recordset as _rs
from dnswatch.updaters.designate import OpenStackDesignateUpdater


@pytest.fixture
def config_mock():
    # Simple mock config object with necessary attributes
    class Config:
        zone_id = "zone-1234"
        record_name = "myhost"
        record_type = "A"
        ttl = 60

    return Config()


@pytest.fixture
def conn_mock():
    # Mock connection object with dns attribute mocked
    conn = MagicMock()
    conn.dns.get_zone.return_value = MagicMock(name="Zone", spec=["name"])
    conn.dns.get_zone.return_value.name = "example.com"

    return conn


@patch("openstack.connection.from_config")
def test_normalizes_record_name(
    from_config_mock, config_mock, conn_mock  # pylint: disable=redefined-outer-name
):
    from_config_mock.return_value = conn_mock

    updater = OpenStackDesignateUpdater(config_mock)

    # The record_name should be normalized to FQDN: myhost.example.com.
    assert updater.record_name == "myhost.example.com."
    conn_mock.dns.get_zone.assert_called_once_with("zone-1234")


@patch("openstack.connection.from_config")
def test_get_current_ip_returns_ip(
    from_config_mock, config_mock, conn_mock  # pylint: disable=redefined-outer-name
):
    from_config_mock.return_value = conn_mock

    # Setup find_recordset to return a mock recordset with records
    mock_recordset = MagicMock()
    mock_recordset.id = "record-5678"
    mock_recordset.records = ["1.2.3.4"]
    conn_mock.dns.find_recordset.return_value = mock_recordset

    updater = OpenStackDesignateUpdater(config_mock)
    ip = updater.get_current_ip()

    assert ip == "1.2.3.4"
    conn_mock.dns.find_recordset.assert_called_once_with(
        name_or_id=updater.record_name,
        zone=config_mock.zone_id,
        type=config_mock.record_type,
        ignore_missing=True,
    )


@patch("openstack.connection.from_config")
def test_get_current_ip_returns_none_when_no_record(
    from_config_mock, config_mock, conn_mock  # pylint: disable=redefined-outer-name
):
    from_config_mock.return_value = conn_mock

    conn_mock.dns.find_recordset.return_value = None

    updater = OpenStackDesignateUpdater(config_mock)
    ip = updater.get_current_ip()

    assert ip is None


@patch("openstack.connection.from_config")
def test_update_existing_recordset(
    from_config_mock, config_mock, conn_mock  # pylint: disable=redefined-outer-name
):
    from_config_mock.return_value = conn_mock

    mock_recordset = MagicMock()
    mock_recordset.id = "record-5678"
    mock_recordset.records = ["1.2.3.4"]
    conn_mock.dns.find_recordset.return_value = mock_recordset

    updater = OpenStackDesignateUpdater(config_mock)
    updater.update("5.6.7.8")

    conn_mock.dns.update_recordset.assert_called_once()
    updated_recordset = conn_mock.dns.update_recordset.call_args.args[0]

    assert isinstance(updated_recordset, _rs.Recordset)
    assert updated_recordset.id == mock_recordset.id
    assert updated_recordset.zone_id == config_mock.zone_id
    assert updated_recordset.records == ["5.6.7.8"]
    assert updated_recordset.ttl == config_mock.ttl

    conn_mock.dns.create_recordset.assert_not_called()


@patch("openstack.connection.from_config")
def test_create_recordset_if_not_found(
    from_config_mock, config_mock, conn_mock  # pylint: disable=redefined-outer-name
):
    from_config_mock.return_value = conn_mock

    conn_mock.dns.find_recordset.return_value = None

    updater = OpenStackDesignateUpdater(config_mock)
    updater.update("5.6.7.8")

    conn_mock.dns.create_recordset.assert_called_once_with(
        config_mock.zone_id,
        name=updater.record_name,
        type=config_mock.record_type,
        records=["5.6.7.8"],
        ttl=config_mock.ttl,
    )
    conn_mock.dns.update_recordset.assert_not_called()
