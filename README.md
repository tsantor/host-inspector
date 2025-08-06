# Host Info

![Coverage](https://img.shields.io/badge/coverage-99%25-brightgreen)

## Overview

A simple python package to gather host information from Windows, Mac and Linux. Returns host data as dicts to be used internally or sent to front-end dashboard applications as JSON.

## Installation

Install Host Info:

```bash
python3 -m pip install host-info
```

## Development

To get a list of all commands with descriptions simply run `make`.

```bash
make env
make pip_install_editable
```

## Testing

```bash
make pytest
make coverage
make open_coverage
```

## Issues

If you experience any issues, please create an [issue](https://github.com/tsantor/host-info/issues) on Github.

## Example Usage

```python
from host_info import get_device_info
from host_info import get_health_info

print(get_device_info())
print(get_health_info())

# You can also call individual methods:
from host_info import get_cpu_info
from host_info import get_datetime_info
from host_infoimport get_disk_info
from host_info import get_gpu_info
from host_info import get_mem_info
from host_info import get_network_info
from host_info import get_os_info
from host_info import get_platform_info
from host_info import get_uptime_info
```
