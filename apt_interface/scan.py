from .KPZ101 import KPZ101
import numpy as np
import matplotlib.pyplot as plt
from pydantic import BaseModel, validator
from pydantic_yaml import parse_yaml_file_as
from typing import Literal, Optional 
from math import sin, cos, pi 
from itertools import starmap


# FIXME: validators need to be fixed, do not publish to pypi until this is fix

class Point(BaseModel):
    X: Optional[int] = None
    Y: Optional[int] = None
    Z: Optional[int] = None

    # TODO: validator -> at least one attribute needs to be not None

class ZoiConfig(BaseModel):
    ref_point: Point
    dimensions: Point

    # TODO: validator -> need a match between ref_point and dimensions

class BalayageConfig(BaseModel):
    steps: Point

class SpiraleConfig(BaseModel):
    rmax: float 
    n: int
    w: float

class ScanConfig(BaseModel):
    """Description du fichier yaml"""

    zoi: ZoiConfig
    scan_type: Literal["balayage", "spirale"]
    balayage: Optional[BalayageConfig] = None
    spirale: Optional[SpiraleConfig] = None
    mode: Literal["open_loop", "closed_loop"]
    acquisition_time: float

class Scan():

    def __init__(self, axis: tuple[KPZ101], config_file="scan.yaml") -> None:
        self.axis = axis

        self.conf = parse_yaml_file_as(ScanConfig, config_file)

        self.mode = "open_loop"

        self.X = self.conf.zoi.ref_point.X
        self.Y = self.conf.zoi.ref_point.Y
        self.Z = self.conf.zoi.ref_point.Z

        self.deltaX = self.conf.zoi.dimensions.X
        self.deltaY = self.conf.zoi.dimensions.Y
        self.deltaZ = self.conf.zoi.dimensions.Z

        # Appeler la bonne fonction pour construire self.coords
        match self.conf.scan_type:
            case "balayage":
                stepx = self.conf.balayage.steps.X
                stepy = self.conf.balayage.steps.Y
                stepz = self.conf.balayage.steps.Z

                self.coords = self.balayage(stepx, stepy, stepz)
            case "spirale":
                # TODO: load conf
                self.coords = self.spiral(10000)


    def scan(self, function, *args, **kwargs) -> np.ndarray:
        res = np.zeros(self.coords.shape[0])
        print(res.shape)

        for i, coord in enumerate(self.coords):
            print(f"{i=}, {coord=}")
            for j, axis_coord in enumerate(coord):
                if axis_coord is not None:
                    if self.mode == "closed_loop":
                        self.axis[j].set_position(int(axis_coord))
                    else:
                        self.axis[j].set_output_voltage(int(axis_coord))

            res[i] = function(args, kwargs)

        return res
    
    def visualize(self) -> None:
        plt.ion()
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        X, Y, Z = zip(*self.coords)
        default = np.zeros(len(X))
        X, Y, Z = map((lambda l: default if np.isnan(l[0]).any() else l), [X, Y, Z])

        ax.plot(X, Y, Z)

        plt.draw()
        plt.pause(1)

        for coord in self.coords:
            x, y, z = map((lambda l: 0 if np.isnan(l) else l), coord)
            print(x, y, z)
            ax.plot(X, Y, Z)
            ax.scatter(x, y, z, c='red', marker='o', s=50)

            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')

            plt.draw()
            plt.pause(self.conf.acquisition_time)

            ax.cla()

        plt.show()

    def switch_axis(self, axis: str, n: list[int]) -> enumerate:
        def manage_void_axis(arg1: int, arg2: int, arg3: int) -> enumerate:
            try:
                res = enumerate(np.linspace(arg1, arg1 + arg2, arg3))
            except TypeError:
                res = enumerate([np.nan]) 

            return res

        match axis:
            case 'X':
                return manage_void_axis(self.X, self.deltaX, n[0])
            case 'Y':
                return manage_void_axis(self.Y, self.deltaY, n[1])
            case 'Z':
                return manage_void_axis(self.Z, self.deltaZ, n[2])

    def balayage(self, stepx: float, stepy: float, stepz: float) -> np.ndarray[tuple]:
        n = [self.deltaX, self.deltaY, self.deltaZ]
        n = list(starmap((lambda x, y: 1 if x is None else int(y/x)), zip([stepx, stepy, stepz], n)))
        # n contains number of point per axis (if axis is not used, element will be set to 1)
        print(n)

        coords = np.zeros(n[0]*n[1]*n[2], dtype=(float, 3))
        estimated_time = coords.size * self.conf.acquisition_time
        print(f"Temps estimé: {estimated_time}")

        index = 0
        for i, z in self.switch_axis('Z', n):
            for j, y in self.switch_axis('Y', n):
                for k, x in self.switch_axis('X', n):
                    match (i%2, j%2):
                        case (0, 0):
                            coords[index] = (x, y, z)
                        case (0, 1):
                            coords[index] = (self.X+self.deltaX-x, y, z)
                        case (1, 0):
                            coords[index] = (x, self.Y+self.deltaY-y, z)
                        case (1, 1):
                            coords[index] = (self.X+self.deltaX-x, self.Y+self.deltaY-y, z)
                    # print(f"{index=} {i=} {j=} {k=} {coords[index] = }")
                    index += 1

        return coords

    def spiral(self, tmax) -> np.ndarray[tuple]:
        # TODO: modify parameters to be coherent with conf file
        coords = np.zeros(tmax, dtype=(float, 3))

        v = 8
        w = 4 * pi / 100

        rmid= v * tmax / 2

        for i in range(tmax):
            r = v * i / 2
            coords[i] = (rmid + r*cos(w*i), rmid + r*sin(w*i), None) 

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
