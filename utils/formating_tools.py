def clear_number_financials(value: str) -> float:
    """
    Uses: general parsing

    Args:
        value (str): str number with $,B and .

    Returns:
        float: parsed value without unnecesary symbols
    """
    num = 0
    original = value
    if value.count('.') >= 2:
        value = value.replace('.', '')
    for char in value:
        if char.isdigit():
            num += 1

    if num in [5, 6]:
        value = value.replace('.', '')

    value = value.replace(',', '.')
    value = value.replace('$', '')
    value = value.replace('B', '')
    value = value.replace('%', '')
    value = value.replace(' ', '')

    if len(value) == 1 and '-' in value:
        value = value.replace('-', '0')

    if value.count('.') >= 2:
        dot = value.find('.')
        value = list(value)
        value.pop(dot)
        value = ''.join(value)

    try:
        if not ('B' in original):
            return float(value) / 1000
        return float(value)
    except Exception as e:
        print(f'error trying to convert {value} into a float')
        return value


def clear_number_ratio(value):
    """
    Uses: general parsing for ratios

    Args:
        value (str): str number with $,B and .

    Returns:
        float: parsed value without unnecesary symbols
    """
    value = value.replace(',', '.')
    value = value.replace('%', '')
    value = value.replace(' ', '')

    if len(value) == 1 and '-' in value:
        value = value.replace('-', '0')
    try:
        return float(value)
    except Exception as e:
        print(f'error trying to convert {value} into a float: ', e)
        return value
