import lightkurve as lk
import matplotlib.pyplot as plt
import argparse
from scipy.interpolate import CubicSpline
import numpy as np
from own import find_planet_combine_iter_per

parser = argparse.ArgumentParser(description='Find an exoplanet around a star.')
parser.add_argument('star', type=str, help='the star')

args = parser.parse_args()

find_planet_combine_iter_per(args.star);
