def calculate_and_plot_trend(lc, star):
    flat, trend = lc.flatten(window_length=301, return_trend=True)
    ax = lc.errorbar(label=star)                   # plot() returns a matplotlib axes ...
    trend.plot(ax=ax, color='red', lw=2, label='Trend');  # which we can pass to the next plot() to use the same axes
    return (flat, trend)
