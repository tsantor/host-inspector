# Host Inspector

A Python package to collect host/system information on macOS, Linux, and Windows.

## Installation

```bash
uv add host-inspector
# or
python3 -m pip install host-inspector
```

## Development Setup

```bash
just pip-install-editable
```

## Testing and Checks

```bash
just ruff-check
just pytest
just api-check
```

List all available project commands:

```bash
just
```

## Public API

Top-level imports from `host_inspector`:

```python
from host_inspector import get_cpu_info
from host_inspector import get_datetime_info
from host_inspector import get_device_info
from host_inspector import get_disk_info
from host_inspector import get_display_info
from host_inspector import get_firewall_info
from host_inspector import get_gpu_info
from host_inspector import get_health_info
from host_inspector import get_mem_info
from host_inspector import get_network_info
from host_inspector import get_os_info
from host_inspector import get_platform_info
from host_inspector import get_uptime_info
```

Additional module APIs:

```python
from host_inspector.firewall import get_firewall_info
from host_inspector.python import get_python_info
```

Example:

```python
from host_inspector import get_device_info, get_health_info
from host_inspector.python import get_python_info

print(get_device_info())
print(get_health_info())
print(get_python_info())
```

## Security Notes

Some firewall and hardware details may require elevated permissions depending on OS configuration.

### Linux (optional sudoers setup)

If your deployment requires passwordless access for specific probes, use `sudo visudo` and add only what you need, for example:

```ini
%sudo ALL=(ALL) NOPASSWD: /usr/sbin/ufw
%sudo ALL=(ALL) NOPASSWD: /usr/sbin/dmidecode
```

Apply the minimum required permissions for your environment.

## Issues

Report issues at: https://bitbucket.org/xstudios/host-inspector/issues
