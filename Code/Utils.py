from fractions import Fraction
import re

def value_to_frac(value):
    allowed_denoms = (2, 4, 8, 16)
    best = None
    min_error = None
    for denom in allowed_denoms:
        numerator = round(value * denom)
        frac = Fraction(numerator, denom)
        error = abs(float(frac) - value)
        if (min_error is None) or (error < min_error):
            min_error = error
            best = frac
    
    whole = best.numerator // best.denominator
    remainder = best - whole
    if remainder:
        if whole:
            return f"{whole} {abs(remainder.numerator)}/{remainder.denominator}"
        else:
            return f"{remainder.numerator}/{remainder.denominator}"
    else:
        return f"{whole}"

def frac_to_value(str):
    str = str.strip()
    if ("." in str) or not (" " in str):
        return float(str)
    whole = str[:str.index(" ")]
    whole = float(re.sub(r'[^0-9]', '', whole))

    frac = str[str.index(" ") + 1:]
    frac = re.sub(r'[^0-9/]', '', frac)
    numerator = int(frac[:frac.index("/")])
    denominator = int(frac[frac.index("/") + 1:])
    return whole + numerator / denominator