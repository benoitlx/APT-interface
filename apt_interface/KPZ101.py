from .device import Device
from pydantic import BaseModel, validator
from pydantic_yaml import parse_yaml_file_as
from apt_interface import baud_rates
from struct import pack

class KPZ101Config(BaseModel):
    """Description du fichier yaml"""

    name: str = "KPZ101_default_controller"
    serial_nm: str
    baudrate: int = 115200
    mode: str = "open"
    feedback_in: str
    voltage_limit: int = 75

    @validator("serial_nm")
    def _chk_sn(cls, sn: str) -> str:
        assert sn[:2] == "29", 'Invalid Serial Number: KPZ101 needs to start with 29'
        return sn
    
    @validator("baudrate")
    def _chk_baud(cls, b: int) -> int:
        assert b in baud_rates, 'Invalid Baudrate'
        return b
    
    @validator("mode")
    def _chk_mode(cls, m: str) -> str:
        assert m in ["open_loop", "closed_loop"], 'Invalid Mode'
        return m
    
    @validator("voltage_limit")
    def _chk_v_lim(cls, v: int) -> int:
        assert v in [75, 100, 150], 'Invalid output voltage limit'
        return v

class KPZ101():
    pass

class KPZ101():

    def __init__(self, config_file="config.yaml") -> None:
        self.conf = parse_yaml_file_as(KPZ101Config, config_file)

        self.dev = Device(self.conf.serial_nm, self.conf.baudrate)

    def __enter__(self) -> KPZ101:
        self.dev.begin_connection()
        #self.set_io()
        self.set_mode()
        return self
    
    def identify(self) -> bool:
        """MGMSG_MOD_IDENTIFY"""
        return self.dev.write(0x0223, 2, 0x00)

    def set_mode(self) -> None:
        mode_dict = {"open_loop": 0x03, "closed_loop": 0x04}
        self.dev.write(0x0640, 2, mode_dict[self.conf.mode])

    def set_io(self) -> None:
        v_lim_dict = {75: 0x01, 100: 0x02, 150: 0x03}
        v_lim = v_lim_dict[self.conf.voltage_limit]

        a_in_dict = {"chann1": 0x01, "chann2": 0x02, "extin": 0x03}
        a_in = a_in_dict[self.conf.feedback_in]

        data = pack("HHHHH", 0x0001, v_lim, a_in, 0x0000, 0x0000)

        self.dev.write_with_data(0x07d4, 10, data)

    def set_output_voltage(self, tension) -> None:
        pass

    def balayage(self, zoi, fonction, *args, **kwargs) -> None:
        def reorganize(z) -> iter:
            """Reorganize the points to scan the nearest point first"""
            pass

        for coord in reorganize(zoi):
            # goto coord

            fonction(*args, **kwargs) # écrire la mesure dans une matrice

    def __exit__(self, *exc_info) -> None:
        self.dev.end_connection()

