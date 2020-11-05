
import lightkurve as lk
import own
def get_flat(star, q):
    tpf = lk.search_targetpixelfile(star, quarter=q).download()
    lc = tpf.to_lightcurve(aperture_mask=tpf.pipeline_mask)
    flat, trend = lc.flatten(window_length=301, return_trend=True)
    return flat

data = {
    7: (get_flat("Kepler-7", 1), 4.882, 134.288),
    8: (get_flat("Kepler-8", 1), 3.520, 131.643)
        }

def calc(flat, period, t0):
    folded = flat.fold(period=period, t0=t0)
    interpolations = own.process_folded_lc(folded)
    print(interpolations)
    valid = own.is_there_a_planet(*interpolations)
    score = own.planet_score(*interpolations)
    print(score)
    return valid, score 

#def test_is_there_a_planet_kepler_7_half_period():
#    valid, score = calc(kepler_7_flat, 0.5*kepler_7_good_period, kepler_7_good_t)
#    assert valid == False

#def test_is_there_a_planet_kepler_7_ok():
#    valid, score = calc(kepler_7_flat, kepler_7_good_period, kepler_7_good_t)
#    assert valid == True

#def test_is_there_a_planet_kepler_7_two_period():
#    valid, score = calc(kepler_7_flat, 2*kepler_7_good_period, kepler_7_good_t)
#    assert valid == False

#def test_is_there_a_planet_kepler_7_three_period():
#    valid, score = calc(kepler_7_flat, 3*kepler_7_good_period, kepler_7_good_t)
#    assert valid == False

def helper_shift(star):
    flat, period, t = data[star]
    _, scoreLeft10 = calc(flat, period, t-period*0.1)
    _, scoreLeft20 = calc(flat, period, t-period*0.2)
    _, scoreLeft30 = calc(flat, period, t-period*0.3)
    _, scoreLeft40 = calc(flat, period, t-period*0.4)
    _, score = calc(flat, period, t)
    _, scoreRight10 = calc(flat, period, t+period*0.1)
    _, scoreRight20 = calc(flat, period, t+period*0.2)
    _, scoreRight30 = calc(flat, period, t+period*0.3)
    _, scoreRight40 = calc(flat, period, t+period*0.4)
    assert scoreLeft10 > score
    assert scoreLeft20 > score
    assert scoreLeft30 > score
    assert scoreLeft40 > score
    assert scoreRight10 > score
    assert scoreRight20 > score
    assert scoreRight30 > score
    assert scoreRight40 > score

def helper_harmonics(star):
    flat, period, t = data[star]
    _, scoreHalf = calc(flat, 0.5*period, t)
    _, score = calc(flat, period, t)
    _, scoreDouble = calc(flat, 2*period, t)
    _, scoreThree = calc(flat, 3*period, t)
    assert scoreHalf > score
    assert scoreDouble > score
    assert scoreThree > score

def test_planet_score_harmonics_kepler_7():
    helper_harmonics(7)

def test_planet_score_shift_kepler_7():
    helper_shift(7)


#def test_is_there_a_planet_kepler_8_half_period():
#    valid, score = calc(kepler_8_flat, 0.5*kepler_8_good_period, kepler_8_good_t)
#    assert valid == False

#def test_is_there_a_planet_kepler_8_ok():
#    valid, score = calc(kepler_8_flat, 2*kepler_8_good_period, kepler_8_good_t)
#    assert valid == True

#def test_is_there_a_planet_kepler_8_two_period():
#    valid, score = calc(kepler_8_flat, 2*kepler_8_good_period, kepler_8_good_t)
#    assert valid == False

#def test_is_there_a_planet_kepler_8_three_period():
#    valid, score = calc(kepler_8_flat, 3*kepler_8_good_period, kepler_8_good_t)
#    assert valid == False

def test_planet_score_harmonics_kepler_8():
    helper_harmonics(8)
def test_planet_score_shift_kepler_8():
    helper_shift(8)
