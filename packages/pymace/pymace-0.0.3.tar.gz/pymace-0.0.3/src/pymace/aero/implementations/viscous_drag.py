import logging

from pymace.aero.generalfunctions import get_reynolds_number
from pymace.aero.implementations.airfoil_analyses import Airfoil
from pymace.aero.implementations.avl.athenavortexlattice import AVL
from pymace.aero.implementations.avl.geometry_and_mass_files import (
    GeometryFile,
    MassFile,
)
from pymace.domain import params
from pymace.domain.parser import PlaneParser
from pymace.domain.vehicle import Vehicle


class ViscousDrag:
    """
    This class calculates the viscous drag of a wing using XFOIL.
    """

    def __init__(self, plane: Vehicle):
        """
        :param plane: Plane object

        Initializes the viscous drag analysis.
        """
        self.plane = plane
        self.mass = self.plane.mass
        self.s_ref = self.plane.reference_values.s_ref
        self.g = params.Constants.g
        self.rho = params.Constants.rho

        self.print_re_warnings = True
        self.sensitivity_study_drag_factor = 1.0

    def match_segment_to_strip(self, surface: int, y: float, z: float):
        """
        :param surface: Surface (Wing) number
        :param y: y-coordinate of the strip (relevant for non-vertical wings)
        :param z: z-coordinate of the strip (relevant for vertical wings)

        This function matches the AVL strip to the corresponding Mace wing segment.
        """
        i = 0
        for wing in self.plane.wings.values():
            if wing.symmetric:
                i += 1
                if surface == i:
                    this_wing = wing
                    break
            i += 1
            if surface == i:
                this_wing = wing
                break

        for segment in this_wing.segments:
            if not this_wing.vertical:
                if segment.nose_inner[1] < abs(y) and segment.nose_outer[1] > abs(y):
                    this_segment = segment
                    break
            else:
                if segment.nose_inner[2] < z and segment.nose_outer[2] > z:
                    this_segment = segment
                    break
        return this_wing, this_segment

    def evaluate(self):
        """
        This function evaluates the viscous drag of a wing using XFOIL.
        It uses the AVL output file to get the geometry and flight condition. Since AVL is not dependent on the
        flight velocity, the velocity defined in the Plane object is used additionally.
        """

        AVL(self.plane).read_avl_output()
        V = self.plane.aero_coeffs.velocity
        FLAP = self.plane.aero_coeffs.flap_angle
        S_ref = self.plane.avl.outputs.s_ref
        S_sum = 0.0
        CD = 0.0

        for surface in range(self.plane.avl.outputs.number_of_surfaces):
            surface += 1
            strips = self.plane.avl.outputs.surface_dictionary[surface]["strips"][:, 0]
            for element in range(len(strips)):
                # initialize strip values
                strip_values = self.plane.avl.outputs.surface_dictionary[surface][
                    "strips"
                ][int(element - 1), :]

                # get local reynolds
                c = strip_values[4]
                cl = strip_values[9]  # 9 und nicht 6 (cl_norm)
                re = get_reynolds_number(V, c)
                y = strip_values[2]
                z = strip_values[3]

                wing, segment = self.match_segment_to_strip(surface, y, z)
                airfoil_name = wing.airfoil

                if segment.control:
                    flap_angle = FLAP * segment.c_gain
                else:
                    flap_angle = 0.0

                airfoil = Airfoil(
                    airfoil_name,
                    flap_angle=flap_angle,
                    x_hinge=(1 - segment.flap_chord_ratio),
                    sensitivity_study_factor=self.sensitivity_study_drag_factor,
                )
                airfoil.print_re_warnings = self.print_re_warnings

                cd = airfoil.get_cd(re, cl)

                S = strip_values[5]

                CD += cd * S / S_ref
                S_sum += S

        self.plane.aero_coeffs.drag_coeff.cd_visc = CD
        self.plane.aero_coeffs.drag_coeff.cd_tot = (
            CD + self.plane.aero_coeffs.drag_coeff.cd_ind
        )

        return CD


if __name__ == "__main__":
    # Initialize aircraft
    plane = PlaneParser("aachen.toml").get("Plane")
    GeometryFile(plane).build_geometry_file(1)
    MassFile(plane).build_mass_file()

    # Define Analysis
    V = 10.0
    W = plane.mass[0]
    CL = 0.5

    # Run AVL
    inviscid_analysis = AVL(plane)
    inviscid_analysis.run_avl(lift_coefficient=CL)
    inviscid_analysis.read_avl_output()

    # Run Xfoil
    viscous_analysis = ViscousDrag(plane)

    CDv = viscous_analysis.evaluate(V)
    CDi = plane.aero_coeffs.drag_coeff.cd_ind
    CD = CDv + CDi
    L_D = CL / CD

    logging.debug("V:  ", V)
    logging.debug("CL:  %.4f" % CL)
    logging.debug("CDv: %.4f" % CDv)
    logging.debug("CDi: %.4f" % CDi)
    logging.debug("L/D: %.4f" % L_D)
