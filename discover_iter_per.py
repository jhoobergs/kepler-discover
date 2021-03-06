import lightkurve as lk
import matplotlib.pyplot as plt
import argparse
from scipy.interpolate import CubicSpline
import numpy as np
from own import find_planet_iter_per

parser = argparse.ArgumentParser(description='Find an exoplanet around a star.')
parser.add_argument('star', type=str, help='the star')
parser.add_argument('quarter', type=int, help='the quarter')

args = parser.parse_args()

find_planet_iter_per(args.star, args.quarter);
