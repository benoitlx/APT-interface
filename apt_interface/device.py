from pyftdi.ftdi import Ftdi
from struct import pack
from time import sleep
import logging
import sys

class Device:
    pass

class Device:
    dest = 0x50
    src = 0x01

    def __init__(self, sn: str, baud: int) -> None:
        """Initialize the device"""
        
        try:
            Ftdi.add_custom_product(Ftdi.DEFAULT_VENDOR, pid=0xfaf0) # watch udev rules !!!!
        except ValueError:
            print("Can't register new pid, trying without") 

        self.ftdi = Ftdi()
        self.sn = sn
        self.baud = baud

    def begin_connection(self) -> None:
        """Begin connection with the device with the serial number sn"""
        self.url = "".join(["ftdi://ftdi:0xfaf0:", self.sn, "/1"])
        self.ftdi.open_from_url(url=self.url)
        self.ftdi.set_baudrate(self.baud)

    def __enter__(self) -> Device:
        self.begin_connection()
        return self

    def read_data(self, func: bytes, size: int) -> bytes:
        self.write(func, 0x00, 0x00) # request value

        sleep(.01) # if you encounter reception problem, please increase the duration 
        return bytes(self.ftdi.read_data_bytes(size, attempt=3)) # get value
    
    def write(self, func: bytes, param1: bytes, param2: bytes) -> bool:
        bytes_array = pack("<HBBBB", func, param1, param2, self.dest, self.src)
        return self.ftdi.write_data(bytes_array) == 6

    def write_with_data(self, func, data_length: bytes, data: bytes) -> bool:
        bytes_array = pack("<HHBB", func, data_length, self.dest|0x80, self.src) + data

        return self.ftdi.write_data(bytes_array) == (6 + data_length)

    def end_connection(self) -> None:
        """Close connection with the device"""
        self.ftdi.close()

    def __exit__(self, *exc_info) -> None:
        self.end_connection()

if __name__ == "__main__":
    """List devices"""
    print("APT devices connected: ")
    Ftdi.add_custom_product(Ftdi.DEFAULT_VENDOR, pid=0xfaf0)
    Ftdi.show_devices()