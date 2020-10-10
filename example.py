import lightkurve as lk
import matplotlib.pyplot as plt

tpf = lk.search_targetpixelfile("Kepler-10", quarter=3).download()
tpf.plot(frame=100, scale='log', show_colorbar=True)
plt.show()

lc = tpf.to_lightcurve(aperture_mask=tpf.pipeline_mask)
lc.plot()
plt.show();

flat, trend = lc.flatten(window_length=301, return_trend=True)
ax = lc.errorbar(label="Kepler-10")                   # plot() returns a matplotlib axes ...
trend.plot(ax=ax, color='red', lw=2, label='Trend');  # which we can pass to the next plot() to use the same axes
plt.show();

flat.errorbar(label="Kepler-10");
plt.show();

import numpy as np
periodogram = flat.to_periodogram(method="bls", period=np.arange(0.3, 1.5, 0.001))
periodogram.plot();
plt.show();

best_fit_period = periodogram.period_at_max_power
print('Best fit period: {:.3f}'.format(best_fit_period))
flat.fold(period=best_fit_period, t0=periodogram.transit_time_at_max_power).scatter() # .errorbar();
plt.show();
flat.fold(period=best_fit_period, t0=periodogram.transit_time_at_max_power).plot_river()
plt.show();

flat.fold(period=0.6, t0=periodogram.transit_time_at_max_power).scatter() # .errorbar();
plt.show();
flat.fold(period=0.6, t0=periodogram.transit_time_at_max_power).plot_river() # .errorbar();
plt.show();

