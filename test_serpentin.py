from apt_interface.KPZ101 import KPZ101
from apt_interface.scan import Scan
from time import sleep

def mesure(*args, **kwargs):
    # il faut laisser assez de délais pour que les mouvements ne soient pas trop brusques

    sleep(.01)
    return 1

with KPZ101(config_file="x.yaml") as x, KPZ101(config_file="y.yaml") as y:
    print(x.conf)
    print(y.conf)


    x.enable_output()
    y.enable_output()

    s = Scan((x, y), )
    m = s.scan(mesure)
    print(m)

    while True:
        pass

    