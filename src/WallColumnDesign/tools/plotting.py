# """
# Module: plotting.py
# Description:
#     Provides visualization tools for plotting reinforced concrete wall sections,
#     including concrete outline and reinforcement layout.

# Author: Ing. Patricio Palacios B., M.Sc.
# Version: 1.1.0
# Date: 2025-05-11
# """

# import matplotlib.pyplot as plt
# from matplotlib.patches import Polygon
# from typing import Any


# def plot_wall_section(section: Any):
#     """
#     Plots the wall geometry and reinforcement layout.

#     Parameters
#     ----------
#     section : WallSection
#         WallSection object with generated geometry and reinforcement.
#     """

#     fig, ax = plt.subplots(figsize=(6, 10))

#     if not section.polygon_head_1 or not section.polygon_head_2 or not section.polygon_web:
#         raise ValueError("Wall geometry not defined. Call generate_geometry() first.")

#     # Head 1 (top)
#     ax.add_patch(
#         Polygon(
#             section.polygon_head_1,
#             closed=True,
#             facecolor='lightgray',
#             edgecolor='black',
#             linewidth=0.8
#         )
#     )

#     # Head 2 (bottom)
#     ax.add_patch(
#         Polygon(
#             section.polygon_head_2,
#             closed=True,
#             facecolor='lightgray',
#             edgecolor='black',
#             linewidth=0.8
#         )
#     )

#     # Web
#     ax.add_patch(
#         Polygon(
#             section.polygon_web,
#             closed=True,
#             fill=False,
#             edgecolor='black',
#             linewidth=1.0
#         )
#     )

#     # Web rebars
#     if section.rebars_main:
#         xm, ym = zip(*section.rebars_main)
#         ax.scatter(xm, ym, s=10, color='red', label='Web Rebars')

#     # Head 1 rebars
#     if section.rebars_N1:
#         x1, y1 = zip(*section.rebars_N1)
#         ax.scatter(x1, y1, s=10, color='blue', label='Head 1 Rebars')

#     # Head 2 rebars
#     if section.rebars_N2:
#         x2, y2 = zip(*section.rebars_N2)
#         ax.scatter(x2, y2, s=10, color='green', label='Head 2 Rebars')

#     ax.set_aspect('equal')
#     ax.set_xlabel('X')
#     ax.set_ylabel('Y')
#     ax.set_title('Wall Section')
#     ax.grid(True)

#     ax.legend(loc='center left', bbox_to_anchor=(1.02, 0.5), fontsize=8)
#     plt.tight_layout()
#     plt.show()
"""
Module: plotting.py
Description:
    Provides visualization tools for plotting reinforced concrete wall sections
    in horizontal orientation, including concrete outline and reinforcement layout.

Author: Ing. Patricio Palacios B., M.Sc.
Version: 1.1.1
Date: 2025-05-14
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from typing import Any


def plot_wall_section(section: Any):
    """
    Plots the wall geometry and reinforcement layout rotated to horizontal orientation.

    Parameters
    ----------
    section : WallSection
        WallSection object with generated geometry and reinforcement.
    """

    fig, ax = plt.subplots(figsize=(10, 6))

    if not section.polygon_head_1 or not section.polygon_head_2 or not section.polygon_web:
        raise ValueError("Wall geometry not defined. Call generate_geometry() first.")

    # Helper to rotate coordinates: (x, y) -> (y, x)
    def rotate_coords(coords):
        return [(y, x) for (x, y) in coords]

    # Head 1 (rotated)
    ax.add_patch(
        Polygon(
            rotate_coords(section.polygon_head_1),
            closed=True,
            facecolor='lightgray',
            edgecolor='black',
            linewidth=0.8
        )
    )

    # Head 2 (rotated)
    ax.add_patch(
        Polygon(
            rotate_coords(section.polygon_head_2),
            closed=True,
            facecolor='lightgray',
            edgecolor='black',
            linewidth=0.8
        )
    )

    # Web (rotated)
    ax.add_patch(
        Polygon(
            rotate_coords(section.polygon_web),
            closed=True,
            fill=False,
            edgecolor='black',
            linewidth=1.0
        )
    )

    # Web rebars (rotated)
    if section.rebars_main:
        xm, ym = zip(*section.rebars_main)
        ax.scatter(ym, xm, s=10, color='red', label='Web Rebars')

    # Head 1 rebars (rotated)
    if section.rebars_N1:
        x1, y1 = zip(*section.rebars_N1)
        ax.scatter(y1, x1, s=10, color='blue', label='Head 1 Rebars')

    # Head 2 rebars (rotated)
    if section.rebars_N2:
        x2, y2 = zip(*section.rebars_N2)
        ax.scatter(y2, x2, s=10, color='green', label='Head 2 Rebars')

    ax.set_aspect('equal')
    ax.set_xlabel('Y')
    ax.set_ylabel('X')
    ax.set_title('Wall Section (Horizontal View)', fontsize=10, fontweight='bold')
    ax.grid(True)

    ax.legend(loc='center left', bbox_to_anchor=(1.02, 0.5), fontsize=8)
    plt.tight_layout()
    plt.show()
