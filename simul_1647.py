import numpy as np
import matplotlib.pyplot as plt

transit = 11.259

planet1 = (1 - 0.8016, -0.017, 0.016, 134.737) # (depth, drop_start, drop_end, start)
planet2_start = -0.46
planet2_end= -0.4348
planet2_mean = (planet2_end + planet2_start) / 2
planet2 = (1 - 0.8326, planet2_start, planet2_end, planet1[3] + (1+planet2_mean) * transit)
print(planet2_mean)
print(planet2[3])

def calc_phase(start, period, value):
    diff = value - start
    cycli = int(diff / period)
    part = diff - cycli * period
    phase = part / period
    if phase < 0:
        phase += 1
        #print("HUH: ", start, period, value)
    if phase > 0.5:
        return -(1-phase)
    else:
        return phase

print(calc_phase(120,10,125) == 0.5)
print(calc_phase(120,10,126) == -0.4)
print(calc_phase(120,10,124) == 0.4)
print(calc_phase(120,10,115) == 0.5)
print(calc_phase(120,10,116) == -0.4)
print(abs(calc_phase(134.737, 11.259, 25.3852) - 0.287609912) < 0.001)

def calculate_planet_drop(planet, x):
    phase = calc_phase(planet1[3], transit, x)
    if planet[1] <= phase <= planet[2]:
        mean = (planet[1] + planet[2]) / 2
        return (1-(abs(mean-phase)/(mean-planet[1]))) * planet[0]
    else:
        return 0
            
    

step = 0.01
start = min(planet1[2], planet2[2])
end = 2000

light = np.ones(int((end-start)/step))

for i in range(len(light)):
    x = start + i * step
    light[i] -= calculate_planet_drop(planet1, x)
    light[i] -= calculate_planet_drop(planet2, x)

#plt.plot(light)
#plt.show()

def fold(light, fold_start, fold_period):
    res_x = []
    res_y = []
    for i in range(len(light)):
        x = start + i * step
        phase = calc_phase(fold_start, fold_period, x)
        res_x.append(phase)
        res_y.append(light[i])
    return (res_x, res_y)

def fold_plot(light, fold_start, fold_period):
    folded = fold(light, fold_start, fold_period)
    plt.scatter(folded[0], folded[1])
    plt.show()
    return folded

default_fold = fold_plot(light, planet1[3], transit)
fold_plot(light, 260.950, 0.750)


        
        

