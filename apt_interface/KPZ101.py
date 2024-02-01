from .device import Device
from pydantic import BaseModel, field_validator, Field, ValidationInfo
from pydantic_yaml import parse_yaml_file_as
from apt_interface import VALID_BAUDRATES
from struct import pack
from typing import Iterable
from typing import Literal, Annotated


class KPZ101Config(BaseModel):
    """Description du fichier yaml"""

    name: str = "KPZ101_default_controller"
    serial_nm: Annotated[str, Field(pattern=r"^29.*")]
    baudrate: VALID_BAUDRATES = 115200
    mode: Literal["open_loop", "closed_loop"] = "open_loop"
    feedback_in: str = "chann2"
    voltage_limit: Literal[75, 100, 150] = 75

    @field_validator("feedback_in")
    def _chk_feedback(cls, f: str, v: ValidationInfo) -> str:
        assert v.data["mode"] == "closed_loop"
        return f
    

class KPZ101():
    pass

class KPZ101():

    def __init__(self, config_file="config_KPZ.yaml") -> None:
        self.conf = parse_yaml_file_as(KPZ101Config, config_file)

        self.dev = Device(self.conf.serial_nm, self.conf.baudrate)

    def __enter__(self) -> KPZ101:
        self.dev.begin_connection()
        self.disable_output()
        self.set_io()
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

    def set_output_voltage(self, tension: int) -> None:
        """
        assert self.conf.mode == "open_loop", 'Cannot specify a voltage in closed_loop mode'
        assert tension >= 0 and tension <= self.conf.voltage_limit, f'{tension} volt is not allowed'

        # TODO: add an offset
        # FIXME: wrong ratoi when changing voltage limit

        self.device_unit = int(32768/self.conf.voltage_limit)
        print(self.device_unit)
        data = pack("HH", 0x0001, int(tension * self.device_unit))

        print(int(tension * self.device_unit))
        """
        data = pack("HH", 0x0001, tension)
        print(data)
        self.dev.write_with_data(0x0643, 4, data)

    def set_position(self, pos: int) -> None:
        assert self.conf.mode == "closed_loop", 'Cannot specify a position in open_loop mode'
        assert pos >= 0 and pos <= 32767 # according to the documentation, negative values aren't used

        data = pack("HH", 0x0001, pos)

        self.dev.write_with_data(0x0646, 4, data)


    def enable_output(self) -> None:
        print("Warning High Voltage !!")
        self.dev.write(0x0210, 2, 0x01)

    def disable_output(self) -> None:
        self.dev.write(0x0210, 2, 0x02)

    def get_info(self) -> bytes:
        """Return KPZ info, parsed as bytes"""
        return self.dev.read_data(0x0005, 90)

    def balayage(self, zoi, fonction, *args, **kwargs) -> None:
        def reorganize(z) -> list[float]:
            """Reorganize the points to scan the nearest point first"""
            pass

        for coord in reorganize(zoi):
            # goto coord

            fonction(*args, **kwargs) # typiquement: écrire la mesure dans une matrice

    def __exit__(self, *exc_info) -> None:
        self.disable_output()
        self.dev.end_connection()

if __name__ == "__main__":
    with KPZ101() as kpz:
        kpz.identify()