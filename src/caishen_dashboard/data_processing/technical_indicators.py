from typing import List
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
        average = sum(values[i:i + lookback]) / (1.0*lookback)
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
    num_values_processed: int = 0
    multiplier: float = smoothing / (1.0*(1 + lookback))
    # calculate EMA for all values except the first lookback # of values
    for i in range(lookback - 1):
        result.append(-1)
    # The EMA of the first N elements is equal to their average
    if len(values) >= lookback:
        ema = sum(values[:lookback]) / (1.0*(lookback))
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
        raise TypeError("The lookback is expected to be an int, but it's type is " + str(type(lookback)))
    if lookback < 0:
        raise ValueError("The lookback value has to be a non negative integer, but it is set to " + str(lookback))

    middle_band: List[float] = []
    upper_band: List[float] = []
    lower_band: List[float] = []

    for i in range(lookback - 1):
        middle_band.append(-1)
        upper_band.append(-1)
        lower_band.append(-1)
    for i in range(len(values) - lookback + 1):
        average = sum(values[i:i + lookback]) / (1.0*lookback)
        stdev = statistics.pstdev(values[i:i + lookback])
        middle_band.append(average)
        upper_band.append(average + 2 * stdev)
        lower_band.append(average - 2 * stdev)

    return [lower_band, middle_band, upper_band]

def fibonacci_retractments(start_price: float, end_price: float, fibonacci_levels: List[float] = [0.236, 0.382, 0.5, 0.618, 0.764]):
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
        raise TypeError("The start price is expected to be a float but it is " +str(start_price))
    if type(end_price) != float:
        raise TypeError("The end price is expected to be a float but it is " +str(end_price))
    
    price_difference = abs(end_price - start_price)
    multiplier = 1
    if end_price > start_price:
        multiplier = -1
    result: List[float] = []
    for level in fibonacci_levels:
        result.append(end_price + multiplier * price_difference * level)

    return result
