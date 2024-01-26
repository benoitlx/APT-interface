from apt_interface.KPZ101 import KPZ101
from time import sleep

with KPZ101(config_file="config.yaml") as kpz:
    print(kpz.conf)

    #kpz.identify()
    #sleep(8)
    kpz.enable_output()
    voltages = [0, 1, 5, 10, 20, 30, 40, 50]
    for v in voltages:
        kpz.set_output_voltage(v)
        sleep(3)

    sleep(100)
