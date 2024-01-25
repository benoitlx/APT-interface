from pyftdi.ftdi import Ftdi
import logging
import sys

class Device:
    
    def __init__(self) -> None:
        """Initialize the device"""
        
        Ftdi.add_custom_product(Ftdi.DEFAULT_VENDOR, pid=0xfaf0) # watch udev rules !!!!

        self.ftdi = Ftdi()

    def begin_connection(self, sn, baud) -> None:
        """Begin connection with the device with the serial number sn"""
        self.url = "".join(["ftdi://ftdi:0xfaf0:", sn, "/1"])
        self.ftdi.open_from_url(url=self.url)
        self.ftdi.set_baudrate(baud)

    def read_data(self) -> str:
        pass

    def write_data(self, bytes_array) -> None:
        pass

    def end_connection(self) -> None:
        """Close connection with the device"""
        
        self.ftdi.close()

if __name__ == "__main__":
    """List devices"""
    print("APT devices connected: ")
    Ftdi.add_custom_product(Ftdi.DEFAULT_VENDOR, pid=0xfaf0)
    Ftdi.show_devices()