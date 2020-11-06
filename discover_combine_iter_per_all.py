import lightkurve as lk
import matplotlib.pyplot as plt
import argparse
from scipy.interpolate import CubicSpline
import numpy as np
from own import find_planet_combine_iter_per

parser = argparse.ArgumentParser(description='Find an exoplanet around a star.')

args = parser.parse_args()

for i in range(1, 300):
    star = "Kepler-" + str(i)
    find_planet_combine_iter_per(star);
