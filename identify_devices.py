from apt_interface.device import Device
from struct import pack
from time import sleep

# KPZ101
with Device("29501986", 115200) as dev:
    print("\nWriting")
    print("should make the KPZ screen blink")
    print(dev.write(0x0223, 2, 0x00))
    
sleep(8)

# KSG101
with Device("59000407", 115200) as dev:
    print("Wrinting")
    print("should make the KSG screen blink")
    print(dev.write(0x0223, 2, 0x00))
        