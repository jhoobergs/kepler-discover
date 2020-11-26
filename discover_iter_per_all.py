import lightkurve as lk
import matplotlib.pyplot as plt
import argparse
from scipy.interpolate import CubicSpline
import numpy as np
from own import find_planet_iter_per

parser = argparse.ArgumentParser(description='Find an exoplanet around a star.')
parser.add_argument('quarter', type=int, help='the quarter')

args = parser.parse_args()

amount = int(input())

for i in range(amount):
    star = input()
    res = find_planet_iter_per(star, args.quarter);
    if res is None:
        print(star, -1)
    else:
        print(star, res)
