"""
Module: shear_capacity.py
Description:
    Computes the shear capacity of reinforced concrete walls
    using ACI 318-19 Section 18.10.4.1 with units in kg and cm.

Author: Ing. Patricio Palacios B., M.Sc.
Version: 1.0.0
Date: 2025-05-11
"""

import math


def compute_shear_capacity(
    f_c: float,
    fy: float,
    bw: float,
    lw: float,
    hw: float,
    rho_t: float,
    lambda_c: float = 1.0,
    phi: float = 0.60
) -> dict:
    """
    Computes shear capacity of a structural wall per ACI 318-19 in kg and cm.

    Parameters
    ----------
    f_c : float
        Concrete compressive strength f'c [kg/cm²].
    fy : float
        Yield strength of transverse reinforcement [kg/cm²].
    bw : float
        Wall thickness (cm).
    lw : float
        Wall length in plan (cm).
    hw : float
        Wall story height (cm).
    rho_t : float
        Total horizontal reinforcement ratio (As / (bw * s)).
    lambda_c : float, optional
        Modification factor for concrete density (default = 1.0 for normal weight).
    phi : float, optional
        Strength reduction factor for shear (default = 0.75).

    Returns
    -------
    dict
        Dictionary containing:
        - Vn : Nominal shear capacity [kg]
        - Vn_max : Upper limit per ACI [kg]
        - phiVn : Reduced shear capacity [kg]
        - alpha_c : ACI factor based on hw/lw
    """

    # Effective wall area
    Acv = bw * lw  

    # Compute alpha_c based on aspect ratio hw/lw
    alpha_c=0.53
    aspect = hw / lw
    if aspect <= 1.5:
        alpha_c = 0.80
    elif aspect >= 2.0:
        alpha_c = 0.53


    # Shear strength 
    Vc = Acv * (0.27 * alpha_c * lambda_c * math.sqrt(f_c))

    Vs = Acv * ( rho_t * fy) 

    Vn=Vc+Vs
    
    Vn_max = 2.65 * math.sqrt(f_c) * (bw * 0.8*lw  ) 

    # Final design strength (reduced)
    phi_Vn = phi * Vn
    phi_Vn_max= phi * Vn_max

    return {
        "Vc": Vc/1000,
        "Vs": Vs/1000,
        "Vn": Vn/1000,
        "Vn_max": Vn_max/1000,
        "phi_Vn": phi_Vn/1000,
        "phi_Vn_max": phi_Vn_max/1000,
    }
