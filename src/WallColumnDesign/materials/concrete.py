"""
Module: concrete.py
Description:
    Defines a class representing concrete material properties for wall interaction diagrams.
    Includes automatic calculation of modulus of elasticity and β₁ coefficient (block depth ratio).

Author: Ing. Patricio Palacios B., M.Sc.
Version: 1.2.1
Date: 2025-05-11
"""

import math

class Concrete:
    """
    Class to define concrete properties.

    Parameters
    ----------
    fc : float
        Compressive strength of concrete (MPa, positive value).
    eps_cu : float, optional
        Ultimate strain (default: 0.003).
    """

    def __init__(self, fc: float = 280.0, eps_cu: float = 0.003):
        self.fc = fc
        self.eps_cu = eps_cu
        self.Ec = 14500 * math.sqrt(fc)
        self.β = self.calculate_β()

    def calculate_β(self) -> float:
        """
        Computes the β₁ coefficient for rectangular stress block,
        based on design recommendations from the normative table.

        Returns
        -------
        float
            β₁ coefficient (dimensionless).
        """
        fc = self.fc

        # Normative thresholds and parameters (based on reference table)
        fc_lower_limit = 17.0*10     
        fc_upper_limit = 28.0*10     
        β_initial = 0.85
        β_reduction = 0.05
        fc_step = 7.0*10             
        β_min = 0.65

        if fc_lower_limit <= fc <= fc_upper_limit:
            β = β_initial
        else:
            β = β_initial - ((fc - fc_upper_limit) / fc_step) * β_reduction
            β = max(β, β_min)

        return β

    def __repr__(self):
        return (
            f"Concrete(fc={self.fc} MPa, Ec={self.Ec:.2f} MPa, "
            f"eps_cu={self.eps_cu}, β₁={self.β:.3f})"
        )
