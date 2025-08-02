# dnswatch

**dnswatch** is a fully customizable, driver-based Dynamic DNS updater.
It periodically checks your public IP address and updates DNS records using pluggable resolver and updater drivers.

Built with [oslo.config](https://docs.openstack.org/oslo.config/latest/) and [oslo.log](https://docs.openstack.org/oslo.log/latest/) from the OpenStack ecosystem.

---

## Features

* Modular design with pluggable resolver and updater drivers
* Oslo-style config support (INI file + environment variables)
* Logging with `oslo.log`
* Supports JSON- or plain-text-based public IP resolvers
* OpenStack Designate integration out of the box

---

## Configuration

### Basic Setup

Your main configuration file should follow the `oslo_config` INI format.

In the `[DEFAULT]` section, you define:

* The resolver and updater drivers to use
* The update interval (in seconds)

Example:

```ini
[DEFAULT]
resolver = dnswatch.resolvers.json.JsonResolver
updater = dnswatch.updaters.noop.NoopUpdater
interval = 300
```

Each driver has its own config group, following the format `[resolvers.<name>]` or `[updaters.<name>]`.

---

## Driver System Overview

### Resolvers

Resolvers determine the current public IP address.

#### `default` resolver

* Expects a plain text response with only the IP address (e.g., from `https://api.ipify.org`)
* Configuration:

```ini
[resolvers.default]
url = https://api.ipify.org
```

#### `json` resolver

* Expects a JSON response and extracts the IP from a specific field.
* Useful for APIs like `https://api64.ipify.org?format=json`

Example response:

```json
{ "ip": "203.0.113.42" }
```

* Configuration:

```ini
[resolvers.json]
url = https://api64.ipify.org?format=json
ip_field = ip
```

---

### Updaters

Updaters handle the logic for updating DNS records.

#### `noop` updater

* No operation: logs the detected IP but performs no updates.
* Useful for testing resolver behavior.

```ini
[updaters.noop]
# No options required
```

#### `designate` updater

* Updates DNS records in an [OpenStack Designate](https://docs.openstack.org/designate/latest/) zone.

* Supports standard OpenStack authentication via:

  * `OS_CLOUD` (with `clouds.yaml`)
  * Full environment variables (`OS_AUTH_URL`, `OS_USERNAME`, etc.)

* Required configuration:

```ini
[updaters.designate]
zone_id = 8f06b1e2-1787-416f-9e73-acb3178acdd9
record_name = home.example.com.
record_type = A
ttl = 300
```

* Auth setup:
  Follow [OpenStack RC file guide](https://docs.openstack.org/ocata/user-guide/common/cli-set-environment-variables-using-openstack-rc.html)
  or use a `clouds.yaml` file with `OS_CLOUD=yourcloud`.

---

## Running

You can run `dnswatch` as a periodic service or one-shot script depending on how you configure its scheduler. Example entry point:

```bash
dnswatch --config-file /etc/dnswatch.conf
```

Logging will go to stderr by default but can be configured using `oslo.log`.

---

## Running in Docker

The Docker image does **not** include a default configuration file. To run `dnswatch` inside a container, you must mount your own config file at `/app/dnswatch.conf`.

The image includes a sample config file for reference, but it performs no updates by default.

Example Docker run command:

```bash
docker run --rm \
  -v /path/to/your/dnswatch.conf:/app/dnswatch.conf:ro \
  -v /path/to/openstack/clouds.yaml:/etc/openstack/clouds.yaml:ro \
  -e OS_CLOUD=cloud \
  ednxzu/dnswatch
```

Make sure to also mount any required credential files or environment variables (like OpenStack credentials) as needed by your updater driver.

---

## Extending

New resolvers or updaters can be implemented by subclassing:

* `dnswatch.resolvers.base.BaseResolver`
* `dnswatch.updaters.base.BaseUpdater`

Drivers are automatically discovered via the configured entry point name.

---

## License

MIT

---

## Contributions

Contributions welcome! Submit issues or pull requests via the Git repo.
