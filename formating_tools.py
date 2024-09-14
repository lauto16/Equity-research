import re


def clear_number(value: str) -> float:
    """_summary_
    Delete simbol '$' and 'B' for formatting
    if the value does not have a simbol, it will return the same value

    Args:
        value (str): a financial value scraped

    Returns:
        float: a financial value filtered
    """
    try:
        match = re.match(r'\$([0-9\.]+)', value)
        numero = match.group(1)
        return float(numero)
    except AttributeError:
        return value
