from caishen_dashboard.data_processing import technical_indicators as TI
import pytest


def test_SMA_calculations():
    values = [1.0, 2.0, 3.0, 4.0]
    lookback = 3
    expected_result = [-1.0, -1.0, 2.0, 3.0]
    output = TI.SMA(values, lookback)
    assert output == expected_result


def test_SMA_false_list():
    values = []
    lookback = 3
    with pytest.raises(Exception) as ex:
        TI.SMA(values, lookback)
    assert "The length of the values list is 0. It should be at least 1" in str(ex.value)


def test_SMA_false_type_lookback():
    values = [1.0, 2.0, 3.0, 4.0]
    lookback = 2.5
    expected_output = "The lookback is expected to be an int, but it's type is " + str(type(lookback))
    with pytest.raises(Exception) as ex:
        TI.SMA(values, lookback)
    assert expected_output in str(ex.value)


def test_SMA_false_value_lookback():
    values = [1.0, 2.0, 3.0, 4.0]
    lookback = -1
    with pytest.raises(Exception) as ex:
        TI.SMA(values, lookback)
    assert "The lookback value has to be a non negative integer, but it is set to -1" in str(ex.value)


def test_EMA_false_list():
    values = []
    lookback = 3
    smoothing = 2
    expected_error = "The length of the values list is 0. It should be at least 1"
    with pytest.raises(Exception) as ex:
        TI.EMA(values, lookback, smoothing)
    assert expected_error in str(ex.value)


def test_EMA_false_type_lookback():
    values = [1.0, 2.0, 3.0, 4.0, 5.0]
    lookback = "fail"
    smoothing = 2
    expected_error = "The lookback is expected to be an int, but it's type is " + str(type(lookback))
    with pytest.raises(Exception) as ex:
        TI.EMA(values, lookback, smoothing)
    assert expected_error in str(ex.value)


def test_EMA_negative_lookback():
    values = [1.0, 2.0, 3.0, 4.0, 5.0]
    lookback = -1
    smoothing = 2
    expected_error = "The lookback value has to be a non negative integer, but it is set to " + str(lookback)
    with pytest.raises(Exception) as ex:
        TI.EMA(values, lookback, smoothing)
    assert expected_error in str(ex.value)


def test_EMA_false_type_smoothing():
    values = [1.0, 2.0, 3.0, 4.0, 5.0]
    lookback = 3
    smoothing = "fail"
    expected_error = "The smoothing value is expected to be a float, but it's type is " + str(smoothing)
    with pytest.raises(Exception) as ex:
        TI.EMA(values, lookback, smoothing)
    assert expected_error in str(ex.value)


def test_EMA_negative_smoothing():
    values = [1.0, 2.0, 3.0, 4.0, 5.0]
    lookback = 3
    smoothing = -2.0
    expected_error = "The smoothing value has to be a non negative float, but it is set to " + str(smoothing)
    with pytest.raises(Exception) as ex:
        TI.EMA(values, lookback, smoothing)
    assert expected_error in str(ex.value)


def test_EMA_calculations():
    values = [1.0, 2.0, 3.0, 4.0, 5.0]
    lookback = 4
    smoothing = 2.0
    expected_result = [-1.0, -1.0, -1.0, 2.5, 3.5]
    output = TI.EMA(values, lookback, smoothing)
    assert output == expected_result


def test_bollinger_bands_empty_list():
    values = []
    lookback = 2
    expected_error = "The length of the values list is 0. It should be at least 1"
    with pytest.raises(Exception) as ex:
        TI.bollinger_bands(values, lookback)
    assert expected_error in str(ex.value)


def test_bollinger_bands_false_type_lookback():
    values = [1, 2, 3, 7, 5]
    lookback = "fail"
    expected_error = "The lookback is expected to be an int, but it's type is " + str(type(lookback))
    with pytest.raises(Exception) as ex:
        TI.bollinger_bands(values, lookback)
    assert expected_error in str(ex.value)


def test_bollinger_bands_negative_lookback():
    values = [1, 2, 3, 7, 5]
    lookback = -1
    expected_error = "The lookback value has to be a non negative integer, but it is set to " + str(lookback)
    with pytest.raises(Exception) as ex:
        TI.bollinger_bands(values, lookback)
    assert expected_error in str(ex.value)


