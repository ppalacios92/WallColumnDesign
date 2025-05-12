"""
Module: wall_builder.py
Description:
    Provides a high-level interface for constructing and configuring
    reinforced concrete wall sections using the WallSection class.
    Also computes interaction diagram and shear capacity.

Author: Ing. Patricio Palacios B., M.Sc.
Version: 1.6.0
Date: 2025-05-11
"""

import math
from WallColumnDesign.geometry.wall_section import WallSection
from WallColumnDesign.tools.plotting import plot_wall_section
from WallColumnDesign.tools.interaction_plotter import plot_interaction_diagram
from WallColumnDesign.materials.concrete import Concrete
from WallColumnDesign.materials.steel import Steel
from WallColumnDesign.analysis.interaction_diagram import compute_interaction_diagram
from WallColumnDesign.analysis.shear_capacity import compute_shear_capacity


class WallBuilder:
    """
    Wrapper class that builds a reinforced concrete wall section using
    external material definitions and reinforcement configuration.

    Attributes
    ----------
    section : WallSection
        The constructed wall section instance.
    concrete : Concrete
        Concrete material object (stored externally).
    steel : Steel
        Steel material object (stored externally).
    results : list of dict
        Precomputed interaction diagram results.
    To, Po, Mb, Pb : float
        Notable points from the interaction diagram.
    Ag : float
        Gross concrete area [mm²].
    rho_main, rho_head1, rho_head2 : float
        Vertical reinforcement ratio in each region.
    Vn : float
        Shear capacity of the wall section [kgf].
    """

    def __init__(
        self,
        concrete: Concrete,
        steel: Steel,
        L1: float,
        thickness: float,
        cover: float,
        inc_main: tuple,
        N1: float, W1: float, inc_N1: tuple,
        N2: float, W2: float, inc_N2: tuple,
        diam_main: float = 1.6,
        diam_head1: float = 1.8,
        diam_head2: float = 1.8,
        rho_web: float = 0.001,
        hw: float = 350,
    ):
        self.concrete = concrete
        self.steel = steel
        self.rho_web=rho_web
        self.hw=hw


        # --- Geometry and reinforcement setup ---
        self.section = WallSection(
            L1=L1,
            thickness=thickness,
            cover=cover,
            inc_main=inc_main,
            N1=N1, W1=W1, inc_N1=inc_N1,
            N2=N2, W2=W2, inc_N2=inc_N2
        )
        self.section.diam_main = diam_main
        self.section.diam_head1 = diam_head1
        self.section.diam_head2 = diam_head2
        self.section.generate_geometry()
        self.section.generate_rebars()
        

        # --- Gross area [cm²] ---
        self.Ag = W1 * N1 + W2 * N2 + (L1 - N1 - N2) * thickness

        # --- Vertical reinforcement ratios ---
        As_main_total = len(self.section.rebars_main) * math.pi * (diam_main / 2)**2
        As_head1_total = len(self.section.rebars_N1) * math.pi * (diam_head1 / 2)**2
        As_head2_total = len(self.section.rebars_N2) * math.pi * (diam_head2 / 2)**2

        self.rho_main = As_main_total / (thickness * L1)
        self.rho_head1 = As_head1_total / (W1 * L1)
        self.rho_head2 = As_head2_total / (W2 * L1)

        # --- Interaction diagram ---
        self.results = compute_interaction_diagram(
            section=self.section,
            concrete=self.concrete,
            steel=self.steel,
            As_main=math.pi * (diam_main / 2)**2,
            As_head1=math.pi * (diam_head1 / 2)**2,
            As_head2=math.pi * (diam_head2 / 2)**2,
            c_max=4 * self.section.L1,
            c_step=1
        )

        self.To = next((r["To"] for r in self.results if "To" in r), None)
        self.Po = next((r["Po"] for r in self.results if "Po" in r), None)
        self.Mb = next((r["Mb"] for r in self.results if "Mb" in r), None)
        self.Pb = next((r["Pb"] for r in self.results if "Pb" in r), None)
        self.RestPo = next((r["RestPo"] for r in self.results if "RestPo" in r), None)

        # --- Shear capacity Vn [kgf] ---
        self.results_Vn = compute_shear_capacity(
            f_c=self.concrete.fc,
            fy=self.steel.fy,            
            bw=thickness,
            lw=L1,
            hw=self.hw,
            rho_t=self.rho_web,          
            lambda_c=1.0,
            phi=0.60
        )

    def build(self, plot: bool = True):
        """
        Optionally plots the wall section and its interaction diagram.

        Parameters
        ----------
        plot : bool
            If True, both the wall section and interaction diagram are plotted.
        """
        if plot:
            plot_wall_section(self.section)
            plot_interaction_diagram(self.results)
