from .device import Device
from pydantic import BaseModel, field_validator, Field, ValidationInfo
from pydantic_yaml import parse_yaml_file_as
from apt_interface import VALID_BAUDRATES
from struct import pack
from typing import Iterable
from typing import Literal, Annotated


class KSG101Config(BaseModel):
    """Description du fichier yaml"""

    name: str = "KPZ101_default_controller"
    serial_nm: Annotated[str, Field(pattern=r"^59.*")]
    baudrate: VALID_BAUDRATES = 115200
    out: Literal["chann1", "chann2"] = "chann2"

class KSG101():
    pass

class KSG101():

    def __init__(self, config_file="config_KSG.yaml") -> None:
        self.conf = parse_yaml_file_as(KSG101Config, config_file)

        self.dev = Device(self.conf.serial_nm, self.conf.baudrate)

    def __enter__(self) -> KSG101:
        self.dev.begin_connection()
        return self

    def identify(self) -> bool:
        """MGMSG_MOD_IDENTIFY"""
        return self.dev.write(0x0223, 2, 0x00)

    def __exit__(self, *exc_info) -> None:
        self.dev.end_connection()

