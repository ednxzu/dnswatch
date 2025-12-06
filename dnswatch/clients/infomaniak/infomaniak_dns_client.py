import os
from typing import Literal

import requests
from oslo_log import log as logging

LOG = logging.getLogger(__name__)


class InfomaniakDnsClient:
    def __init__(self, api_token: str | None = None):
        self.api_url = "https://api.infomaniak.com"
        self.api_token = api_token if api_token is not None else os.getenv("INFOMANIAK_API_TOKEN")
        if self.api_token is None:
            raise ValueError(
                "Infomaniak API token is required. "
                "Provide it via 'api_token' parameter or 'INFOMANIAK_API_TOKEN' ",
                "environment variable.",
            )

        self.api_headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }

    # NOTE(blanson): kwargs are standard requests.request arguments
    # default headers and timeout are injected.
    def _make_api_request(
        self,
        method: Literal["GET", "POST", "PATCH", "PUT", "DELETE"],
        route: str,
        **kwargs,
    ):
        ALLOWED_METHODS = {"GET", "POST", "PATCH", "PUT", "DELETE"}

        if method not in ALLOWED_METHODS:
            raise ValueError(f"Invalid method: {method}")

        endpoint_url = f"{self.api_url}/{route.lstrip('/')}"

        kwargs.setdefault("headers", self.api_headers)
        kwargs.setdefault("timeout", 10)

        try:
            query = requests.request(method=method, url=endpoint_url, **kwargs)
            query.raise_for_status()
            json_query = query.json()
            return json_query

        except requests.exceptions.Timeout:
            LOG.error("Request timed out on %s from %s", method, route)
            raise

        except requests.exceptions.HTTPError as e:
            status = e.response.status_code

            if status == 401:
                LOG.error("Invalid Infomaniak API token")
                raise ValueError("Invalid Infomaniak API token") from e
            elif status == 403:
                LOG.error("%s on %s: Permission denied", method, route)
                raise ValueError(f"No permission to send {method} to route {route}") from e
            elif status == 404:
                LOG.warning("Route %s not found with method %s", route, method)
            elif status == 429:
                LOG.error("Rate limited by Infomaniak API")
            else:
                LOG.error("HTTP %s error from Infomaniak API", status)
            raise

        except requests.exceptions.ConnectionError as e:
            LOG.error("Connection error to Infomaniak API: %s", e)
            raise

        except requests.exceptions.RequestException as e:
            LOG.error("Request error: %s", e)
            raise

    def _get_record_by_name(self, zone: str, record: str, record_type: str = "A") -> dict | None:
        method = "GET"
        route = f"2/zones/{zone}/records"
        query_params = {
            "filter[source]": record,
            "filter[types][]": record_type,
        }

        result = self._make_api_request(method=method, route=route, params=query_params)
        data = result.get("data", [])
        nb_results = len(data)

        if not nb_results:
            LOG.warning(
                "Did not find %s record for %s in zone %s",
                record_type,
                record,
                zone,
            )
            return None

        if nb_results > 1:
            LOG.warning("Multiple %s records found for %s, using first", record_type, record)

        return data[0]

    def create_record(
        self,
        zone: str,
        record: str,
        target: str,
        ttl: int = 3600,
        record_type: str = "A",
    ) -> dict:
        method = "POST"
        route = f"2/zones/{zone}/records"

        if not 60 <= ttl <= 86400:
            raise ValueError("The record's ttl must be between 60 and 86400")

        body = {"source": record, "target": target, "ttl": ttl, "type": record_type}

        result = self._make_api_request(method=method, route=route, json=body)
        if result.get("result") != "success":
            error = result.get("error", "Unknown error")
            raise ValueError(f"Failed to create record: {error}")

        data = result.get("data", {})
        LOG.info(
            "Created %s record '%s' → '%s' in zone %s (ID: %s)",
            record_type,
            record,
            target,
            zone,
            data.get("id"),
        )

        return data

    def get_record(self, zone: str, record: str, record_type: str = "A") -> dict | None:
        return self._get_record_by_name(zone, record, record_type)

    def update_record(
        self,
        zone: str,
        record_id: int,
        target: str | None = None,
        ttl: int | None = None,
        record_type: str | None = None,
    ):
        method = "PUT"
        route = f"2/zones/{zone}/records/{record_id}"
        body = {}

        if ttl is not None:
            if not 60 <= ttl <= 86400:
                raise ValueError("The record's ttl must be between 60 and 86400")
            body["ttl"] = ttl

        if target is not None:
            body["target"] = target

        if record_type is not None:
            body["type"] = record_type

        if not body:
            raise ValueError(
                "Must provide at least one field to update (target, ttl, or record_type)"
            )

        result = self._make_api_request(method=method, route=route, json=body)
        if result.get("result") != "success":
            error = result.get("error", "Unknown error")
            raise ValueError(f"Failed to update record: {error}")

        data = result.get("data", {})
        LOG.info(
            "Updated record ID %s in zone %s (fields: %s)", record_id, zone, ", ".join(body.keys())
        )

        return data
