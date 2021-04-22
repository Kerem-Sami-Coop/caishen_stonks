from caishen_dashboard.data_processing import technical_indicators as TI
import pytest

def test_SMA_calculations():
    values = [1.0,2.0,3.0,4.0]
    lookback = 3
    expected_result = [-1.0,-1.0,2.0,3.0]
    output = TI.SMA(values, lookback)
    assert output == expected_result

def test_SMA_false_list():
    values = []
    lookback = 3
    with pytest.raises(Exception) as ex:
        TI.SMA(values, lookback)
    assert "The length of the values list is 0. It should be at least 1" in str(ex.value)

def test_SMA_false_type_lookback():
    values = [1.0,2.0,3.0,4.0]
    lookback = 2.5
    expected_output = "The lookback is expected to be an int, but it's type is " + str(type(lookback))
    with pytest.raises(Exception) as ex:
        TI.SMA(values, lookback)
    assert expected_output in str(ex.value)

def test_SMA_false_value_lookback():
    values = [1.0,2.0,3.0,4.0]
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
    values = [1.0,2.0,3.0,4.0,5.0]
    lookback = "fail"
    smoothing = 2
    expected_error = "The lookback is expected to be an int, but it's type is " + str(type(lookback))
    with pytest.raises(Exception) as ex:
        TI.EMA(values, lookback, smoothing)
    assert expected_error in str(ex.value)

def test_EMA_negative_lookback():
    values = [1.0,2.0,3.0,4.0,5.0]
    lookback = -1
    smoothing = 2
    expected_error = "The lookback value has to be a non negative integer, but it is set to " + str(lookback)
    with pytest.raises(Exception) as ex:
        TI.EMA(values, lookback, smoothing)
    assert expected_error in str(ex.value)

def test_EMA_false_type_smoothing():
    values = [1.0,2.0,3.0,4.0,5.0]
    lookback = 3
    smoothing = "fail"
    expected_error = "The smoothing value is expected to be a float, but it's type is " + str(smoothing)
    with pytest.raises(Exception) as ex:
        TI.EMA(values, lookback, smoothing)
    assert expected_error in str(ex.value)

def test_EMA_negative_smoothing():
    values = [1.0,2.0,3.0,4.0,5.0]
    lookback = 3
    smoothing = -2.0
    expected_error = "The smoothing value has to be a non negative float, but it is set to " + str(smoothing)
    with pytest.raises(Exception) as ex:
        TI.EMA(values, lookback, smoothing)
    assert expected_error in str(ex.value)

def test_EMA_calculations():
    values = [1.0,2.0,3.0,4.0,5.0]
    lookback = 4
    smoothing = 2.0
    expected_result = [-1.0,-1.0,-1.0,2.5,3.5]
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
    expected_result = [[-1, 0.5, 1.5, 2.5, 3.5], [-1, 1.5, 2.5, 3.5, 4.5], [-1, 2.5, 3.5, 4.5, 5.5]]
    output = TI.bollinger_bands(values, lookback)
    assert output == expected_result

def test_fibonacci_retractments_false_type_start_price():
    start_price = "fail"
    end_price = 20.0
    fibonacci_levels = [0.236, 0.764]
    with pytest.raises(Exception) as ex:
        TI.fibonacci_retractments(start_price, end_price, fibonacci_levels)
    expected_error = "The start price is expected to be a float but it is " +str(start_price)
    assert expected_error in str(ex.value)

def test_fibonacci_retractments_false_type_end_price():
    start_price = 10.0
    end_price = "fail"
    fibonacci_levels = [0.236, 0.764]
    with pytest.raises(Exception) as ex:
        TI.fibonacci_retractments(start_price, end_price, fibonacci_levels)
    expected_error = "The end price is expected to be a float but it is " +str(end_price)
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
