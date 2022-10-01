from doepy.build import box_behnken, central_composite, full_fact, frac_fact_res, plackett_burman, sukharev
import pytest
import numpy as np


def test_full_fact():
    factors = {'Pressure': [50, 60, 70], 'Temperature': [290, 320, 350], 'Flow rate': [0.09, 0.1]}
    df = full_fact(factors)
    assert len(df) == 3 * 3 * 2
    for factor, values in factors.items():
        assert set(df[factor]) == set(values)


def test_frac_fact_res():
    factors = {'A': [1, 5], 'B': [0.3, 0.7], 'C': [10, 15], 'D': [3, 7], 'E': [-2, -1]}
    df = frac_fact_res(factors, 3)
    assert len(df) == 2**5 / 2**(3-1)
    for factor, values in factors.items():
        assert set(df[factor]) == set(values), f'Incorrect values for {factor}'

    with pytest.raises(AssertionError):
        frac_fact_res(factors, 5)


def test_plackett_burman():
    factors = {'Pressure': [50, 70], 'Temperature': [290, 350], 'Flow rate': [0.9, 1.0]}
    df = plackett_burman(factors)
    assert len(df) == 4
    for factor, values in factors.items():
        assert set(df[factor]) == set(values), f'Incorrect values for {factor}'


def test_sukharev():
    factors = {'Pressure': [50, 70], 'Temperature': [290, 350], 'Flow rate': [0.9, 1.0]}
    df = sukharev(factors, 2)
    assert len(df) == 8
    for factor, values in factors.items():
        assert all(min(values) < v < max(values) for v in df[factor]), f'Incorrect values for {factor}'


def test_box_behnken():
    factors = {'Pressure': [50, 60, 70], 'Temperature': [290, 320, 350], 'Flow rate': [0.9, 1.0, 1.1]}
    df = box_behnken(factors)
    assert len(df) == 13
    for factor, values in factors.items():
        assert set(df[factor]) == set(values), f'Incorrect values for {factor}'

    factors_2 = {'Pressure': [50, 70], 'Temperature': [290, 350], 'Flow rate': [0.9, 1.1]}
    df = box_behnken(factors_2)
    assert len(df) == 13
    for factor, values in factors.items():
        assert set(df[factor]) == set(values), 'Adds mid point'

    factors = {'Pressure': [50, 60, 70], 'Temperature': [290, 320, 350], 'Flow rate': [0.9, 1.0, 1.1]}
    df = box_behnken(factors, center=4)
    assert len(df) == 13 + 3, "Adds center four times"
    for factor, values in factors.items():
        assert set(df[factor]) == set(values), f'Incorrect values for {factor}'


def test_central_composite():
    factors = {'Pressure': [50, 70], 'Temperature': [-10, 10]}
    df = central_composite(factors)
    assert len(df) == 12
    # add additional generated values (note that factors already has the center point added)
    factors['Pressure'].extend([60 + np.sqrt(2)*10, 60 - np.sqrt(2)*10])
    factors['Temperature'].extend([np.sqrt(2)*10, - np.sqrt(2)*10])
    for factor, values in factors.items():
        assert set(df[factor]) == set(values), f'Incorrect values for {factor}'
