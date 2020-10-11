import lightkurve as lk
import matplotlib.pyplot as plt
star = 'Kepler-8'
max_period = 1
min_period = 15
lcfs = lk.search_lightcurvefile(star, mission='Kepler').download_all()
lc = lcfs.PDCSAP_FLUX.stitch()
lc.scatter()
def my_custom_corrector_func(lc):
    corrected_lc = lc.normalize().flatten(window_length=401)
    return corrected_lc
lc = lcfs.PDCSAP_FLUX.stitch(corrector_func=my_custom_corrector_func)
lc.scatter()
lc.fold(period=3.52254, t0=1.35).bin().scatter();

flat, trend = lc.flatten(window_length=301, return_trend=True)
ax = lc.errorbar(label=star)                   # plot() returns a matplotlib axes ...
trend.plot(ax=ax, color='red', lw=2, label='Trend');  # which we can pass to the next plot() to use the same axes

flat.errorbar(label=star);

import numpy as np
periodogram = flat.to_periodogram(method="bls", period=np.arange(min_period, max_period, (max_period - min_period) / 100))
periodogram.plot();

best_fit_period = periodogram.period_at_max_power
print('Best fit period: {:.3f}'.format(best_fit_period))
flat.fold(period=best_fit_period, t0=periodogram.transit_time_at_max_power).bin().scatter() # .errorbar();
flat.fold(period=best_fit_period, t0=periodogram.transit_time_at_max_power).plot_river()
plt.show();
plt.show()
