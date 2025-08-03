## v0.2.0 (2025-08-03)

### Feat

- **container**: copy sample config file in the container to avoid unusable state if left untouched
- **config**: make configuration modular and generate sample file

### Fix

- **updaters/designate**: fix error on updating an existing but wrong DNS record

## v0.1.0 (2025-08-02)

### Feat

- add version tracking in-app
- add json resolver as builtin resolver
- **updaters**: add OpenStack Designate updateru
- **resolvers**: add better ip address handling for default resolver

### Fix

- remove unused library from final container to avoid unnecessary vulnerabilities
- use lazy loading for default resolver logs
