import lightkurve as lk
import matplotlib.pyplot as plt
import argparse
from scipy.interpolate import UnivariateSpline
import numpy as np

def is_there_a_planet(left, center, right, left_stats, center_stats, right_stats):
    

    return \
    abs(1-left[0]) < 0.01 and abs(left[1]) < 0.01 and \
    abs(center[0]) > 0.02 and abs(center[1]) < 0.01 and abs(center[2]) > 2 and \
    abs(1-right[0]) < 0.01 and abs(right[1]) < 0.01 and \
    left_stats[0] < 0.001 and center_stats[0] < 0.001 and right_stats[0] < 0.001 # and \
    #abs(1-left[0]) < 0.01 and abs(left[1]) < 0.01 and abs(left[2]) < 0.01 and \
    #abs(1-right[0]) < 0.01 and abs(right[1]) < 0.01 and abs(right[2]) < 0.01 
    
def planet_score(left, center, right, left_stats, center_stats, right_stats):
    L = left.integ()
    C = center.integ()
    R = right.integ()
    return abs(1 - (L(0)-L(-0.5) + R(0.5) - R(0)))
    #return \
    #10*abs(left[1])**1 + \
    #10*abs(right[1])**1 + \
    #abs(center[1])**1
    #abs(1-left[0])**1 + abs(left[1])**1 + \
    #abs(1-right[0])**1 + abs(right[1])**1 + \
    #abs(center[1])**1
    

def process_folded_lc(folded, border=0.03, plots=False, prints=False):
    left_part = list(filter(lambda t: t < -border, folded.time))
    left_flux = folded.flux[:len(left_part)]
    left_valid_idx = np.isfinite(left_flux)
    left_line, left_stats = np.polyfit(np.array(left_part)[left_valid_idx], left_flux[left_valid_idx], 1, full=True)[:2]
    left_line_p = np.poly1d(left_line)

    right_part = list(filter(lambda t: t > border, folded.time))
    right_flux = folded.flux[-len(right_part):]
    right_valid_idx = np.isfinite(right_flux)
    right_line, right_stats = np.polyfit(np.array(right_part)[right_valid_idx], right_flux[right_valid_idx], 1, full=True)[:2]
    right_line_p = np.poly1d(right_line)

    center_part = folded.time[len(left_part):-len(right_part)]
    center_line, center_stats = np.polyfit(center_part, folded.flux[len(left_part):-len(right_part)], 2, full=True)[:2]
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
    
    result = (left_line_p, center_line_p, right_line_p, left_stats, center_stats, right_stats)
    if prints:
        print(result[0], result[3])
        print(result[1], result[4])
        print(result[2], result[5])
    return result

def find_planet_iter_per(star, quarter):
    tpf = lk.search_targetpixelfile(star, quarter=quarter).download()
    if tpf is None:
        print(star, "No planet found")
        return


    lc = tpf.to_lightcurve(aperture_mask=tpf.pipeline_mask)

    flat, trend = lc.flatten(window_length=301, return_trend=True)

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
        #if is_there_a_planet(*interpolations):
        score = planet_score(*interpolations)
        # print(best_fit_period, transit_time_at_max_power, interpolations, score)
        if best_planet_score is None or score < best_planet_score:
            #print(score)
            interpolations = process_folded_lc(folded, plots=False)

            best_planet_score = score
            best_folded = folded
            best_result = (best_fit_period, transit_time_at_max_power)
            best_interpolations = interpolations
            # print(interpolations)
    if best_result is not None:
        process_folded_lc(best_folded, plots= False)
        print(star, str(best_result[0])[:-2], best_result[1], best_planet_score)
    else:
        print(star, "No planet found")
    #print(best_interpolations)

def combine(star):
    lcs = []
    flat_lcs = []
    trend_lcs = []
    for quarter in range(1, 18):
        tpf = lk.search_targetpixelfile(star, quarter=quarter).download()
        if tpf is None:
            # print("Missing", quarter)
            continue

        lc = tpf.to_lightcurve(aperture_mask=tpf.pipeline_mask)
        flat, trend = lc.flatten(window_length=301, return_trend=True)
        lcs.append(lc)
        flat_lcs.append(flat)
        trend_lcs.append(trend)
        lc = lk.LightCurveCollection(lcs).stitch() 

    if len(lcs) == 0:
        return None
    flat = lk.LightCurveCollection(flat_lcs).stitch()
    trend = lk.LightCurveCollection(trend_lcs).stitch()
    
    return flat, trend



def find_planet_combine_iter_per(star):
    res = combine(star)
    if res is None:
        print(star, "No planet found")
    flat, trend = res
    best_planet_score = None
    best_folded = None
    best_result = None
    best_interpolations = None
    #for best_fit_period_start in np.arange(0.5, 700.1, 0.5): 
    ranges = np.logspace(0,11, num=50, base=2) / 2
    for i in range(len(ranges)-1):
        best_fit_period_start = ranges[i]
        best_fit_period_end = ranges[i+1]
        diff = best_fit_period_end - best_fit_period_start 
        periodogram = flat.to_periodogram(method="bls", period=np.arange(best_fit_period_start, best_fit_period_end, max(0.0001, diff/10000)))
        best_fit_period = periodogram.period_at_max_power
        transit_time_at_max_power = periodogram.transit_time_at_max_power
        folded = flat.fold(period=best_fit_period, t0=transit_time_at_max_power)

        interpolations = process_folded_lc(folded)
        #if is_there_a_planet(*interpolations):
        score = planet_score(*interpolations)
        # print(best_fit_period, transit_time_at_max_power, interpolations, score)
        if best_planet_score is None or score < best_planet_score:
            #print(score)
            interpolations = process_folded_lc(folded, plots=False)

            best_planet_score = score
            best_folded = folded
            best_result = (best_fit_period, transit_time_at_max_power)
            best_interpolations = interpolations
            # print(interpolations)
    if best_result is not None:
        process_folded_lc(best_folded, plots= False)
        print(star, str(best_result[0])[:-2], best_result[1], best_planet_score)
    else:
        print(star, "No planet found")
    #print(best_interpolations)
