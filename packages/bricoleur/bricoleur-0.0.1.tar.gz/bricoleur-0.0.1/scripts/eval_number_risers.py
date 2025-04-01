#! /usr/bin/env python3
"""
A script to verify the calculations for bric.stairs.number_risers.
"""

import argparse

import bricoleur as bric


def main():
    parser = argparse.ArgumentParser(description="number of risers")
    parser.add_argument(
        "-tr",
        "--total_rise",
        default=77.5,
        type=float,
        required=False,
        help="Provide the total rise",
    )
    parser.add_argument(
        "-xrh",
        "--max_riser_height",
        default=7,
        type=float,
        required=False,
        help="Provide the maximum riser height",
    )
    args = parser.parse_args()
    number_risers = bric.number_risers(
        total_rise = args.total_rise,
        max_riser_height = args.max_riser_height
    )
    print(number_risers)


if __name__ == "__main__":
    main()
