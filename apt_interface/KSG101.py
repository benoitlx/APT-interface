from .device import Device
import yaml
import logging
import sys

class KSG101:

    def __init__(self) -> None:
        pass

    def __enter__(self) -> None:
        Device.begin_connection(self.serial_number)

    def __exit__(self, *exc_info) -> None:
        Device.end_connection()

