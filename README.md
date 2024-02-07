# APT-interface

A python module to interface lab equipment that communicate with the Thorlab APT protocol


The module is composed for now of 4 differents files and modules:
 - `device.py` with class `Device` a low level communication class with APT devices
 - `KPZ101.py` with class `KPZ101` and `KPZ101Config` a module with multiple function to control KPZ101 devices
 - `KSG101.py` with class `KSG101` and `KSG101Config` a module with multiple function to control KSG101 devices
 - `scan.py` with class `Scan` and `ScanConfig` a module to generate coordinates and follow them with a KPZ101 device

 The full documentation is available [here](https://benoitlx.github.io/Documentation-Stage-G1/) (not finished yet)

 Feel free to create pull requests and add support for other devices, i will try my best to review the code and merge changes in time! You can as well add issues for any problem you encounter with implemented functions. 
 The documentation for APT protocol is available [here](https://www.thorlabs.com/Software/Motion%20Control/APT_Communications_Protocol.pdf).