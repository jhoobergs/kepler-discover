import lightkurve as lk

def calculate_and_plot_trend(lc, star):
    flat, trend = lc.flatten(window_length=301, return_trend=True)
    ax = lc.errorbar(label=star)                   # plot() returns a matplotlib axes ...
    trend.plot(ax=ax, color='red', lw=2, label='Trend');  # which we can pass to the next plot() to use the same axes
    return (flat, trend)

def combine_lcs_and_calculate_and_plot_trend(star, *input_lcs):
    lcs = []
    flat_lcs = []
    trend_lcs = []

    for lc in input_lcs:
        flat, trend = lc.flatten(window_length=301, return_trend=True)
        lcs.append(lc)
        flat_lcs.append(flat)
        trend_lcs.append(trend)
    lc = lk.LightCurveCollection(lcs).stitch() #corrector_func=my_custom_corrector_func)
    flat = lk.LightCurveCollection(flat_lcs).stitch()
    trend = lk.LightCurveCollection(trend_lcs).stitch()
    ax = lc.errorbar(label=star)                   # plot() returns a matplotlib axes ...
    trend.plot(ax=ax, color='red', lw=2, label='Trend');  # which we can pass to the next plot() to use the same axes

    return (lc, flat, trend)
