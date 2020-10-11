import math

def au_to_m(val):
    return val * 1.495978707*10**11

def m_to_jup(val):
    return val / (7.1492*10**7)

def radius(a_in_au, dt_in_years, P_in_years):
    left = dt_in_years/P_in_years
    r_in_au = left * math.pi * a_in_au
    r_in_m = au_to_m(r_in_au)
    r_in_jup = m_to_jup(r_in_m)
    return r_in_jup

def radius_by_star_radius(r_star_in_r0, drop):
    tmp = drop*(r_star_in_r0*6.957*10**8)**2
    return tmp**(0.5) / (7.1492*10**7)

# Kepler 15b
print("Kepler 15b")
a_in_au = 0.05714
dt_in_years = 0.125 / 365
P_in_years = 4.95 / 365
print(radius(a_in_au, dt_in_years, P_in_years))
print(radius_by_star_radius(0.992, 0.011127))

print("Kepler 4b")
a_in_au = 0.04558
dt_in_years = 0.125 / 365
P_in_years = 3.250 / 365
#P_in_years = 3.2135 / 365
print(radius(a_in_au, dt_in_years, P_in_years))
print(radius_by_star_radius(1.555, 0.00087))
