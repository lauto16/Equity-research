import re


def clear_number(valor: str) -> float:
    # Delete simbol '$' and 'B' for formatting
    match = re.match(r'\$([0-9\.]+)', valor)
    numero = match.group(1)
    return float(numero)
