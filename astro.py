import lightkurve as lk
import matplotlib.pyplot as plt
import argparse
parser = argparse.ArgumentParser(description='Find seismographic data of exoplanet around a star.')
parser.add_argument('star', type=str, help='the star')
parser.add_argument('T', type=int, help='the t_eff')
parser.add_argument('freq1', type=int, help='the min freq')
parser.add_argument('freq2', type=int, help='the max freq')
args = parser.parse_args()

#KIC10963065 Kepler-408
search = lk.search_lightcurvefile(args.star, cadence='short', mission='Kepler')
print(search)

files = search[1:10].download_all()
files

lc = files.PDCSAP_FLUX.stitch()

lc.plot();
plt.show()

lc = lc.remove_outliers().remove_nans()
lc.plot();
plt.show()

pg = lc.to_periodogram(method='lombscargle', normalization='psd')
pg.plot(scale='log')
plt.show()

pg = lc.to_periodogram(method='lombscargle', normalization='psd', minimum_frequency=args.freq1, maximum_frequency=args.freq2)
ax = pg.plot()
pg.smooth(method='boxkernel', filter_width=1.).plot(ax=ax, label='Smoothed', c='red', lw=2);
plt.show()

print(pg.frequency_at_max_power)
print(pg.show_properties())

ax = pg.plot()
ax.axvline(pg.frequency_at_max_power.value, lw=5, ls='dashed');
plt.show()

snr = pg.flatten()
snr.plot();
plt.show()

seis = snr.to_seismology()
print(seis)

numax = seis.estimate_numax()
print(numax) # don't trust this blindly

seis.diagnose_numax();
plt.show()

deltanu = seis.estimate_deltanu()
ax = seis.diagnose_deltanu();
plt.show()

seis.plot_echelle();
plt.show()

seis.plot_echelle(smooth_filter_width=3., scale='log', cmap='viridis');
plt.show()

print(seis)
print(seis.deltanu)

#Teff = 6046
Teff = args.T

mass = seis.estimate_mass(Teff)
print(mass)
radius = seis.estimate_radius(Teff)
print(radius)
logg = seis.estimate_logg(Teff)
print(logg)


