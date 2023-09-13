# Imports
import numpy as np
import matplotlib.pyplot as plt


def plating_oz_to_thickness(oz):
    return 0.00135 * oz


def area_d(diameter):
    return (diameter/2)**2 * 3.14


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


def calc_max_vias(finished_hole, min_spacing, pad_l):
    """This function calculates the number of vias that can be packed into a square pad of length pad_l on a side
    The minimum spacing from the edge of a hole to the next is min_spacing."""

    num_vias = (pad_l // (finished_hole + min_spacing))**2
    
    return num_vias


def calc_effective_pad_conductivity(finished_hole, plating_thickness, number_vias, via_cond, board_cond, pad_l,):
    pad_area = pad_l ** 2
    via_area = area_d(finished_hole + (2 * plating_thickness))
    farm_area = via_area * number_vias
    board_area = pad_area - farm_area
    conductivity = ((farm_area / pad_area) * via_cond) + ((board_area / pad_area) * board_cond)
    return conductivity

def calc_thermal_resistance(cross_area, thickness, conductivity):
    return thickness / (cross_area * conductivity)



if __name__ == "__main__":

    hole_sizes = np.linspace(.004, .020, 1000)
    conductivities = via_effective_k(hole_sizes, plating_oz_to_thickness(.5), 3, 500)
    num_holes = calc_max_vias(hole_sizes, .005, .118)
    padn_conds = calc_effective_pad_conductivity(hole_sizes, plating_oz_to_thickness(.5), num_holes, conductivities, 3, .118)
    resistances = calc_thermal_resistance((meters_from_inches(0.118)**2),meters_from_inches(.010), padn_conds)

    fig, ax1 = plt.subplots()

    ax1.set_xlabel('Finished Hole Size [in]')
    ax1.set_ylabel('Effective Thermal Conductivity W/mK')
    ax1.plot(hole_sizes, padn_conds, color='b',label="Effective Conductivity of Pad")

    # Adding Twin Axes to plot using dataset_2
    ax2 = ax1.twinx()

    # ax2.set_xlabel('Finished Hole Size [in]')
    # ax2.set_ylabel('Number of Supported Vias')
    # ax2.plot(hole_sizes, num_holes, color='r', label="Number of Vias")
    
    ax2.set_xlabel('Finished Hole Size [in]')
    ax2.set_ylabel('Thermal Resistance')
    ax2.plot(hole_sizes, resistances, color='r', label="Number of Vias")
    
    plt.show()
    plt.savefig("holes.png",format='png')