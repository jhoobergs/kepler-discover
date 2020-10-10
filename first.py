import lightkurve as lk
import matplotlib.pyplot as plt

pixels = lk.search_targetpixelfile("Kepler-10").download()
pixels.plot()
plt.show()

lightcurve = pixels.to_lightcurve()
lightcurve.plot()
plt.show()

exoplanet = lightcurve.flatten().fold(period=0.838)
exoplanet.plot()
plt.show()
