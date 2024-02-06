from .device import Device
from pydantic import BaseModel, field_validator, Field, ValidationInfo
from pydantic_yaml import parse_yaml_file_as
from apt_interface import VALID_BAUDRATES
from struct import pack, unpack
from typing import Iterable
from typing import Literal, Annotated


class KSG101Config(BaseModel):
    """Description du fichier yaml"""

    name: str = "KPZ101_default_controller"
    serial_nm: Annotated[str, Field(pattern=r"^59.*")]
    baudrate: VALID_BAUDRATES = 115200
    out: Literal["chann1", "chann2"] = "chann2"
    unit: Literal["pos", "volt", "force"]

class KSG101():
    pass

class KSG101():

    def __init__(self, config_file="config_KSG.yaml") -> None:
        self.conf = parse_yaml_file_as(KSG101Config, config_file)

        self.dev = Device(self.conf.serial_nm, self.conf.baudrate)

    def __enter__(self) -> KSG101:
        print("test")
        self.dev.begin_connection()
        self.set_io()
        return self
    
    def set_io(self) -> None:
        unit_dict = {"pos": 0x01, "volt": 0x02, "force": 0x03}
        self.unit = unit_dict[self.conf.unit]

        chann_dict = {"chann1": 0x01, "chann2": 0x02}
        self.chann = chann_dict[self.conf.out]

        data = pack("HHHHHHH", 0x0001, self.chann, self.unit, 0x0000, 0x7530, 0, 0)
        print(data)

        self.dev.write_with_data(0x07da, 14, data)

    def get_io(self) -> None:
        buffer = self.dev.read_data(0x07db, 20)

        data = unpack("HHHHHHHHHH", buffer)
        unit = data[5]
        out = data[4]

        print(f"{unit=}, {out=}")


    def get_reading(self) -> float:
        buffer = self.dev.read_data(0x07dd, 12)

        read = unpack("HHHHhH", buffer)[4]

        return read
    
    def get_max_travel(self) -> None:
        buffer = self.dev.read_data(0x0650, 10)

        print(unpack("HHHHH", buffer)[4])
    
    def zeroing(self) -> None:
        self.dev.write(0x0658, 0, 0)

    def identify(self) -> bool:
        """MGMSG_MOD_IDENTIFY"""
        return self.dev.write(0x0223, 2, 0x00)

    def __exit__(self, *exc_info) -> None:
        self.dev.end_connection()

