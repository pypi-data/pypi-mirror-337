from pytest import approx, mark

import bricoleur as bric


@mark.parametrize(
    "total_rise, max_riser_height, expected",
    [
        (77.5, 7, 12),
        (77, 7, 11),
    ],
)


def test_number_risers(total_rise, max_riser_height, expected):
    result = bric.number_risers(
        total_rise=total_rise, max_riser_height=max_riser_height
    )
    assert result == expected
