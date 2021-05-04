from typing import List, Tuple
from .errors import InvalidInputError
import statistics


def SMA(values: List[float], lookback: int = 14):
    """Calculates Simple Moving Average (SMA) for a given lookback.

    The lookback determines the rolling window for which the averages are taken over. For example,
    lookback = 20 calculates SMA20

    Args:
        values (List[float]): The list of float values to average
        lookback (int, optional): The lookback. Defaults to 14.

    Raises:
        InvalidInputError: The list "values" must not be empty
        InvalidInputError: The lookback has to be an int
        InvalidInputError: The lookback has to be non negative

    Returns:
        List[float]: The list of SMA values. This list has the same length as "values"
                     The first "lookback - 1" elements are set to -1 to indicate there
                     is no real calculation to be done for them
    Example:
        >>> from caishen_dashboard.data_processing.technical_indicators import SMA
        >>> SMA([1.0,2.0,3.0,4.0],3)
        [-1, -1, 2.0, 3.0]
    """

    # Error Checking
    if len(values) == 0:
        raise InvalidInputError("The length of the values list is 0. It should be at least 1")
    if type(lookback) is not int:
        raise TypeError("The lookback is expected to be an int, but it's type is " + str(type(lookback)))
    if lookback < 0:
        raise ValueError("The lookback value has to be a non negative integer, but it is set to " + str(lookback))

    result: List[float] = []

    # calculate SMA for all values except the first lookback ones
    for i in range(lookback - 1):
        result.append(-1)
    for i in range(len(values) - lookback + 1):
        average = sum(values[i:i + lookback]) / (1.0 * lookback)
        result.append(average)

    return result


def EMA(values: List[float], lookback: int = 12, smoothing: float = 2.0):
    """Calculates Exponential Moving Average (EMA) for a given lookback.

    The lookback determines the rolling window for which the averages are taken over. For example,
    lookback = 20 calculates EMA20

    The formula for EMA is EMA(t) = price(t) * multiplier + EMA(t-1)*(1-multiplier)
    where multiplier = smoothing / (1 + MIN(# of entries,lookback))

    Args:
        values (List[float]): The list of float values to average
        lookback (int, optional): The lookback. . Defaults to 12.
        smoothing (float, optional): Smoothing factor. Defaults to 2.0.

    Raises:
        InvalidInputError: The list "values" must not be empty
        InvalidInputError: The lookback has to be an int
        InvalidInputError: The lookback has to be non negative
        InvalidInputError: The smoothing has to be non negative

    Returns:
        List[float]: The list of EMA values. This list has the same length as "values"
                     The first "lookback - 1" elements are set to -1 to indicate there
                     is no real calculation to be done for them

    Example:
        >>> from caishen_dashboard.data_processing.technical_indicators import EMA
        >>> EMA([1.0,2.0,3.0,4.0,5.0],4,2.0)
        [-1, -1, -1, 2.5, 3.5]
    """
    # Error Checking
    if len(values) == 0:
        raise InvalidInputError("The length of the values list is 0. It should be at least 1")
    if type(lookback) is not int:
        raise TypeError("The lookback is expected to be an int, but it's type is " + str(type(lookback)))
    if lookback < 0:
        raise ValueError("The lookback value has to be a non negative integer, but it is set to " + str(lookback))
    if type(smoothing) is not float:
        raise TypeError("The smoothing value is expected to be a float, but it's type is " + str(smoothing))
    if smoothing < 0:
        raise ValueError("The smoothing value has to be a non negative float, but it is set to " + str(smoothing))

    result: List[float] = []
    ema: float = values[0]
    # num_values_processed: int = 0
    multiplier: float = smoothing / (1.0 * (1 + lookback))
    # calculate EMA for all values except the first lookback # of values
    for i in range(lookback - 1):
        result.append(-1)
    # The EMA of the first N elements is equal to their average
    if len(values) >= lookback:
        ema = sum(values[:lookback]) / (1.0 * (lookback))
        result.append(ema)
    for value in values[lookback:]:
        ema = value * multiplier + ema * (1 - multiplier)
        result.append(ema)

    return result


