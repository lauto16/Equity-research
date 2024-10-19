def zero_division(dividend, divisor):
    try:
        return dividend / divisor

    except ZeroDivisionError:
        return 0


def clear_number(value: str) -> float:
    """
    Uses: general parsing

    Args:
        value (str): str number with $,B and .

    Returns:
        float: parsed value without unnecesary symbols
    """
    original = value
    value = value.replace(',', '.')
    value = value.replace('$', '')
    value = value.replace('B', '')
    value = value.replace('%', '')
    value = value.replace(' ', '')

    if len(value) == 1 and '-' in value:
        value = value.replace('-', '0')

    try:
        if not ('B' in original):
            return float(value) / 1000
        return float(value)
    except Exception as e:
        print(f'error trying to convert {value} into a float')
        return value


def clear_hyphen(value):

    if len(value) == 1 and '-' in value:
        value = value.replace('-', '0')

    try:
        return float(value)

    except Exception as e:
        print(f'error trying to convert {value} into a float: ', e)
        return value
