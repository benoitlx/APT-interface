from apt_interface.KPZ101 import KPZ101
from apt_interface.KSG101 import KSG101

gauge_fn = "conf_strain_gauge.yaml"
controller_fn = "conf_controller.yaml"

with KSG101(gauge_fn, "sn_x") as gauge_x, KSG101(gauge_fn, "sn_y") as gauge_y: 
    """Automatically close the connection"""
    gauge_x.init_conf()
    gauge_y.init_conf()

with KPZ101(controller_fn, "serial_number_x") as x, KPZ101(controller_fn, "serial_number_y") as y:
    """Balayage de surface

    load scan conf

    for coor_x in zoi_x:
        for coord_y in zoi_y:
            mesure du point
            ajouter la mesure dans une matrice

    Autre idée:

    with serial_com as pscm:
        y.balayage(zoi_y, x.balayage(zoi_x, pscm.mesure))
    """
    pass