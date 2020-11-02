import numpy as np
import matplotlib.pyplot as plt

def is_there_a_planet(left, center, right):
    return \
    abs(1-left[0]) < 0.001 and abs(left[1]) < 0.001 and abs(left[2]) < 0.001 and \
    abs(center[0]) > 0.02 and abs(center[1]) < 0.01 and abs(center[2]) > 4 and \
    abs(1-right[0]) < 0.001 and abs(right[1]) < 0.001 and abs(right[2]) < 0.001 


def process_folded_lc(folded, border=0.03, plots=False, prints=False):
    left_part = list(filter(lambda t: t < -border, folded.time))
    left_line = np.polyfit(left_part, folded.flux[:len(left_part)], 2)
    left_line_p = np.poly1d(left_line)
    right_part = list(filter(lambda t: t > border, folded.time))
    right_line = np.polyfit(right_part, folded.flux[-len(right_part):], 2)
    right_line_p = np.poly1d(right_line)
    center_part = folded.time[len(left_part):-len(right_part)]
    center_line = np.polyfit(center_part, folded.flux[len(left_part):-len(right_part)], 2)
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
    
    result = (left_line_p, center_line_p, right_line_p)
    if prints:
        print(result[0])
        print(result[1])
        print(result[2])
    return result

