import lightkurve as lk
import matplotlib.pyplot as plt
import argparse
from scipy.interpolate import CubicSpline
import numpy as np
from own import find_planet_combine_iter_per

amount = int(input())

for i in range(amount):
    star = input()
    res = find_planet_combine_iter_per(star);
    if res is None:
        print(star, -1)
    else:
        print(star, res)
