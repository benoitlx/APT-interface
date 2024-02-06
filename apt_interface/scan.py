from .KPZ101 import KPZ101
import numpy as np
from math import sin, cos, pi 

# TODO: import pydantic
# create a class ScanConfig with pydantic

class Scan():

    def __init__(self, axis: tuple[KPZ101], config_file="scan.yaml") -> None:
        self.axis = axis

        # self.mode = axis[0].conf.mode
        self.mode = "open_loop"

        # TODO: import yaml config with pydantic
        
        self.X = 0#self.conf.zoi.ref_point[0]
        self.Y = 0#self.conf.zoi.ref_point[1]
        self.Z = 0#self.conf.zoi.ref_point[2]

        self.deltaX = 32767#self.conf.zoi.dimension[0]
        self.deltaY = 32767#self.conf.zoi.dimension[1]
        self.deltaZ = 1#self.conf.zoi.dimension[2]

        # Appeler la bonne fonction pour construire self.coords
        # TODO: pattern matching sur le nom de la fonction
        stepx = self.deltaX/100 
        stepy = self.deltaY/100 
        stepz = 1

        self.axis_number = 3 - (stepz == self.deltaZ) - (stepy == self.deltaY)
        self.coords = self.balayage(stepx, stepy, stepz)
        #self.coords = self.spiral(10000)

    def scan(self, function, *args, **kwargs) -> np.ndarray:
        res = np.zeros(self.coords.shape[0])
        print(res.shape)

        for i, coord in enumerate(self.coords):
            print(f"{i=}, {coord=}")
            for j, axis_coord in enumerate(coord):
                if j < self.axis_number:
                    if self.mode == "closed_loop":
                        self.axis[j].set_position(int(axis_coord))
                    else:
                        self.axis[j].set_output_voltage(int(axis_coord))

            res[i] = function(args, kwargs)

        return res


    def balayage(self, stepx, stepy, stepz) -> np.ndarray[tuple]:
        coords = np.zeros(int(self.deltaZ/stepz*self.deltaY/stepy*self.deltaX/stepx), dtype=(float, 3))
        estimated_time = coords.size * 1 # self.conf.acquisition_time
        print(f"Temps estimé: {estimated_time}")

        index = 0
        for i, z in enumerate(np.linspace(self.Z, self.Z + self.deltaZ, int(self.deltaZ/stepz))):
            for j, y in enumerate(np.linspace(self.Y, self.Y + self.deltaY, int(self.deltaY/stepy))):
                for k, x in enumerate(np.linspace(self.X, self.X + self.deltaX, int(self.deltaX/stepx))):
                    match (i%2, j%2):
                        case (0, 0):
                            coords[index] = (x, y, z)
                        case (0, 1):
                            coords[index] = (self.X+self.deltaX-x, y, z)
                        case (1, 0):
                            coords[index] = (self.X+self.deltaX-x, self.Y+self.deltaY-y, z)
                        case (1, 1):
                            coords[index] = (x, self.Y+self.deltaY-y, z)
                    # print(f"{index=} {i=} {j=} {k=} {coords[index] = }")
                    index += 1

        return coords

    def spiral(self, tmax) -> np.ndarray[tuple]:
        coords = np.zeros(tmax, dtype=(float, 2))

        v = 2
        w = 4 * pi / 100

        rmid= v * tmax / 2

        for i in range(tmax):
            r = v * i / 2
            coords[i] = (rmid + r*cos(w*i), rmid + r*sin(w*i)) 

        return coords


    """
    def hilbert_curve_coordinates(order, t):
        if order == 0:
            return [(0.5, 0.5)]

        # Define the four corners of the unit square
        corners = [(0, 0), (0, 1), (1, 1), (1, 0)]

        # Map t to the appropriate quadrant
        index = (t >> (2 * (order - 1))) & 0b11

        # Calculate the midpoint of the current quadrant
        mid_x = (corners[0][0] + corners[2][0]) / 2
        mid_y = (corners[0][1] + corners[2][1]) / 2

        # Rotate and translate the coordinates
        if index == 0:
            return [(mid_y, mid_x)] + hilbert_curve_coordinates(order - 1, t)
        elif index == 1:
            return hilbert_curve_coordinates(order - 1, t) + [(mid_x, mid_y)]
        elif index == 2:
            return hilbert_curve_coordinates(order - 1, t) + [(mid_x, mid_y)]
        elif index == 3:
            return [(mid_y, mid_x)] + hilbert_curve_coordinates(order - 1, t)
    """
