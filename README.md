# APT-interface

A python module to interface lab equipment that communicate with the Thorlab APT protocol

# Installation

> The pypi package is not published yet, it will be soon

The package is based on the library [pyftdi](https://github.com/eblot/pyftdi) which uses `libusb 1.x` as a native dependency and thus should be installed.

## Windows

The easiest way is to install [zadig](https://zadig.akeo.ie/) (it will detect ftdi device automatically)

## Linux

```bash
apt-get install libusb-1.0
```

### udev rules configuration

Udev rules need to be created to communicate with devices without using administrator privileges.

> TODO

Finally, run the following command to install my package.
```bash
pip install apt-interface
```

# Usage

The package is composed for now of 4 differents files and modules:
 - `device.py` with class `Device` a low level communication class with APT devices
 - `KPZ101.py` with class `KPZ101` and `KPZ101Config` a module with multiple function to control KPZ101 devices
 - `KSG101.py` with class `KSG101` and `KSG101Config` a module with multiple function to control KSG101 devices
 - `scan.py` with class `Scan` and `ScanConfig` a module to generate coordinates and follow them with a KPZ101 device

## Simple example

### Configuration

Here is a simple configuration for a KPZ device

```yaml
name: X_axis_controller
serial_nm: "29501986"
baudrate: 115200
mode: closed_loop
feedback_in: chann2
voltage_limit: 75 
```

### Usage

```python
from apt_interface.KPZ101 import KPZ101

with KPZ101(config_file="config_KPZ.yaml") as kpz:
    print(kpz.conf)
    print(kpz.get_info())
    kpz.identify() # Should make the screen of the specified KPZ blink

    print("Warning High Voltage")
    kpz.enable_output()
    kpz.set_output_voltage(20) # The KPZ needs to be configured in open_loop for voltage control
```

The full documentation is available [here](https://benoitlx.github.io/Documentation-Stage-G1/) (not finished yet, a dedicated page will be added)

Feel free to create pull requests and add support for other devices, i will try my best to review the code and merge changes in time! You can as well add issues for any problem you encounter with implemented functions. 
The documentation for APT protocol is available [here](https://www.thorlabs.com/Software/Motion%20Control/APT_Communications_Protocol.pdf).