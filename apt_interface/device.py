from pyftdi.ftdi import Ftdi

class Device:
    
    def __init__(self) -> None:
        """Initialize the device"""
        pass

    def __enter__(self) -> None:
        """Begin connection with the device"""
        pass

    def read_data(self) -> str:
        pass

    def write_data(self, bytes_array) -> None:
        pass

    def __exit__(*exc_info) -> None:
        """Close connection with the device"""
        pass