def bollinger_bands(values: List[float], lookback: int = 20):
    """Calculates upper (avg + 2 * stdev), middle (avg) and lower (avg - 2 * stdev) bollinger bands

    Args:
        values (List[float]): The list of float values to bollinger band
        lookback (int, optional): The lookback. Defaults to 20.

    Raises:
        InvalidInputError: The list "values" must not be empty
        InvalidInputError: The lookback has to be an int
        InvalidInputError: The lookback has to be non negative

    Returns:
        [List[float], List[float], List[float]: A list of lower_band, middle_band and upper_band lists, in that order
                                                The first "lookback - 1" elements are set to -1 to indicate there
                                                is no real calculation to be done for them

    Example:
        >>> from caishen_dashboard.data_processing.technical_indicators import bollinger_bands
        >>> bollinger_bands([1, 2, 3, 4, 5], 2)
        [[-1, 0.5, 1.5, 2.5, 3.5], [-1, 1.5, 2.5, 3.5, 4.5], [-1, 2.5, 3.5, 4.5, 5.5]]

    """
    # Error Checking
    if len(values) == 0:
        raise InvalidInputError("The length of the values list is 0. It should be at least 1")
    if type(lookback) is not int:
        raise TypeError(
            "The lookback is expected to be an int, but it's type is " + str(type(lookback)))
    if lookback < 0:
        raise ValueError(
            "The lookback value has to be a non negative integer, but it is set to " + str(lookback))

    middle_band: List[float] = []
    upper_band: List[float] = []
    lower_band: List[float] = []

    for i in range(lookback - 1):
        middle_band.append(-1)
        upper_band.append(-1)
        lower_band.append(-1)
    for i in range(len(values) - lookback + 1):
        average = sum(values[i:i + lookback]) / (1.0 * lookback)
        stdev = statistics.pstdev(values[i:i + lookback])
        middle_band.append(average)
        upper_band.append(average + 2 * stdev)
        lower_band.append(average - 2 * stdev)

    return [lower_band, middle_band, upper_band]


def fibonacci_retractments(start_price: float, end_price: float,
                           fibonacci_levels: List[float] = [0.236, 0.382, 0.5, 0.618, 0.764]):
    """Calculates Fibonacci retractment levels for the given start price, end price and fibonacci levels

    Args:
        start_price (float): The starting price - aka the first price in the time range
        end_price (float): The end price - aka the last price in the time range
        fibonacci_levels (List[float], optional): Set of fibonacci levels to calculate.
                                                  The levels are fed as floats, so 0.236 means 23.6%
                                                  Defaults to [0.236, 0.382, 0.5, 0.618, 0.764].

    Raises:
        InvalidInputError: The start_price must be float
        InvalidInputError: The end_price must be float
        InvalidInputError: The list "fibonacci_levels" must not be empty

    Returns:
        List[float]: The values of Fibonacci retractment levels, in the order of the "fibonacci_levels" list

    Example:
        >>> from caishen_dashboard.data_processing.technical_indicators import fibonacci_retractments
        >>> fibonacci_retractments(10.0, 20.0, [0.236,0.786])
        [17.64, 12.14]
        >>> fibonacci_retractments(20.0, 10.0, [0.236,0.786])
        [12.36, 17.86]
    """
    # Error Checking
    if type(start_price) != float:
        raise TypeError("The start price is expected to be a float but it is " + str(start_price))
    if type(end_price) != float:
        raise TypeError("The end price is expected to be a float but it is " + str(end_price))

    price_difference = abs(end_price - start_price)
    multiplier = 1
    if end_price > start_price:
        multiplier = -1
    result: List[float] = []
    for level in fibonacci_levels:
        result.append(end_price + multiplier * price_difference * level)

    return result