def test_bollinger_bands_calculations():
    values = [1, 2, 3, 4, 5]
    lookback = 2
    expected_result = ([-1, 0.5, 1.5, 2.5, 3.5], [-1, 1.5, 2.5, 3.5, 4.5], [-1, 2.5, 3.5, 4.5, 5.5])
    output = TI.bollinger_bands(values, lookback)
    assert output == expected_result


def test_fibonacci_retractments_false_type_start_price():
    start_price = "fail"
    end_price = 20.0
    fibonacci_levels = [0.236, 0.764]
    with pytest.raises(Exception) as ex:
        TI.fibonacci_retractments(start_price, end_price, fibonacci_levels)
    expected_error = "The start price is expected to be a float but it is " + str(start_price)
    assert expected_error in str(ex.value)


def test_fibonacci_retractments_false_type_end_price():
    start_price = 10.0
    end_price = "fail"
    fibonacci_levels = [0.236, 0.764]
    with pytest.raises(Exception) as ex:
        TI.fibonacci_retractments(start_price, end_price, fibonacci_levels)
    expected_error = "The end price is expected to be a float but it is " + str(end_price)
    assert expected_error in str(ex.value)


def test_fibonacci_retractments_rising_price():
    start_price = 10.0
    end_price = 20.0
    fibonacci_levels = [0.236, 0.764]
    expected_result = [17.64, 12.36]
    output = TI.fibonacci_retractments(start_price, end_price, fibonacci_levels)
    assert output == expected_result


def test_fibonacci_retractments_falling_price():
    start_price = 20.0
    end_price = 10.0
    fibonacci_levels = [0.236, 0.764]
    expected_result = [12.36, 17.64]
    output = TI.fibonacci_retractments(start_price, end_price, fibonacci_levels)
    assert output == expected_result


def test_stochastic_oscillator_success():
    high_values = [100.0, 101.0, 104.0, 105.0, 100.0, 110.0, 108.0, 97.0]
    low_values = [99.0, 100.0, 99.0, 102.0, 98.0, 105.0, 95.0, 94.0]
    closing_values = [100.50, 100.50, 103.0, 104.0, 99.0, 106.0, 95.0, 96.0]
    K_lookback = 5
    D_lookback = 3
    output = TI.SO(high_values, low_values, closing_values, K_lookback, D_lookback)
    assert [round(x, 4) for x in output[0]] == [14.2857, 66.6667, 0.0, 12.5]
    assert [round(x, 4) for x in output[1]] == [-1, -1, 26.9841, 26.3889]


def test_stochastic_oscillator_fail_high_values():
    high_values = "fail"
    low_values = [99.0, 100.0, 99.0, 102.0, 98.0, 105.0, 95.0]
    closing_values = [100.50, 100.50, 103.0, 104.0, 99.0, 106.0, 95.0]
    K_lookback = 5
    D_lookback = 3
    with pytest.raises(Exception) as ex:
        TI.SO(high_values, low_values, closing_values, K_lookback, D_lookback)
    assert "is expected to be a list" in str(ex.value)


def test_MACD_success():
    values = [10.40, 10.50, 10.10, 10.48, 10.51, 10.80, 10.80, 10.71, 10.79, 11.21, 11.42, 11.84]
    output = TI.MACD(values=values, MACD_lookback=(3, 6), signal_lookback=3)
    assert [round(x, 4) for x in output[0]] == [-1, -1, -1, -1, -1, 0.1642, 0.1539, 0.1089, 0.0945, 0.1658, 0.2126, 0.2889]
    assert [round(x, 4) for x in output[1]] == [-1, -1, -1, -1, -1, -1, -1, 0.1423, 0.1184, 0.1421, 0.1773, 0.2331]


def test_RSI_success():
    values = [1.0, 1.2, 1.4, 1.1, 0.9]
    output = TI.RSI(values=values, lookback=3)
    assert [-1, -1, 0.0, 57.1429, 28.5714] == [round(x, 4) for x in output]
