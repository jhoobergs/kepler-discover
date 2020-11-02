import lightkurve as lk
import matplotlib.pyplot as plt
import argparse
from scipy.interpolate import CubicSpline
import numpy as np

def is_there_a_planet(left, center, right):
    return \
    abs(1-left[0]) < 0.001 and abs(left[1]) < 0.001 and abs(left[2]) < 0.001 and \
    abs(center[0]) > 0.02 and abs(center[1]) < 0.01 and abs(center[2]) > 4 and \
    abs(1-right[0]) < 0.001 and abs(right[1]) < 0.001 and abs(right[2]) < 0.001 
    
def planet_score(left, center, right):
    return \
    abs(1-left[0])**2 + abs(left[1])**2 + abs(left[2])**2 + \
    abs(1-right[0])**2 + abs(right[1])**2 + abs(right[2])**2  + \
    abs(center[1])**2
    #abs(center[0]) > 0.02 and abs(center[1]) < 0.01 and abs(center[2]) > 4 and \
    


def process_folded_lc(folded, border=0.03, plots=False, prints=False):
    left_part = list(filter(lambda t: t < -border, folded.time))
    left_line = np.polyfit(left_part, folded.flux[:len(left_part)], 2)
    left_line_p = np.poly1d(left_line)
    right_part = list(filter(lambda t: t > border, folded.time))
    right_line = np.polyfit(right_part, folded.flux[-len(right_part):], 2)
    right_line_p = np.poly1d(right_line)
    center_part = folded.time[len(left_part):-len(right_part)]
    center_line = np.polyfit(center_part, folded.flux[len(left_part):-len(right_part)], 2)
    center_line_p = np.poly1d(center_line)
    #cs = CubicSpline(folded.time, folded.flux)
    left_range = np.arange(-0.5, -border, 0.001)
    right_range = np.arange(border, 0.5, 0.001)
    center_range = np.arange(-border, border, 0.001)
    if plots:
        folded.scatter() 
        plt.plot(left_range, left_line_p(left_range))
        plt.plot(right_range, right_line_p(right_range))
        plt.plot(center_range, center_line_p(center_range))
        plt.show();
    
    result = (left_line_p, center_line_p, right_line_p)
    if prints:
        print(result[0])
        print(result[1])
        print(result[2])
    return result

def find_planet_iter_per(star, quarter):
    tpf = lk.search_targetpixelfile(star, quarter=quarter).download()
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

    best_planet_score = None
    best_folded = None
    best_result = None
    best_interpolations = None
    for best_fit_period_start in np.arange(0.5, 30.1, 0.5): 
        periodogram = flat.to_periodogram(method="bls", period=np.arange(best_fit_period_start, best_fit_period_start + 0.5, 0.0001))
        best_fit_period = periodogram.period_at_max_power
        transit_time_at_max_power = periodogram.transit_time_at_max_power
        folded = flat.fold(period=best_fit_period, t0=transit_time_at_max_power)

        interpolations = process_folded_lc(folded)
        if is_there_a_planet(*interpolations):
            score = planet_score(*interpolations)
            # print(best_fit_period, transit_time_at_max_power, interpolations, score)
            if best_planet_score is None or score < best_planet_score:
                best_planet_score = score
                best_folded = folded
                best_result = (best_fit_period, transit_time_at_max_power)
                best_interpolations = interpolations
                # print(interpolations)
    #best_folded.bin().scatter() # .errorbar();
    #plt.show();
    #best_folded.plot_river()
    #plt.show();
    if best_result is not None:
        print(star, best_result[0], best_result[1])
    else:
        print(star, "No planet found")
    #print(best_interpolations)
