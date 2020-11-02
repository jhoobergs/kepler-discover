import lightkurve as lk
import matplotlib.pyplot as plt
import argparse
parser = argparse.ArgumentParser(description='Find an exoplanet around a star.')
parser.add_argument('star', type=str, help='the star')
#parser.add_argument('min_period', type=float, help='the minimal period')
#parser.add_argument('max_period', type=float, help='the maximal period')
#parser.add_argument('step_size' type=float, help='the period step size')

args = parser.parse_args()
lcs = []
flat_lcs = []
trend_lcs = []
#lcfs = lk.search_lightcurvefile(args.star).download_all()
for quarter in range(1, 18):
    print(quarter)
    tpf = lk.search_targetpixelfile(args.star, quarter=quarter).download()
    if tpf is None:
        print("Missing", quarter)
        continue
    #lc = lk.search_lightcurvefile(args.star, quarter=quarter).download()
    #tpf.plot(frame=100, scale='log', show_colorbar=True)
    #plt.show()

    lc = tpf.to_lightcurve(aperture_mask=tpf.pipeline_mask)
    flat, trend = lc.flatten(window_length=301, return_trend=True)
    lcs.append(lc)
    flat_lcs.append(flat)
    trend_lcs.append(trend)
    #lc.plot()
    #plt.show();
def my_custom_corrector_func(lc):
    corrected_lc = lc.normalize().flatten(window_length=401)
    return corrected_lc
lc = lk.LightCurveCollection(lcs).stitch() #corrector_func=my_custom_corrector_func)
#lc = lcfs.PDCSAP_FLUX.stitch()
#lc.plot()
#plt.show()
#lc.scatter()
#plt.show()

flat = lk.LightCurveCollection(flat_lcs).stitch()
trend = lk.LightCurveCollection(trend_lcs).stitch()
#flat, trend = lc.flatten(window_length=301, return_trend=True)
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
    periodogram = flat.to_periodogram(method="bls", period=np.arange(min_period, max_period, 0.0001)) # (max_period - min_period) / 100))
    periodogram.plot();
    plt.show();

    best_fit_period = periodogram.period_at_max_power
    print('Best fit period: {:.3f}'.format(best_fit_period))
    best_fit_duration = periodogram.duration_at_max_power
    print('Best fit duration: {:.3f}'.format(best_fit_duration))
    best_fit_depth = periodogram.depth_at_max_power
    print('Best fit depth: {:.3f}'.format(best_fit_depth))
    print('Best fit transit time: {:.3f}'.format(periodogram.transit_time_at_max_power))
    flat.fold(period=best_fit_period, t0=periodogram.transit_time_at_max_power).bin().scatter() # .errorbar();
    plt.show();
    flat.fold(period=best_fit_period, t0=periodogram.transit_time_at_max_power).plot_river()
    plt.show();
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
        
    print("Period")
    period = float(input())
