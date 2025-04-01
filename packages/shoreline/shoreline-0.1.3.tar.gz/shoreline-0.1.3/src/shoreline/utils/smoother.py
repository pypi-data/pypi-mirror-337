import numpy as np
from shapely.geometry import LineString, Point

SMALL_EPSILON = 1e-10


def cast_smoothed_rays(
    input_linestring, window=500, ray_length=1000, right=False
) -> list[Point]:
    """
    Smooth rays cast from input LineString

    An implementation of the ray smoothing technique described by DSAS:
    Emily A Himmelstoss, Rachel E Henderson, Meredith G Kratzmann, and Amy S Farris.
    Digital shoreline analysis system (dsas) version 5.0 user guide.
    Technical Report, US Geological Survey, 2018
    """
    if window <= 0:
        raise ValueError("Smoothing window size must be positive")
    if ray_length <= 0:
        raise ValueError("Ray length must be positive")
    rays = []

    for vertex in input_linestring.coords:
        vertex_distance = input_linestring.project(Point(vertex))

        # Get points half window before / after, clamped to line ends
        smoother_start_pos = max(0, vertex_distance - window / 2)
        smoother_end_pos = min(input_linestring.length, vertex_distance + window / 2)

        # make points
        smoother_start_point = np.array(
            input_linestring.interpolate(smoother_start_pos).coords[0]
        )
        smoother_end_point = np.array(
            input_linestring.interpolate(smoother_end_pos).coords[0]
        )
        vertex_point = np.array(vertex)

        # Check for collinearity using cross product
        v1 = vertex_point - smoother_start_point
        v2 = smoother_end_point - smoother_start_point
        # Convert to 3D vectors by adding z=0 to keep NumPy 2 happy
        v1_3d = np.array([v1[0], v1[1], 0])
        v2_3d = np.array([v2[0], v2[1], 0])
        cross_prod = np.cross(v1_3d, v2_3d)[2]

        if (
            abs(cross_prod) < SMALL_EPSILON
        ):  # Using small epsilon for floating point comparison
            # For collinear points, use the direction vector directly
            direction = v2 / np.linalg.norm(v2)
            # Create perpendicular vector (consistently with non-collinear case)
            perp_vec = (
                np.array([direction[1], -direction[0]])
                if right
                else np.array([-direction[1], direction[0]])
            )
            ray = LineString([vertex, vertex + perp_vec * ray_length])
            rays.append(ray)
            continue

        # Original smoothing logic for non-collinear points

        # smoothing_vec will be rotated from the input LineString segment that vertex is on
        # if start_pos, vertex, and end_pos are not collinear
        # (i.e. the line has "turned" and the window has "seen" the turn)
        smoothing_vec = smoother_end_point - smoother_start_point
        perp_vec = (
            np.array([smoothing_vec[1], -smoothing_vec[0]])
            if right
            else np.array([-smoothing_vec[1], smoothing_vec[0]])
        )

        # Normalize to unit vector
        perp_vec = perp_vec / np.linalg.norm(perp_vec)
        ray = LineString([vertex, vertex + perp_vec * ray_length])
        rays.append(ray)

    return rays
