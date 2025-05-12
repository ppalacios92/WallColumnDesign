"""
Module: wall_section.py
Description:
    Represents the cross-section of a reinforced concrete wall with two heads (cabezales)
    and a central web (alma). Includes separate polygon geometry and rebar coordinates.

Author: Ing. Patricio Palacios B., M.Sc.
Version: 1.2.0
Date: 2025-05-11
"""

from typing import Tuple, List


class WallSection:
    """
    Represents a vertical reinforced concrete wall section composed of:
    - a central web (alma),
    - a lower head (cabezal 2),
    - an upper head (cabezal 1).

    The section is fully centered with respect to the maximum head thickness.

    Coordinate system:
    - X: horizontal (thickness direction)
    - Y: vertical (height direction)
    - Origin: bottom-left of the section bounding box

    Parameters
    ----------
    L1 : float
        Total height of the wall (mm).
    thickness : float
        Wall thickness (mm).
    cover : float
        Free cover from edge to center of rebar (mm).
    inc_main : Tuple[int, int]
        (n_thickness, n_height) for web reinforcement.
    N1, N2 : float
        Heights of head 1 (top) and head 2 (bottom) respectively.
    W1, W2 : float
        Thicknesses of head 1 and 2 (mm).
    inc_N1, inc_N2 : Tuple[int, int]
        (n_thickness, n_height) for reinforcement in heads 1 and 2.
    """

    def __init__(
        self,
        L1: float,
        thickness: float,
        cover: float,
        inc_main: Tuple[int, int],
        N1: float, W1: float, inc_N1: Tuple[int, int],
        N2: float, W2: float, inc_N2: Tuple[int, int],
    ):
        self.L1 = L1
        self.thickness = thickness
        self.cover = cover

        # Head 1 (top)
        self.N1 = N1
        self.W1 = W1
        self.inc_N1 = inc_N1

        # Head 2 (bottom)
        self.N2 = N2
        self.W2 = W2
        self.inc_N2 = inc_N2

        # Web (alma)
        self.L_web = L1 - N1 - N2
        self.inc_main = inc_main

        # Geometry (polygons)
        self.polygon_head_1: List[Tuple[float, float]] = []
        self.polygon_head_2: List[Tuple[float, float]] = []
        self.polygon_web: List[Tuple[float, float]] = []

        # Reinforcement coordinates
        self.rebars_main: List[Tuple[float, float]] = []
        self.rebars_N1: List[Tuple[float, float]] = []
        self.rebars_N2: List[Tuple[float, float]] = []

    def __repr__(self):
        return (
            f"WallSection(L1={self.L1}, thickness={self.thickness}, cover={self.cover},\n"
            f"  web: H={self.L_web}, inc_main={self.inc_main},\n"
            f"  head_1: H={self.N1}, W={self.W1}, inc={self.inc_N1},\n"
            f"  head_2: H={self.N2}, W={self.W2}, inc={self.inc_N2})"
        )

    def generate_geometry(self):
        """
        Generates the polygons that define the outline of head 1, head 2, and web.
        Each is centered horizontally within the maximum total thickness.
        """

        # Determine maximum thickness and center offsets
        T_max = max(self.W1, self.W2, self.thickness)
        offset_web = (T_max - self.thickness) / 2
        offset_head1 = (T_max - self.W1) / 2
        offset_head2 = (T_max - self.W2) / 2

        # Bottom head 2
        self.polygon_head_2 = [
            (offset_head2, 0),
            (offset_head2 + self.W2, 0),
            (offset_head2 + self.W2, self.N2),
            (offset_head2, self.N2)
        ]

        # Top head 1
        self.polygon_head_1 = [
            (offset_head1, self.L1 - self.N1),
            (offset_head1 + self.W1, self.L1 - self.N1),
            (offset_head1 + self.W1, self.L1),
            (offset_head1, self.L1)
        ]

        # Web 
        self.polygon_web = [
            (offset_web, self.N2),
            (offset_web + self.thickness, self.N2),
            (offset_web + self.thickness, self.N2 + self.L_web),
            (offset_web, self.N2 + self.L_web)
        ]

    def generate_rebars(self):
        """
        Generates the (x, y) coordinates of all reinforcement bars.
        All positions are centered and offset by cover on all sides.
        """

        T_max = max(self.W1, self.W2, self.thickness)
        offset_web = (T_max - self.thickness) / 2
        offset_head1 = (T_max - self.W1) / 2
        offset_head2 = (T_max - self.W2) / 2

        # Web
        x0_web = offset_web + self.cover
        x1_web = offset_web + self.thickness - self.cover
        y0_web = self.N2 + self.cover + self.cover
        y1_web = self.N2 + self.L_web - self.cover - self.cover
        self.rebars_main = self._perimeter_coordinates(x0_web, x1_web, y0_web, y1_web,
                                                       self.inc_main[0], self.inc_main[1])

        # Head 1 (top)
        x0_c1 = offset_head1 + self.cover
        x1_c1 = offset_head1 + self.W1 - self.cover
        y0_c1 = self.L1 - self.N1 + self.cover
        y1_c1 = self.L1 - self.cover
        self.rebars_N1 = self._perimeter_coordinates(x0_c1, x1_c1, y0_c1, y1_c1,
                                                     self.inc_N1[0], self.inc_N1[1])

        # Head 2 (bottom)
        x0_c2 = offset_head2 + self.cover
        x1_c2 = offset_head2 + self.W2 - self.cover
        y0_c2 = self.cover
        y1_c2 = self.N2 - self.cover
        self.rebars_N2 = self._perimeter_coordinates(x0_c2, x1_c2, y0_c2, y1_c2,
                                                     self.inc_N2[0], self.inc_N2[1])

    def _perimeter_coordinates(self, x_start, x_end, y_start, y_end, nx, ny):
        """
        Creates rebar coordinates only along the perimeter of a rectangular zone.

        Parameters
        ----------
        x_start, x_end : float
            Horizontal bounds.
        y_start, y_end : float
            Vertical bounds.
        nx, ny : int
            Number of bars along X and Y (at least 2 each).

        Returns
        -------
        list of tuple
            Rebar coordinates along the perimeter.
        """
        coords = []

        # Horizontal sides
        x_coords = [x_start + i * (x_end - x_start) / (nx - 1) for i in range(nx)]
        coords += [(x, y_start) for x in x_coords]
        coords += [(x, y_end) for x in x_coords]

        # Vertical sides
        y_coords = [y_start + j * (y_end - y_start) / (ny - 1) for j in range(1, ny - 1)]
        coords += [(x_start, y) for y in y_coords]
        coords += [(x_end, y) for y in y_coords]

        return coords
