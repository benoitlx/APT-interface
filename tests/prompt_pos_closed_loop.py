
from apt_interface.KSG101 import KSG101
from apt_interface.KPZ101 import KPZ101
from time import sleep

with KSG101() as ksg, KPZ101() as kpz:
    print(ksg.conf)
    print(kpz.conf)
    ksg.get_io() 
    ksg.get_max_travel()

    kpz.enable_output()
    ksg.zeroing()

    """
    positions = range(1000)
    for p in positions:
        kpz.set_position(p)
        sleep(.3)
        print(65534 - p, ksg.get_reading())
    """

    while True:
        p = int(input("desired position -32768..32767: "))
        kpz.set_position(p)
        sleep(2)
        print("reading -32768..32767: ", ksg.get_reading())