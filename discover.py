import lightkurve as lk
import matplotlib.pyplot as plt
import argparse
from scipy.interpolate import CubicSpline
from own import process_folded_lc, is_there_a_planet
parser = argparse.ArgumentParser(description='Find an exoplanet around a star.')
parser.add_argument('star', type=str, help='the star')
parser.add_argument('quarter', type=int, help='the quarter')
#parser.add_argument('min_period', type=float, help='the minimal period')
#parser.add_argument('max_period', type=float, help='the maximal period')
#parser.add_argument('step_size' type=float, help='the period step size')

args = parser.parse_args()

tpf = lk.search_targetpixelfile(args.star, quarter=args.quarter).download()
tpf.plot(frame=100, scale='log', show_colorbar=True)
plt.show()

lc = tpf.to_lightcurve(aperture_mask=tpf.pipeline_mask)
lc.plot()
plt.show();

flat, trend = lc.flatten(window_length=301, return_trend=True)
ax = lc.errorbar(label=args.star)                   # plot() returns a matplotlib axes ...
trend.plot(ax=ax, color='red', lw=2, label='Trend');  # which we can pass to the next plot() to use the same axes
plt.show();

flat.errorbar(label=args.star);
plt.show();

import numpy as np
print("From")
min_period=float(input())
while min_period != -1:
    print("To")
    max_period=float(input())
    periodogram = flat.to_periodogram(method="bls", period=np.arange(min_period, max_period, 0.0001))
    periodogram.plot();
    plt.show();

    best_fit_period = periodogram.period_at_max_power
    print('Best fit period: {:.3f}'.format(best_fit_period))
    best_fit_duration = periodogram.duration_at_max_power
    print('Best fit duration: {:.3f}'.format(best_fit_duration))
    best_fit_depth = periodogram.depth_at_max_power
    print('Best fit depth: {:.3f}'.format(best_fit_depth))
    print('Best fit transit time: {:.3f}'.format(periodogram.transit_time_at_max_power))
    folded = flat.fold(period=best_fit_period, t0=periodogram.transit_time_at_max_power)
    folded.bin().scatter() # .errorbar();
    plt.show();
    folded.plot_river()
    plt.show();

    interpolations=process_folded_lc(folded, prints=True, plots=True)
    valid=is_there_a_planet(*interpolations)
    print(valid)

    print("From")
    min_period=float(input())

print("Period")
period = float(input())
while period != -1:
    print("t0")
    t0 = float(input())

    folded = flat.fold(period=period, t0=t0)
    folded.bin().scatter() # .errorbar();
    plt.show();
    folded.plot_river()
    plt.show();

    process_folded_lc(folded)

    print("Period")
    period = float(input())
