import lightkurve as lk
import matplotlib.pyplot as plt
import argparse
from scipy.interpolate import CubicSpline
import numpy as np
from own import process_folded_lc, is_there_a_planet, planet_score

parser = argparse.ArgumentParser(description='Find an exoplanet around a star.')
parser.add_argument('star', type=str, help='the star')
parser.add_argument('quarter', type=int, help='the quarter')

args = parser.parse_args()

tpf = lk.search_targetpixelfile(args.star, quarter=args.quarter).download()
#tpf.plot(frame=100, scale='log', show_colorbar=True)
#plt.show()

lc = tpf.to_lightcurve(aperture_mask=tpf.pipeline_mask)
#lc.plot()
#plt.show();

flat, trend = lc.flatten(window_length=301, return_trend=True)
#ax = lc.errorbar(label=args.star)                   # plot() returns a matplotlib axes ...
#trend.plot(ax=ax, color='red', lw=2, label='Trend');  # which we can pass to the next plot() to use the same axes
#plt.show();

#flat.errorbar(label=args.star);
#plt.show();

found_fit_periods = []
found_fit_times = []
# TODO
for best_fit_period in np.arange(4.5, 5.0, 0.01): 
    print(best_fit_period)
    for transit_time_at_max_power in np.arange(min(lc.time), min(lc.time) + best_fit_period, 0.01): # 0.001):
        # print(best_fit_period, transit_time_at_max_power)
        folded = flat.fold(period=best_fit_period, t0=transit_time_at_max_power)

        interpolations = process_folded_lc(folded)
        if is_there_a_planet(*interpolations):
            #folded.bin().scatter() # .errorbar();
            #plt.show();
            #folded.plot_river()
            #plt.show();
            print("Found", best_fit_period, transit_time_at_max_power)
            print(interpolations)
            found_fit_periods.append(best_fit_period)
            found_fit_times.append(transit_time_at_max_power)
print()

lowest_found_period = min(found_fit_periods)
highest_found_period = max(found_fit_periods)
best_planet_score = None
best_folded = None
best_result = None
best_interpolations = None
for best_fit_period in np.arange(lowest_found_period, highest_found_period + 0.01 , 0.001):
    print(best_fit_period)
    for transit_time_at_max_power in np.arange(min(lc.time), min(lc.time) + best_fit_period, 0.001):
        # print(best_fit_period, transit_time_at_max_power)
        folded = flat.fold(period=best_fit_period, t0=transit_time_at_max_power)

        interpolations = process_folded_lc(folded)
        if is_there_a_planet(*interpolations):
            score = planet_score(*interpolations)
            print(best_fit_period, transit_time_at_max_power, interpolations, score)
            if best_planet_score is None or score < best_planet_score:
                best_planet_score = score
                best_folded = folded
                best_result = (best_fit_period, transit_time_at_max_power)
                best_interpolations = interpolations
                # print(interpolations)
best_folded.bin().scatter() # .errorbar();
plt.show();
best_folded.plot_river()
plt.show();
print("Found", best_fit_period, transit_time_at_max_power)
print(best_interpolations)
