"""
Module: geometry_utils.py
Description:
    Provides utility functions for geometric operations, such as
    clipping a polygon above a horizontal line and computing area and centroid.

Author: Ing. Patricio Palacios B., M.Sc.
Version: 1.0.0
Date: 2025-05-11
"""

from typing import List, Tuple
from WallColumnDesign.geometry.wall_section import WallSection


def clip_polygon_above_c(
    polygon: List[Tuple[float, float]], 
    c: float
) -> Tuple[float, float, float]:
    """
    Clips the polygon above a horizontal line y = c and returns
    the area and centroid of the resulting polygon (if any).

    Returns
    -------
    area : float
    cx : float
    cy : float
    """
    clipped = []
    n = len(polygon)

    for i in range(n):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % n]
        y1, y2 = p1[1], p2[1]

        if y1 >= c:
            if y2 >= c:
                clipped.append(p2)
            else:
                x_int = p1[0] + (p2[0] - p1[0]) * (y1 - c) / (y1 - y2)
                clipped.append((x_int, c))
        else:
            if y2 >= c:
                x_int = p1[0] + (p2[0] - p1[0]) * (c - y1) / (y2 - y1)
                clipped.append((x_int, c))
                clipped.append(p2)

    if len(clipped) < 3:
        return 0.0, 0.0, 0.0

    x = [pt[0] for pt in clipped]
    y = [pt[1] for pt in clipped]
    return _polygon_area_centroid(x, y)


def _polygon_area_centroid(x: List[float], y: List[float]) -> Tuple[float, float, float]:
    """
    Computes the area and centroid of a polygon using the Gauss-Green formula.

    Parameters
    ----------
    x : list of float
        X-coordinates of the vertices.
    y : list of float
        Y-coordinates of the vertices.

    Returns
    -------
    area : float
        Polygon area.
    cx : float
        X-coordinate of the centroid.
    cy : float
        Y-coordinate of the centroid.
    """
    n = len(x)
    A = 0.0
    Cx = 0.0
    Cy = 0.0

    for i in range(n):
        j = (i + 1) % n
        cross = x[i] * y[j] - x[j] * y[i]
        A += cross
        Cx += (x[i] + x[j]) * cross
        Cy += (y[i] + y[j]) * cross

    A *= 0.5
    if A == 0.0:
        return 0.0, 0.0, 0.0

    Cx /= (6 * A)
    Cy /= (6 * A)

    return abs(A), Cx, Cy


def compute_area_and_centroid(polygon: List[Tuple[float, float]]) -> Tuple[float, float, float]:
    """
    Wrapper to compute area and centroid from a list of 2D points.

    Parameters
    ----------
    polygon : list of tuple
        Polygon vertices in counter-clockwise order.

    Returns
    -------
    area : float
    cx : float
    cy : float
    """
    x = [pt[0] for pt in polygon]
    y = [pt[1] for pt in polygon]
    return _polygon_area_centroid(x, y)


def compute_compression_block(section: WallSection, c_values: List[float]) -> List[dict]:
    """
    Computes the compressed block geometry for a range of neutral axis depths 'c'.

    Parameters
    ----------
    section : WallSection
        The wall section object with generated polygons.
    c_values : list of float
        Values of neutral axis depth 'c' (mm) to evaluate.

    Returns
    -------
    list of dict
        Each entry contains {'c', 'a', 'area', 'centroid'}.
    """
    results = []
    y_top = section.L1
    β = section.β  # Must be set externally

    for c in c_values:
        a = β * c
        y_min = y_top - a

        clipped_total = []
        for poly in [section.polygon_head_1, section.polygon_web, section.polygon_head_2]:
            part = clip_polygon_above_c(poly, y_min)
            if part:
                clipped_total.append(part)

        # Merge clipped parts
        merged = [pt for poly in clipped_total for pt in poly]
        if not merged:
            continue

        area, cx, cy = compute_area_and_centroid(merged)
        results.append({
            "c": c,
            "a": a,
            "area": area,
            "centroid": (cx, cy),
            "polygon": merged
        })

    return results
