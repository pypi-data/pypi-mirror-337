"""
Function for stair calculations
"""

import math


def number_risers(
    total_rise: float,
    max_riser_height: float = 7
    ) -> float:
    """
    Calculate the number of risers (steps) between the upper and lower finish
    levels.

    Parameters
    ----------
    total_rise : float
        The vertical distance between the finished flooring of the upper and
        the lower levels.
    max_riser_height : float
        The maximum riser height (usually from the building code).

    Returns
    -------
    no_risers
        The number of risers.

    Example
    -------

    >>> import bricoleur as bric
    >>> total_rise_datum = 77.5
    >>> max_riser_height_datum = 7
    >>> number_risers = bric.number_risers(
    >>>     total_rise = total_rise_datum,
    >>>     max_riser_height = max_riser_height_datum
    >>> )
    >>> print(number_risers)
    12

    """
    no_risers = math.ceil(total_rise / max_riser_height)
    return no_risers


__all__ = (
    "number_risers",
)
