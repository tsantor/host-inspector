# History

All notable changes to this project will be documented in this file. This project adheres to [Semantic Versioning](http://semver.org/).

## 0.3.0 (2026-04-20)

- CHANGED: Migrated packaging/build backend to `hatchling` with `xapp-tools`.
- CHANGED: Updated supported Python baseline to `>=3.11`.
- CHANGED: Removed legacy setuptools packaging artifacts and build helper scripts.
- CHANGED: Updated public API contract to focus on module-level exports.

## 0.2.5 (2026-03-13)

- CHANGED: Completed layered (domain/application/infrastructure) refactors across host info domains.
- CHANGED: Replaced dict-style application port payloads with dataclass DTO contracts where structured payloads cross boundaries.
- CHANGED: Updated README workflow docs to use `just` commands for setup/check/test tasks.

## 0.2.4 (2025-11-21)

- CHANGED: Firewall rule `enabled` will always be a boolean rather than YES/NO on Windows for consistency.
- ADDED: Added tox and tox-uv for testing against multiple versions of python

## 0.2.3 (2025-10-07)

- CHANGED: Ensure tests pass on Ubuntu (not all data available - yet)

## 0.2.2 (2025-09-25)

- CHANGED: Standardize date/time formatting for device `uptime` and `local_datetime`

## 0.2.1 (2025-09-23)

- ADDED: Support for getting Linux Firewall status and rules using `ufw`.

## 0.2.0 (2025-09-09)

- CHANGED: `get_device_info` now returns a `displays` key which is a list of connected displays
- CHANGED: `get_gpu_info` now returns a list of dicts (one for each GPU)
- ADDED: `get_display_info` returns a list of dicts (one for each display)
- CHANGED: For backawards compatability, when calling `get_device_info`, the `gpu` key will be an object if only one GPU detected.

## 0.1.1 (2025-09-04)

- ADDED: Support for getting Windows Firewall status and rules

## 0.1.0 (2025-08-06)

- First release