def SO(high_values: List[float], low_values: List[float], closing_values: List[float], K_lookback: int = 5,
       D_lookback: int = 3):
    """Calculates stochastic oscillator for the provided stock.

    Args:
        high_values (List[float]): A list of the highest stock value for each day in the last N days.
        low_values (List[float]): A list of the lowest stock value for each day in the last N days.
        closing_values (float): The closing prices for the last N days.
        K_lookback (int, optional): lookback days for the last 5 days.
        D_lookback (int, optional): lookback days for the last 3 days.
    Raises:
        InvalidInputError: The length of the lists are not matching
        TypeError: closing_values must be list
        TypeError: high_values must be list
        TypeError: low_values must be list
        TypeError: K_lookback must be int
        TypeError: D_lookback must be int
    Returns:
        Tuple(float, float): K score & D score
    Example:
        >>> from caishen_dashboard.data_processing.technical_indicators import stochastic_oscillator
        >>> stochastic_oscillator([100.0, 101.0, 104.0, 105.0, 100.0, 110.0, 108.0, 97.0],
        ...                       [99.0, 100.0, 99.0, 102.0, 98.0, 105.0, 95.0, 94.0],
        ...                       [100.50, 100.50, 103.0, 104.0, 99.0, 106.0, 95.0, 96.0])
        (0, 26.9841)
    """
    # Error Checking
    if type(closing_values) != list:
        raise TypeError("The closing_values is expected to be a list")
    if type(high_values) != list:
        raise TypeError("The high_values is expected to be a list")
    if type(low_values) != list:
        raise TypeError("The low_values is expected to be a list")
    if (len(high_values) != len(low_values)) or (len(high_values) != len(closing_values)):
        raise InvalidInputError("The length of values are mismatching")
    if type(K_lookback) != int:
        raise TypeError("The K_lookback is expected to be a int")
    if type(D_lookback) != int:
        raise TypeError("The D_lookback is expected to be a int")

    D_list = []
    for start, close in enumerate(closing_values[K_lookback - 1:]):
        highest = max(high_values[start:start + K_lookback])
        lowest = min(low_values[start:start + K_lookback])
        K_score = 100.0 * (close - lowest) / (highest - lowest)
        D_list.append(K_score)
    D_score = SMA(D_list[-D_lookback:], D_lookback)[-1]
    return K_score, D_score


def MACD(values: List[float], MACD_lookback: Tuple[int, int] = (12, 26), MACD_smoothing: Tuple[float, float] = (2.0, 2.0),
         signal_lookback: int = 9, signal_smoothing: float = 2.0):
    """Calculates Moving Average Convergence Divergence for a stock

    MACD uses different SMAs to identify support and resistance levels. The MACD not only determines whether a trend is up
    or down, but it the strength of buy and sell signals

    Args:
        values (List[float]): list of closing stock prices
        MACD_lookback (Tuple[int, int], optional): the lookback values used for creating MACD line
        signal_lookback (int, optional): the lookback value used for signal line
    Raises:
        TypeError: The signal lookback is expected to be integer
        TypeError: The MACD_lookback is expected to be a tuple
        TypeError: The signal lookback is expected to be integer

    Returns:
        Tuple[List(float), List(float)]: The lists represent the MACD values and the signal values

    Example:
        >>> from caishen_dashboard.data_processing.technical_indicators import MACD
        >>> MACD(values = [10.40, 10.50, 10.10, 10.48, 10.51, 10.80, 10.80, 10.71, 10.79, 11.21, 11.42, 11.84]
        ...      MACD_lookback = (3, 6), signal_lookback = 3)
        ([0.1642, 0.1539, 0.1089, 0.0944, 0.1658, 0.2126,0.2889], [0.1423, 0.1184, 0.1421, 0.1773, 0.2331])
    """
    # Error Checking
    if type(values) != list:
        raise TypeError("The values is expected to be a list but it is " + str(values))
    if type(MACD_lookback) != tuple:
        raise TypeError("The MACD_lookback is expected to be a tuple but it is " + str(MACD_lookback))
    if type(signal_lookback) != int:
        raise TypeError("The signal lookback is expected to be integer but it is " + str(signal_lookback))

    MACD_values = EMA(values, MACD_lookback[0], MACD_smoothing[0]) - EMA(values, MACD_lookback[1], MACD_smoothing[1])
    signal_values = EMA(MACD_values, signal_lookback, signal_smoothing)

    return MACD_values, signal_values


def RSI(values: List[float]):
    """Calculates Relative Strength Index for a stock

    The length of the provided list provides an implicit lookback period.

    Args:
        values (List[float]): list of closing stock prices
    Raises:
        TypeError: The values is expected to be a list

    Returns:
        float: The RSI score of a stock

    Example:
        >>> from caishen_dashboard.data_processing.technical_indicators import RSI
        >>> RSI([1.0, 1.2, 1.4, 1.1, 0.9])
        44.4445
    """
    # Error Checking
    if type(values) != list:
        raise TypeError("The values is expected to be a list but it is " + str(values))

    gain: List[float] = [0.0]
    loss: List[float] = [0.0]
    lookback = len(values)
    previous = values[0]
    for current in values[1:]:
        change = current - previous
        if change >= 0:
            gain.append(change)
            loss.append(0.0)
        else:
            gain.append(0.0)
            loss.append(abs(change))

    average_gain = SMA(gain, lookback)
    average_loss = SMA(loss, lookback)
    RS = average_gain / average_loss
    RSI = 100 - 100 / (1 + RS)

    return round(RSI, 4)
