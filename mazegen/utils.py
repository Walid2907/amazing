def set_42_limits(width: int, height: int) -> list[tuple[int, int]]:
    """
    Compute the coordinates that form the '42' pattern inside the maze.

    The pattern is centered relative to the maze dimensions.

    Args:
        width: Width of the maze.
        height: Height of the maze.

    Returns:
        A list of coordinate tuples representing the '42' pattern cells.
    """
    center_r = height // 2
    center_c = width // 2

    coords_fc: list[tuple[int, int]] = [
        (0, -1), (0, -2), (0, -3), (-1, -3),
        (-2, -3), (1, -1), (2, -1), (0, 1),
        (1, 1), (2, 1), (2, 2), (2, 3),
        (0, 2), (0, 3), (-1, 3), (-2, 3),
        (-2, 2), (-2, 1),
    ]

    form_42: list[tuple[int, int]] = []
    for dr, dc in coords_fc:
        target_r = center_r + dr
        target_c = center_c + dc
        form_42.append((target_r, target_c))

    return form_42
