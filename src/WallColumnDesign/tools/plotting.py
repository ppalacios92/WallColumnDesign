"""
Module: plotting.py
Description:
    Provides visualization tools for plotting reinforced concrete wall sections,
    including concrete outline and reinforcement layout.

Author: Ing. Patricio Palacios B., M.Sc.
Version: 1.1.0
Date: 2025-05-11
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from typing import Any


def plot_wall_section(section: Any):
    """
    Plots the wall geometry and reinforcement bars based on precomputed geometry.

    Parameters
    ----------
    section : WallSection
        A WallSection object with previously generated geometry and rebar positions.
    """

    fig, ax = plt.subplots(figsize=(6, 10))

    # Validate required polygons
    if not section.polygon_head_1 or not section.polygon_head_2 or not section.polygon_web:
        raise ValueError("Wall geometry not generated. Call section.generate_geometry() first.")

    # Draw head 1 (top) as filled gray zone
    ax.add_patch(
        Polygon(
            section.polygon_head_1,
            closed=True,
            facecolor='lightgray',
            edgecolor='black',
            linewidth=0.8
        )
    )

    # Draw head 2 (bottom) as filled gray zone
    ax.add_patch(
        Polygon(
            section.polygon_head_2,
            closed=True,
            facecolor='lightgray',
            edgecolor='black',
            linewidth=0.8
        )
    )

    # Draw web (alma) as outlined polygon
    ax.add_patch(
        Polygon(
            section.polygon_web,
            closed=True,
            fill=False,
            edgecolor='black',
            linewidth=1.0
        )
    )

    # Draw rebars for web
    if section.rebars_main:
        xm, ym = zip(*section.rebars_main)
        ax.scatter(xm, ym, s=10, color='red', label='Web Rebars')

    # Draw rebars for head 1
    if section.rebars_N1:
        x1, y1 = zip(*section.rebars_N1)
        ax.scatter(x1, y1, s=10, color='blue', label='Head 1 Rebars')

    # Draw rebars for head 2
    if section.rebars_N2:
        x2, y2 = zip(*section.rebars_N2)
        ax.scatter(x2, y2, s=10, color='green', label='Head 2 Rebars')

    # Axes and labels
    ax.set_aspect('equal')
    ax.set_xlabel('Thickness X [mm]', fontsize=9, fontweight='bold')
    ax.set_ylabel('Height Y [mm]', fontsize=9, fontweight='bold')
    ax.set_title('Reinforced Concrete Wall Section', fontsize=10, fontweight='bold')
    ax.grid(True)

    # Place legend outside to the right
    ax.legend(
        loc='center left',
        bbox_to_anchor=(1.02, 0.5),
        borderaxespad=0.5,
        fontsize=8
    )

    plt.tight_layout()
    plt.show()
