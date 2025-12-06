# dnswatch Tests

This directory contains the test suite for dnswatch, organized into unit and integration tests.

## Structure

```
tests/
├── conftest.py                    # Shared pytest fixtures
├── unit/                          # Unit tests (mocked, fast)
│   ├── resolvers/                 # Resolver tests
│   │   ├── test_default_resolver.py
│   │   └── test_json_resolver.py
│   ├── updaters/                  # Updater tests
│   │   ├── test_noop_updater.py
│   │   └── test_designate_updater.py
│   └── clients/                   # Client tests
│       └── test_infomaniak_client.py
└── integration/                   # Integration tests (real APIs)
    └── test_infomaniak_client.py
```

## Running Tests

### Run all unit tests (fast, no external dependencies)
```bash
uv run pytest tests/unit -v
```

### Run specific test file
```bash
uv run pytest tests/unit/clients/test_infomaniak_client.py -v
```

### Run specific test class
```bash
uv run pytest tests/unit/clients/test_infomaniak_client.py::TestInfomaniakDnsClient -v
```

### Run specific test
```bash
uv run pytest tests/unit/clients/test_infomaniak_client.py::TestInfomaniakDnsClient::test_get_record_success -v
```

### Run integration tests (requires API tokens)
```bash
export INFOMANIAK_API_TOKEN="your-token-here"

uv run pytest tests/integration -v -s
```

### Run all tests
```bash
uv run pytest tests/ -v
```

## Test Categories

### Unit Tests
- **Location**: `tests/unit/`
- **Purpose**: Test individual components in isolation with mocked dependencies
- **Speed**: Fast (< 1 second)
- **Dependencies**: None (all external calls mocked)
- **When to run**: Always, in CI/CD, pre-commit

### Integration Tests
- **Location**: `tests/integration/`
- **Purpose**: Test real API interactions
- **Speed**: Slower (network calls)
- **Dependencies**: Requires API tokens and network access
- **When to run**: Manually, before releases
- **Note**: Automatically skipped if required environment variables are not set

## Writing Tests

### Unit Test Example

```python
class TestMyComponent:
    """Unit tests for MyComponent."""

    def test_something_success(self):
        component = MyComponent()

        result = component.do_something()

        assert result == expected_value
```

### Integration Test Example

```python
@pytest.mark.skipif(
    not os.getenv('SOME_API_TOKEN'),
    reason="SOME_API_TOKEN not set"
)
class TestMyClientIntegration:
    def test_real_api_call(self):
        client = MyClient()
        result = client.call_api()
        assert result is not None
```

## Coverage

To run tests with coverage:

```bash
uv run coverage run -m pytest tests/unit -v
uv run coverage report -m --omit="tests/*"
```

## Continuous Integration

Unit tests run automatically in CI/CD pipelines. Integration tests are skipped unless
API tokens are explicitly configured in the CI environment.
