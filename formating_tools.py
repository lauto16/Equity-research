def clear_number(value: str) -> float:
    """
    Uses: general parsing

    Args:
        value (str): str number with $,B and .

    Returns:
        float: parsed value without unnecesary symbols
    """

    value = value.replace(',', '')
    value = value.replace('$', '')
    value = value.replace('B', '')

    try:
        return float(value)
    except Exception as e:
        print(f'error trying to convert {value} into a float')
        return value


def special_clear(value: str) -> float:
    """
    Uses: sga parsing

    Args:
        value (str): str number with $,B and .

    Returns:
        float: parsed value
    """
    value = value.replace('$', '')
    value = value.replace('B', '')
    value = value.replace('.', '')

    try:
        return float(value)
    except Exception as e:
        print(f'error trying to convert {value} into a float')
        return value
