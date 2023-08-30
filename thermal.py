# Imports
import numpy as np
# import matplotlib.pyplot as plt


def plating_oz_to_thickness(oz):
    return 0.00135 * oz


def area_d(diameter):
    return (diameter/2)**2


def temp_rise(p_diss, r_theta):
    return p_diss * r_theta


def r_theta(thickness, area, conductivity):
    return thickness / (area * conductivity)


def meters_from_inches(inches):
    return inches * 0.0254


def via_effective_k(finished_hole, plating_thickness, fill_k, copper_k):
    barrel_dia = finished_hole + 2 * plating_thickness
    via_inner_dia = finished_hole
    hole_area = area_d(via_inner_dia)
    barrel_area = area_d(barrel_dia)
    copper_area = barrel_area - hole_area
    composite = (copper_area / barrel_area * copper_k) + (hole_area / barrel_area * fill_k)
    return composite


if __name__ == "__main__":
    print( via_effective_k(.0038, .0007, 3, 400) )
