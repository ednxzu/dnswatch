from importlib import import_module

VERSION = "0.2.0"


def load_driver(import_path, config) -> object:
    module_path, class_name = import_path.rsplit(".", 1)
    module = import_module(module_path)

    driver_cls = getattr(module, class_name)
    return driver_cls(config)


def infer_group(driver_path) -> str:
    if not driver_path.startswith("dnswatch."):
        raise ValueError(f"Expected driver path to start with 'dnswatch.': {driver_path}")

    parts = driver_path[len("dnswatch.") :].split(".")
    if len(parts) < 2:
        raise ValueError(f"Driver path too short to infer group: {driver_path}")

    return ".".join(parts[:-1])


def get_version(semantic: bool = False) -> str:
    if semantic:
        return f"v{VERSION}"
    return VERSION
