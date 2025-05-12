"""
Module: steel.py
Description:
    Defines a class representing steel material properties for wall reinforcement.

Author: Ing. Patricio Palacios B., M.Sc.
Version: 1.0.0
Date: 2025-05-11
"""

class Steel:
    """
    Class to define steel properties.

    Parameters
    ----------
    fy : float
        Yield strength (MPa).
    Es : float
        Modulus of elasticity (MPa).
    """

    def __init__(self, fy: float = 4200.0, Es: float = 2.0e6):
        self.fy = fy
        self.Es = Es

    def __repr__(self):
        return f"Steel(fy={self.fy} MPa, Es={self.Es:.2f} MPa)"
