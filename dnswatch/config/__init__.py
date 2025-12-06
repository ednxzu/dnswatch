from oslo_config import cfg


def register_opts(conf: cfg.ConfigOpts) -> None:
    from dnswatch.config import defaults
    from dnswatch.config.resolvers import default as resolver_default
    from dnswatch.config.resolvers import json as resolver_json
    from dnswatch.config.updaters import designate as updater_designate
    from dnswatch.config.updaters import noop as updater_noop

    conf.register_opts(defaults.opts)

    conf.register_opts(resolver_default.opts, group="resolvers.default")
    conf.register_opts(resolver_json.opts, group="resolvers.json")
    conf.register_opts(updater_noop.opts, group="updaters.noop")
    conf.register_opts(updater_designate.opts, group="updaters.designate")


def list_opts():
    try:
        from dnswatch.config import defaults
        from dnswatch.config.resolvers import default as resolver_default
        from dnswatch.config.resolvers import json as resolver_json
        from dnswatch.config.updaters import designate as updater_designate
        from dnswatch.config.updaters import noop as updater_noop
    except Exception:
        import traceback

        traceback.print_exc()
        raise

    return [
        ("DEFAULT", defaults.opts),
        ("resolvers.default", resolver_default.opts),
        ("resolvers.json", resolver_json.opts),
        ("updaters.noop", updater_noop.opts),
        ("updaters.designate", updater_designate.opts),
    ]
