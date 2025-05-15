"""
Module: interaction_diagram.py
Description:
    Computes the axial-moment interaction diagram for a vertical reinforced concrete wall.

    Includes results of concrete and steel contributions, and identifies key control points:
    - To: Axial force when c = 0
    - Po: Maximum compressive axial force (moment ≈ 0)
    - Mb: Maximum moment resistance
    - Pb: Axial force corresponding to Mb

    Also includes:
    - phi_Pn: reduced axial force
    - phi_Mn: reduced moment

Author: Ing. Patricio Palacios B., M.Sc.
Version: 1.4.0
Date: 2025-05-11
"""

import numpy as np
from typing import List, Dict
from WallColumnDesign.geometry.wall_section import WallSection
from WallColumnDesign.geometry.geometry_utils import clip_polygon_above_c
from WallColumnDesign.materials.concrete import Concrete
from WallColumnDesign.materials.steel import Steel


def compute_phi_E(epsilon_s: float) -> float:
    """
    Computes the phi_E factor (ACI 318) based on steel strain.
    """
    eps = epsilon_s*-1
    eps_yield = 0.002
    eps_max = 0.005
    phi_min = 0.65
    phi_max = 0.90

    if eps >= eps_max:
        return phi_max
    elif eps <= eps_yield:
        return phi_min
    else:
        return phi_min + (eps - eps_yield) * (phi_max - phi_min) / (eps_max - eps_yield)


def compute_interaction_diagram(
    section: WallSection,
    concrete: Concrete,
    steel: Steel,
    As_main: float,
    As_head1: float,
    As_head2: float,
    c_max: float,
    c_step: float = 5.0
) -> List[dict]:
    """
    Computes the interaction diagram for a wall at 0° rotation (vertical position).

    Parameters
    ----------
    section : WallSection
        Wall section geometry with generated rebars and polygons.
    concrete : Concrete
        Concrete material object (contains fc and β₁).
    steel : Steel
        Steel material object (contains Es and fy).
    As_main : float
        Area per bar in web (cm²).
    As_head1 : float
        Area per bar in head 1 (cm²).
    As_head2 : float
        Area per bar in head 2 (cm²).
    c_max : float
        Maximum value of neutral axis depth to evaluate (mm).
    c_step : float, optional
        Step for evaluating c (mm). Default is 5.0 mm.

    Returns
    -------
    List[dict]
        List with keys:
        - 'c', 'Pn', 'Mn', 'Ac', 'Fc', 'Ps', 'phi_Pn', 'phi_Mn', 'To', 'Po', 'Mb', 'Pb'
    """

    results = []
    y_top = section.L1
    β = concrete.β
    fc = concrete.fc
    Es = steel.Es
    fy = steel.fy

    rebars = (
        [(x, y, As_main) for x, y in section.rebars_main] +
        [(x, y, As_head1) for x, y in section.rebars_N1] +
        [(x, y, As_head2) for x, y in section.rebars_N2]
    )

    To = None
    Po = None
    min_abs_moment = float("inf")
    Mb = -np.inf
    Pb = None

    c_values = np.linspace(0.0001, c_max, int(c_max // c_step) + 1)

    for c in c_values:
        a = β * c
        y_min = y_top - a

        # Concrete contribution
        Ac = 0.0
        cx_total = 0.0
        cy_total = 0.0
        for poly in [section.polygon_head_1, section.polygon_web, section.polygon_head_2]:
            area, cx, cy = clip_polygon_above_c(poly, y_min)
            Ac += area
            cx_total += area * cx
            cy_total += area * cy

        if Ac == 0:
            continue

        cx_total /= Ac
        cy_total /= Ac
        Fc = 0.85 * fc * Ac / 1000        # kN
        zc = (cy_total - section.L1 / 2) / 100  # m
        Mc = Fc * zc

        # Steel contribution
        Ps = 0.0
        Ms = 0.0


        y_min = min(y for _, y, _ in rebars)
        x_max = max(x for x, y, _ in rebars if abs(y - y_min) < 1e-3)

        for x, y, As in rebars:
            ε_s = (0.003 / c) * (c - (section.L1 - y)) if c > 0 else 0.0
            σ_s = max(min(Es * ε_s, fy), -fy)
            Fs = σ_s * As / 1000  
            arm = (y - section.L1 / 2) / 100  
            Ps += Fs
            Ms += Fs * arm
            if abs(y - y_min) < 1e-3 and abs(x - x_max) < 1e-3:
                ε_s_max = ε_s

        Pn = Fc + Ps
        Mn = Mc + Ms
        ϕ = compute_phi_E(ε_s_max)

        RestPo_0_35 = 0.35 * fc * Ac / 1000 
        RestPo_0_10 = 0.10 * fc * Ac / 1000 


        # Save control points
        if c <= 0.01:
            To = Pn
        if Pn > 0 and abs(Mn) < min_abs_moment:
            min_abs_moment = abs(Mn)
            Po = Pn
        if Mn > Mb:
            Mb = Mn
            Pb = Pn

        results.append({
            "c": c,
            "Pn": Pn,
            "Mn": Mn,
            "Ac": Ac,
            "Fc": Fc,
            "Ps": Ps,
            "phi_Pn": ϕ * Pn,
            "phi_Mn": ϕ * Mn
        })


    if results:
        results[0]["To"] = To
        results[0]["Po"] = Po
        results[0]["Mb"] = Mb
        results[0]["Pb"] = Pb
        results[0]["RestPo_0_35"] = RestPo_0_35
        results[0]["RestPo_0_10"] = RestPo_0_10

        # Calcular Rec_C2 (restricción máxima de capacidad a compresión)
        Rec_C2 = 0.80 * 0.65 * Po  # Tonf
        for r in results:
            if r["phi_Pn"] > Rec_C2:
                r["phi_Pn"] = Rec_C2


    return results
