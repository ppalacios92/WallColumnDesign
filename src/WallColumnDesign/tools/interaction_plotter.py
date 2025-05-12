"""
Module: interaction_plotter.py
Description:
    Contains utilities for plotting the axial-moment interaction diagram
    of a reinforced concrete wall section using precomputed results.

Author: Ing. Patricio Palacios B., M.Sc.
Version: 1.4.0
Date: 2025-05-11
"""

import matplotlib.pyplot as plt
from typing import List


def plot_interaction_diagram(results: List[dict]):
    """
    Plots the nominal and reduced interaction diagrams with control points.

    Parameters
    ----------
    results : list of dict
        List with 'Pn', 'Mn', 'phi_Pn', 'phi_Mn', and optionally control points.
    """

    if not results:
        raise ValueError("No results to plot.")

    P = [r["Pn"] for r in results]
    M = [r["Mn"] for r in results]

    P_phi = [r["phi_Pn"] for r in results if "phi_Pn" in r]
    M_phi = [r["phi_Mn"] for r in results if "phi_Mn" in r]

    plt.figure(figsize=(8, 5))

    plt.plot(M, P, linestyle='-', linewidth=1.8, label="Nominal")
    plt.plot(M_phi, P_phi, linestyle='--', color='red', linewidth=1.5, label="Reduced")

    first = results[0]
    if all(key in first for key in ["To", "Po", "Mb", "Pb"]):
        plt.plot(0, first["To"], 's', color='purple', markersize=6,
                 label=f"To: M=0.0, P={first['To']:.1f}")
        plt.plot(0, first["Po"], 's', color='purple', markersize=6,
                 label=f"Po: M=0.0, P={first['Po']:.1f}")
        plt.plot(first["Mb"], first["Pb"], 's', color='purple', markersize=6,
                 label=f"Mb={first['Mb']:.1f}, Pb={first['Pb']:.1f}")

    if "RestPo" in first:
        rest_po = first["RestPo"]
        plt.axhline(y=rest_po, color='green', linestyle=':', linewidth=1.2,
                    label=f"Limit = {rest_po:.1f}")

    plt.xlabel("Moment M", fontsize=9, fontweight='bold')
    plt.ylabel("Axial Force P", fontsize=9, fontweight='bold')
    plt.title("Axial-Moment Interaction Diagram", fontsize=10, fontweight='bold')
    plt.grid(True)
    plt.legend(fontsize=8, loc='center left', bbox_to_anchor=(1.02, 0.5))
    plt.xlim(left=0)
    plt.tight_layout()
    plt.show()
