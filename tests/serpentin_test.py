from apt_interface.KPZ101 import KPZ101
from apt_interface.scan import Scan
import matplotlib.pyplot as plt
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

    s = Scan((x, y))

    """Ploting Scan"""
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    x = [i for i, j, k in s.coords]
    y = [j for i, j, k in s.coords]
    z = [k for i, j, k in s.coords]
    ax.plot3D(x, y, z)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()
    """Ploting Scan"""

    # Launching scan on nanomax
    m = s.scan(mesure)
    print(m)

    while True:
        pass

    