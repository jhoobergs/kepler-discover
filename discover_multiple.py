import lightkurve as lk
import matplotlib.pyplot as plt
import argparse
parser = argparse.ArgumentParser(description='Find an exoplanet around a star.')
parser.add_argument('star', type=str, help='the star')
parser.add_argument('quarter', type=int, help='the quarter')
parser.add_argument('min_period', type=float, help='the minimal period')
parser.add_argument('max_period', type=float, help='the maximal period')
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
periodogram = flat.to_periodogram(method="bls", period=np.arange(args.min_period, args.max_period, (args.max_period - args.min_period) / 100))
periodogram.plot();
plt.show();

best_fit_period = periodogram.period_at_max_power
print('Best fit period: {:.3f}'.format(best_fit_period))
best_fit_duration = periodogram.duration_at_max_power
print('Best fit duration: {:.3f}'.format(best_fit_duration))
best_fit_depth = periodogram.depth_at_max_power
print('Best fit depth: {:.3f}'.format(best_fit_depth))
best_fit_time=periodogram.transit_time_at_max_power
print(best_fit_time)
folded = flat.fold(period=best_fit_period, t0=best_fit_time)
folded.scatter() # .errorbar();
plt.show();
folded.plot_river()
plt.show();

#seismology = periodogram.to_seismology()
#numax = seismology.estimate_numax()  
#deltanu = seismology.estimate_deltanu()
#print(numax)
#print(deltanu)
#seismology.plot_echelle()
#plt.show()
