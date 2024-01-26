from apt_interface.KPZ101 import KPZ101

with KPZ101() as kpz:
    print(kpz.conf.name)
    print(kpz.conf.serial_nm)
    print(kpz.conf.mode)
    kpz.identify()
