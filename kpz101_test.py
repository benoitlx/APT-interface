from apt_interface.KPZ101 import KPZ101, KPZ101Config
from time import sleep
import json

print(json.dumps(KPZ101Config.model_json_schema()))

with KPZ101(config_file="config.yaml") as kpz:
    print(kpz.conf)

    kpz.identify()
    sleep(8)
    kpz.enable_output()
    voltages = [0, 1, 5, 10, 20, 30, 40, 50]
    for v in voltages:
        kpz.set_output_voltage(v)
        sleep(3)

    sleep(100)