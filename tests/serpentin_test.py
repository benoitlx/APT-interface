from apt_interface.KPZ101 import KPZ101
from apt_interface.scan import Scan
from time import sleep

def mesure(*args, **kwargs):
    # il faut laisser assez de délais pour que les mouvements ne soient pas trop brusques

    sleep(.05)
    return 1

with KPZ101(config_file="tests/x.yaml") as x, \
     KPZ101(config_file="tests/y.yaml") as y, \
     KPZ101(config_file="tests/z.yaml") as z:
    print(x.conf)
    print(y.conf)
    print(z.conf)


    x.enable_output()
    y.enable_output()
    z.enable_output()

    s = Scan((x, y, None), config_file="tests/scan.yaml")

    # Launching scan on nanomax
    # s.visualize()
    m = s.scan(mesure)

    # m contains the matrix of measurement
    print(m)

    while True:
        pass

    