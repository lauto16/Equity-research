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

    try:
        if not ('B' in original):
            return float(value) / 1000
        return float(value)
    except Exception as e:
        print(f'error trying to convert {value} into a float')
        return value
