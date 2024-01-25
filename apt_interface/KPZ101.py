from .device import Device
import yaml
import logging
import sys

class KPZ101:

    def __init__(self) -> None:
        self.serial_number = 0

        self.dev = Device()

    def __enter__(self) -> None:
        self.dev.begin_connection(self.serial_number)

    def set_mode(self, mode) -> None:
        pass

    def set_output_voltage(self, tension) -> None:
        pass

    def balayage(self, zoi, fonction, *args, **kwargs) -> None:
        for coord in zoi:
            # goto coord

            fonction(*args, **kwargs) # écrire la mesure dans une matrice

    def __exit__(self, *exc_info) -> None:
        self.dev.end_connection()

