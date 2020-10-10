import lightkurve as lk
import matplotlib.pyplot as plt
import argparse
parser = argparse.ArgumentParser(description='Find an exoplanet around a star.')
parser.add_argument('star', type=str, help='the star')
parser.add_argument('min_period', type=float, help='the minimal period')
parser.add_argument('max_period', type=float, help='the maximal period')
#parser.add_argument('step_size' type=float, help='the period step size')

args = parser.parse_args()
lcs = []
flat_lcs = []
trend_lcs = []
#lcfs = lk.search_lightcurvefile(args.star).download_all()
for quarter in range(1, 18):
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
periodogram = flat.to_periodogram(method="bls", period=np.arange(args.min_period, args.max_period, (args.max_period - args.min_period) / 100))
periodogram.plot();
plt.show();

best_fit_period = periodogram.period_at_max_power
print('Best fit period: {:.3f}'.format(best_fit_period))
flat.fold(period=best_fit_period, t0=periodogram.transit_time_at_max_power).scatter() # .errorbar();
plt.show();
flat.fold(period=best_fit_period, t0=periodogram.transit_time_at_max_power).plot_river()
plt.show();
